<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { api } from '../../api';
import BarLayout from '../../components/BarLayout.vue';
import type { ProductState } from '../../types';

const productStates = ref<ProductState[]>([]);
const error = ref('');
const loading = ref(false);
const searchQuery = ref('');
const expandedCategories = ref<Set<string>>(new Set());

const groupByCategory = (productStates: ProductState[]) => {
  const categoryMap = new Map<string, { name: string; products: ProductState[] }>();
  productStates.forEach((ps) => {
    const categoryId = ps.product.category_id;
    const categoryName = ps.product.category?.name || 'Uncategorized';
    if (!categoryMap.has(categoryId)) {
      categoryMap.set(categoryId, { name: categoryName, products: [] });
    }
    categoryMap.get(categoryId)?.products.push(ps);
  });
  return Array.from(categoryMap.entries()).map(([id, { name, products }]) => ({ id, name, products }));
};

const filteredCategories = computed(() => {
  const categories = groupByCategory(productStates.value);
  const query = searchQuery.value.toLowerCase().trim();

  if (!query) return categories;

  return categories
    .map((category) => ({
      ...category,
      products: category.products.filter((ps) =>
        ps.product.name.toLowerCase().includes(query) ||
        ps.product.category?.name.toLowerCase().includes(query)
      ),
    }))
    .filter((category) => category.products.length > 0);
});

const toggleCategory = (categoryId: string) => {
  if (expandedCategories.value.has(categoryId)) {
    expandedCategories.value.delete(categoryId);
  } else {
    expandedCategories.value.add(categoryId);
  }
};

const fetchData = async () => {
  loading.value = true;
  try {
    productStates.value = await api.bar.listStates();
    const categories = groupByCategory(productStates.value);
    expandedCategories.value.clear();
    categories.forEach((category) => {
      expandedCategories.value.add(category.id);
    });
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const setState = async (productId: string, state: 'enough' | 'required' | 'emergency') => {
  try {
    let result;
    if (state === 'enough') {
      result = await api.bar.setEnough(productId);
    } else if (state === 'required') {
      result = await api.bar.setRequired(productId);
    } else {
      result = await api.bar.setEmergency(productId);
    }
    productStates.value = result;
  } catch (err: any) {
    error.value = err.message;
  }
};

onMounted(fetchData);
</script>

<template>
  <BarLayout>
    <template #title>Product Status Management</template>

    <template #top-actions>
      <button
        @click="fetchData"
        class="bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors font-medium text-sm whitespace-nowrap"
        :disabled="loading"
      >
        {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
    </template>

    <div class="max-w-6xl">
      <!-- Search Bar -->
      <div class="mb-6">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search products or categories..."
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500 text-sm"
          />
          <svg
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-3 top-3 w-5 h-5 text-gray-400 cursor-pointer hover:text-gray-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg
            v-else
            class="absolute right-3 top-3 w-5 h-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
        {{ error }}
      </div>

      <!-- Categories -->
      <div v-if="filteredCategories.length > 0" class="space-y-4">
        <div v-for="category in filteredCategories" :key="category.id" class="bg-white rounded-lg shadow-sm overflow-hidden">
          <!-- Category Header (collapsible) -->
          <button
            @click="toggleCategory(category.id)"
            class="w-full px-6 py-4 flex justify-between items-center hover:bg-gray-50 transition border-b border-gray-100"
          >
            <div class="flex items-center gap-3 text-left">
              <h2 class="text-lg font-semibold text-gray-900">
                📂 {{ category.name }}
              </h2>
              <span class="text-sm font-medium text-gray-600 bg-gray-100 px-3 py-1 rounded">
                {{ category.products.length }}
              </span>
            </div>
            <svg
              :class="expandedCategories.has(category.id) ? 'rotate-180' : ''"
              class="w-5 h-5 text-gray-500 transition-transform duration-200"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
            </svg>
          </button>

          <!-- Products (collapsible) -->
          <div
            v-if="expandedCategories.has(category.id)"
            class="divide-y divide-gray-100"
          >
            <div
              v-for="ps in category.products"
              :key="ps.product.id"
              class="p-4 flex flex-col gap-4 hover:bg-gray-50 transition"
              :class="{'bg-red-50': ps.status === 'EMERGENCY', 'bg-amber-50': ps.status === 'REQUIRED'}"
            >
              <!-- Product Info -->
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h3 class="text-base font-semibold text-gray-900">{{ ps.product.name }}</h3>
                  <p class="text-sm text-gray-600 mt-1">
                    Current Status:
                    <span
                      class="font-bold ml-2 px-2 py-1 rounded text-xs"
                      :class="{
                        'bg-green-100 text-green-800': ps.status === 'ENOUGH',
                        'bg-amber-100 text-amber-800': ps.status === 'REQUIRED',
                        'bg-red-100 text-red-800': ps.status === 'EMERGENCY'
                      }"
                    >
                      {{ ps.status }}
                    </span>
                  </p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-2 flex-wrap">
                <button
                  @click="setState(ps.product.id, 'enough')"
                  class="px-4 py-2 rounded text-sm font-medium transition"
                  :class="ps.status === 'ENOUGH' ? 'bg-green-600 text-white' : 'bg-green-100 text-green-700 hover:bg-green-200'"
                >
                  ✓ Enough Stock
                </button>
                <button
                  @click="setState(ps.product.id, 'required')"
                  class="px-4 py-2 rounded text-sm font-medium transition"
                  :class="ps.status === 'REQUIRED' ? 'bg-amber-600 text-white' : 'bg-amber-100 text-amber-700 hover:bg-amber-200'"
                >
                  ! Required
                </button>
                <button
                  @click="setState(ps.product.id, 'emergency')"
                  class="px-4 py-2 rounded text-sm font-medium transition"
                  :class="ps.status === 'EMERGENCY' ? 'bg-red-600 text-white' : 'bg-red-100 text-red-700 hover:bg-red-200'"
                >
                  ⚠ Emergency
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="productStates.length === 0 && !loading" class="text-center py-12 bg-white rounded-lg shadow-sm">
        <p class="text-lg text-gray-600">No products found</p>
        <p class="text-sm text-gray-500 mt-2">Add products in the admin panel to get started</p>
      </div>

      <!-- No Search Results -->
      <div v-else class="text-center py-12 bg-white rounded-lg shadow-sm">
        <p class="text-lg text-gray-600">No products match your search</p>
        <p class="text-sm text-gray-500 mt-2">Try different keywords</p>
      </div>
    </div>
  </BarLayout>
</template>

