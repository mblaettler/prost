<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { api } from '../api';
import type { ProductState } from '../types';

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
  <div class="min-h-screen bg-gray-50 p-4 sm:p-6 max-w-4xl mx-auto">
    <!-- Header -->
    <div class="sticky top-0 bg-gray-50 z-10 mb-6 pt-2 pb-4 border-b border-gray-200">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-3xl font-bold text-gray-900">🍺 Bar Management</h1>
        <button
          @click="fetchData"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm transition"
          :disabled="loading"
        >
          {{ loading ? 'Refreshing...' : 'Refresh' }}
        </button>
      </div>

      <!-- Search Bar (optimized for mobile) -->
      <div class="relative">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search products or categories..."
          class="w-full px-4 py-3 pr-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
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
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Categories -->
    <div v-if="filteredCategories.length > 0" class="space-y-3">
      <div v-for="category in filteredCategories" :key="category.id" class="bg-white rounded-lg shadow-sm overflow-hidden">
        <!-- Category Header (collapsible) -->
        <button
          @click="toggleCategory(category.id)"
          class="w-full px-4 py-4 flex justify-between items-center hover:bg-gray-50 transition border-b border-gray-100"
        >
          <div class="flex items-center gap-3 text-left">
            <h2 class="text-lg font-semibold text-gray-800">
              {{ category.name }}
            </h2>
            <span class="text-sm font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded">
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
            class="p-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 hover:bg-gray-50 transition"
            :class="{'bg-red-50': ps.status === 'EMERGENCY', 'bg-amber-50': ps.status === 'REQUIRED'}"
          >
            <!-- Product Info -->
            <div class="flex-1 min-w-0">
              <h3 class="text-base font-semibold text-gray-800 break-words">{{ ps.product.name }}</h3>
              <p class="text-sm text-gray-500 mt-1">
                Status:
                <span
                  class="font-bold inline-block ml-1"
                  :class="{
                    'text-green-600': ps.status === 'ENOUGH',
                    'text-amber-600': ps.status === 'REQUIRED',
                    'text-red-600': ps.status === 'EMERGENCY'
                  }"
                >
                  {{ ps.status }}
                </span>
              </p>
            </div>

            <!-- Action Buttons (mobile-friendly layout) -->
            <div class="w-full sm:w-auto flex gap-2 flex-wrap sm:flex-nowrap">
              <button
                @click="setState(ps.product.id, 'enough')"
                class="flex-1 sm:flex-none px-3 py-2 rounded text-xs sm:text-sm font-medium transition"
                :class="ps.status === 'ENOUGH' ? 'bg-green-600 text-white' : 'bg-green-100 text-green-700 hover:bg-green-200'"
                title="Mark as enough stock"
              >
                Enough
              </button>
              <button
                @click="setState(ps.product.id, 'required')"
                class="flex-1 sm:flex-none px-3 py-2 rounded text-xs sm:text-sm font-medium transition"
                :class="ps.status === 'REQUIRED' ? 'bg-amber-600 text-white' : 'bg-amber-100 text-amber-700 hover:bg-amber-200'"
                title="Mark as required"
              >
                Required
              </button>
              <button
                @click="setState(ps.product.id, 'emergency')"
                class="flex-1 sm:flex-none px-3 py-2 rounded text-xs sm:text-sm font-medium transition"
                :class="ps.status === 'EMERGENCY' ? 'bg-red-600 text-white' : 'bg-red-100 text-red-700 hover:bg-red-200'"
                title="Mark as emergency"
              >
                Emergency
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="productStates.length === 0 && !loading" class="text-center py-12 text-gray-500">
      No products found. Add some in the admin panel!
    </div>

    <!-- No Search Results -->
    <div v-else class="text-center py-12 text-gray-500">
      No products match your search. Try different keywords!
    </div>
  </div>
</template>
