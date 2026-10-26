<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import { api } from '../../api';
import BarLayout from '../../components/BarLayout.vue';
import type { ProductState, ProductStatus } from '../../types';

const { t } = useI18n();
const productStates = ref<ProductState[]>([]);
const error = ref('');
const loading = ref(false);
const manualRefreshing = ref(false);
const searchQuery = ref('');
const expandedCategories = ref<Set<string>>(new Set());
const refreshInterval = ref<number | null>(null);
const REFRESH_INTERVAL = 1000;

// Must match BAR_TRANSITIONS in backend/models/order/ProductState.py
const allowedTransitions: Record<ProductStatus, ProductStatus[]> = {
  ENOUGH: ['REQUIRED', 'EMERGENCY'],
  REQUIRED: ['EMERGENCY', 'ENOUGH'],
  EMERGENCY: ['ENOUGH'],
  IN_PROGRESS: [],
};

const canSetState = (current: ProductStatus, target: ProductStatus) => allowedTransitions[current].includes(target);

const groupByCategory = (productStates: ProductState[]) => {
  const categoryMap = new Map<string, { name: string; products: ProductState[] }>();
  productStates.forEach((ps) => {
    const categoryId = ps.product.category_id;
    const categoryName = ps.product.category?.name || t('bar.uncategorized');
    if (!categoryMap.has(categoryId)) {
      categoryMap.set(categoryId, { name: categoryName, products: [] });
    }
    categoryMap.get(categoryId)?.products.push(ps);
  });
  return Array.from(categoryMap.entries())
    .map(([id, { name, products }]) => ({ id, name, products }))
    .sort((a, b) => a.name.localeCompare(b.name));
};

// Sorted once here so every derived list (categories, favourites, ordered) is alphabetical
const sortedProductStates = computed(() =>
  [...productStates.value].sort((a, b) => a.product.name.localeCompare(b.product.name))
);

const filteredCategories = computed(() => {
  const categories = groupByCategory(sortedProductStates.value);
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

const favourites = computed(() => sortedProductStates.value.filter((ps) => ps.product.favourite));

// Favourites are excluded: they already show their status in the favourites grid
const ordered = computed(() =>
  sortedProductStates.value.filter((ps) => ps.status !== 'ENOUGH' && !ps.product.favourite)
);

const quickAccessSections = computed(() =>
  [
    { id: 'favourites', title: t('bar.favourites'), products: favourites.value },
    { id: 'ordered', title: t('bar.ordered'), products: ordered.value },
  ].filter((section) => section.products.length > 0)
);

const productAnchor = (productId: string) => `product-${productId}`;

const highlightedProduct = ref<string | null>(null);

const scrollToProduct = async (ps: ProductState) => {
  // Make sure the target row is rendered: not hidden by the search or a collapsed category
  const visible = filteredCategories.value.some((category) =>
    category.products.some((p) => p.product.id === ps.product.id)
  );
  if (!visible) searchQuery.value = '';
  expandedCategories.value.add(ps.product.category_id);
  await nextTick();
  document.getElementById(productAnchor(ps.product.id))?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  highlightedProduct.value = ps.product.id;
  window.setTimeout(() => {
    if (highlightedProduct.value === ps.product.id) highlightedProduct.value = null;
  }, 1500);
};

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

const manualRefresh = async () => {
  manualRefreshing.value = true;
  await fetchData();
  manualRefreshing.value = false;
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

onMounted(() => {
  fetchData();
  refreshInterval.value = window.setInterval(fetchData, REFRESH_INTERVAL);
});

onUnmounted(() => {
  if (refreshInterval.value !== null) {
    clearInterval(refreshInterval.value);
  }
});
</script>

<template>
  <BarLayout>
    <template #title>{{ t('bar.title') }}</template>

    <template #top-actions>
      <button
        @click="manualRefresh"
        class="bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors font-medium text-sm whitespace-nowrap"
        :disabled="manualRefreshing"
      >
        {{ manualRefreshing ? t('common.refreshing') : t('common.refresh') }}
      </button>
    </template>

    <div class="max-w-6xl">
      <!-- Favourites and ordered products -->
      <div v-for="section in quickAccessSections" :key="section.id" class="mb-6">
        <h2 class="text-sm font-semibold text-gray-600 uppercase tracking-wide mb-3">{{ section.title }}</h2>
        <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-3">
          <a
            v-for="ps in section.products"
            :key="ps.product.id"
            :href="`#${productAnchor(ps.product.id)}`"
            @click.prevent="scrollToProduct(ps)"
            class="aspect-square rounded-lg shadow-sm border-2 p-2 flex flex-col items-center justify-center text-center transition hover:shadow-md hover:-translate-y-0.5"
            :class="{
              'bg-white border-green-300': ps.status === 'ENOUGH',
              'bg-amber-50 border-amber-400': ps.status === 'REQUIRED',
              'bg-red-50 border-red-500': ps.status === 'EMERGENCY',
              'bg-blue-50 border-blue-400': ps.status === 'IN_PROGRESS'
            }"
          >
            <span class="text-sm font-semibold text-gray-900 break-words line-clamp-3">{{ ps.product.name }}</span>
            <span
              class="mt-2 px-1.5 py-0.5 rounded text-[10px] font-bold"
              :class="{
                'bg-green-100 text-green-800': ps.status === 'ENOUGH',
                'bg-amber-100 text-amber-800': ps.status === 'REQUIRED',
                'bg-red-100 text-red-800': ps.status === 'EMERGENCY',
                'bg-blue-100 text-blue-800': ps.status === 'IN_PROGRESS'
              }"
            >
              {{ t(`status.${ps.status}`) }}
            </span>
          </a>
        </div>
      </div>

      <!-- Search Bar -->
      <div class="mb-6">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="t('bar.searchPlaceholder')"
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
              :id="productAnchor(ps.product.id)"
              class="p-4 flex flex-col gap-4 hover:bg-gray-50 transition scroll-mt-24"
              :class="{'ring-2 ring-inset ring-amber-500': highlightedProduct === ps.product.id, 'bg-red-50': ps.status === 'EMERGENCY', 'bg-amber-50': ps.status === 'REQUIRED', 'bg-blue-50': ps.status === 'IN_PROGRESS'}"
            >
              <!-- Product Info -->
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <h3 class="text-base font-semibold text-gray-900">
                    <span v-if="ps.product.favourite" class="text-amber-500" :title="t('bar.favourite')">★</span>
                    {{ ps.product.name }}
                  </h3>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ t('bar.currentStatus') }}
                    <span
                      class="font-bold ml-2 px-2 py-1 rounded text-xs"
                      :class="{
                        'bg-green-100 text-green-800': ps.status === 'ENOUGH',
                        'bg-amber-100 text-amber-800': ps.status === 'REQUIRED',
                        'bg-red-100 text-red-800': ps.status === 'EMERGENCY',
                        'bg-blue-100 text-blue-800': ps.status === 'IN_PROGRESS'
                      }"
                    >
                      {{ t(`status.${ps.status}`) }}
                    </span>
                  </p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-2 flex-wrap">
                <button
                  @click="setState(ps.product.id, 'enough')"
                  :disabled="!canSetState(ps.status, 'ENOUGH')"
                  class="px-4 py-2 rounded text-sm font-medium transition"
                  :class="ps.status === 'ENOUGH' ? 'bg-green-600 text-white cursor-default' : canSetState(ps.status, 'ENOUGH') ? 'bg-green-100 text-green-700 hover:bg-green-200' : 'bg-green-100 text-green-700 opacity-50 cursor-not-allowed'"
                >
                  {{ t('bar.setEnough') }}
                </button>
                <button
                  @click="setState(ps.product.id, 'required')"
                  :disabled="!canSetState(ps.status, 'REQUIRED')"
                  class="px-4 py-2 rounded text-sm font-medium transition"
                  :class="ps.status === 'REQUIRED' ? 'bg-amber-600 text-white cursor-default' : canSetState(ps.status, 'REQUIRED') ? 'bg-amber-100 text-amber-700 hover:bg-amber-200' : 'bg-amber-100 text-amber-700 opacity-50 cursor-not-allowed'"
                >
                  {{ t('bar.setRequired') }}
                </button>
                <button
                  @click="setState(ps.product.id, 'emergency')"
                  :disabled="!canSetState(ps.status, 'EMERGENCY')"
                  class="px-4 py-2 rounded text-sm font-medium transition"
                  :class="ps.status === 'EMERGENCY' ? 'bg-red-600 text-white cursor-default' : canSetState(ps.status, 'EMERGENCY') ? 'bg-red-100 text-red-700 hover:bg-red-200' : 'bg-red-100 text-red-700 opacity-50 cursor-not-allowed'"
                >
                  {{ t('bar.setEmergency') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="productStates.length === 0 && !loading" class="text-center py-12 bg-white rounded-lg shadow-sm">
        <p class="text-lg text-gray-600">{{ t('bar.noProducts') }}</p>
        <p class="text-sm text-gray-500 mt-2">{{ t('bar.noProductsHint') }}</p>
      </div>

      <!-- No Search Results -->
      <div v-else class="text-center py-12 bg-white rounded-lg shadow-sm">
        <p class="text-lg text-gray-600">{{ t('bar.noMatches') }}</p>
        <p class="text-sm text-gray-500 mt-2">{{ t('bar.noMatchesHint') }}</p>
      </div>
    </div>
  </BarLayout>
</template>

