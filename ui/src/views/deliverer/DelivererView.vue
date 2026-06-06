<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { api } from '../../api';
import type { ProductState } from '../../types';

const notEnoughProducts = ref<ProductState[]>([]);
const error = ref('');
const loading = ref(false);

const statusPriority: Record<string, number> = {
  'EMERGENCY': 0,
  'REQUIRED': 1,
  'ENOUGH': 2,
};

const sortedProducts = computed(() => {
  return [...notEnoughProducts.value].sort((a, b) => {
    // First sort by status (EMERGENCY > REQUIRED)
    const statusDiff = (statusPriority[a.status] ?? 999) - (statusPriority[b.status] ?? 999);
    if (statusDiff !== 0) return statusDiff;

    // Then sort by bar name
    return a.bar.name.localeCompare(b.bar.name);
  });
});

const groupedByBar = computed(() => {
  const grouped: Record<string, ProductState[]> = {};
  const barOrder: string[] = [];
  
  sortedProducts.value.forEach((product) => {
    const barId = product.bar.id;
    if (!grouped[barId]) {
      grouped[barId] = [];
      barOrder.push(barId);
    }
    grouped[barId].push(product);
  });
  
  // Sort products within each bar by status (EMERGENCY first)
  Object.keys(grouped).forEach((barId) => {
    grouped[barId].sort((a, b) => {
      return (statusPriority[a.status] ?? 999) - (statusPriority[b.status] ?? 999);
    });
  });
  
  return { bars: grouped, order: barOrder };
});

const fetchNotEnoughProducts = async () => {
  loading.value = true;
  error.value = '';
  try {
    notEnoughProducts.value = await api.deliverer.getNotEnoughProducts();
  } catch (err: any) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const markAsEnough = async (barId: string, productId: string) => {
  try {
    notEnoughProducts.value = await api.deliverer.markProductEnough(barId, productId);
  } catch (err: any) {
    error.value = err.message;
  }
};

const getStatusColor = (status: string): string => {
  switch (status) {
    case 'EMERGENCY':
      return 'bg-red-100 border-red-300 text-red-900';
    case 'REQUIRED':
      return 'bg-yellow-100 border-yellow-300 text-yellow-900';
    default:
      return 'bg-gray-100 border-gray-300 text-gray-900';
  }
};

const getStatusBadgeColor = (status: string): string => {
  switch (status) {
    case 'EMERGENCY':
      return 'bg-red-600 text-white';
    case 'REQUIRED':
      return 'bg-yellow-600 text-white';
    default:
      return 'bg-gray-600 text-white';
  }
};

onMounted(fetchNotEnoughProducts);
</script>

<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold">Missing Products</h1>
      <button
        @click="fetchNotEnoughProducts"
        :disabled="loading"
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div v-if="notEnoughProducts.length === 0 && !loading" class="text-center py-8 text-gray-500">
      <p>All products are sufficiently stocked!</p>
    </div>

    <div v-else class="space-y-6">
      <!-- Bar Cards -->
      <div
        v-for="barId in groupedByBar.order"
        :key="barId"
        class="border border-gray-300 rounded-lg p-6 bg-white shadow-md"
      >
        <!-- Bar Header -->
        <div class="flex items-center justify-between mb-4 pb-4 border-b border-gray-200">
          <h2 class="text-2xl font-bold text-gray-800">{{ groupedByBar.bars[barId][0].bar.name }}</h2>
          <span class="bg-gray-600 text-white px-3 py-1 rounded text-sm font-medium">
            {{ groupedByBar.bars[barId].length }} item(s)
          </span>
        </div>

        <!-- Emergency Products -->
        <div v-if="groupedByBar.bars[barId].some(p => p.status === 'EMERGENCY')" class="mb-6">
          <h3 class="text-lg font-semibold text-red-700 mb-3 flex items-center gap-2">
            <span class="inline-block w-3 h-3 bg-red-600 rounded-full"></span>
            Emergency
          </h3>
          <div class="space-y-3 pl-5">
            <div
              v-for="item in groupedByBar.bars[barId].filter(p => p.status === 'EMERGENCY')"
              :key="`${item.bar.id}-${item.product.id}`"
              class="border-l-4 border-red-500 bg-red-50 p-4 rounded flex justify-between items-center"
            >
              <div class="flex-1">
                <div class="font-semibold text-lg">{{ item.product.name }}</div>
                <div class="text-xs text-gray-600 mt-1">
                  Category: {{ item.product.category?.name || 'Unknown' }}
                </div>
              </div>
              <button
                @click="markAsEnough(item.bar.id, item.product.id)"
                class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 ml-4 whitespace-nowrap"
              >
                Mark as Enough
              </button>
            </div>
          </div>
        </div>

        <!-- Required Products -->
        <div v-if="groupedByBar.bars[barId].some(p => p.status === 'REQUIRED')" class="mb-6">
          <h3 class="text-lg font-semibold text-yellow-700 mb-3 flex items-center gap-2">
            <span class="inline-block w-3 h-3 bg-yellow-600 rounded-full"></span>
            Required
          </h3>
          <div class="space-y-3 pl-5">
            <div
              v-for="item in groupedByBar.bars[barId].filter(p => p.status === 'REQUIRED')"
              :key="`${item.bar.id}-${item.product.id}`"
              class="border-l-4 border-yellow-500 bg-yellow-50 p-4 rounded flex justify-between items-center"
            >
              <div class="flex-1">
                <div class="font-semibold text-lg">{{ item.product.name }}</div>
                <div class="text-xs text-gray-600 mt-1">
                  Category: {{ item.product.category?.name || 'Unknown' }}
                </div>
              </div>
              <button
                @click="markAsEnough(item.bar.id, item.product.id)"
                class="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 ml-4 whitespace-nowrap"
              >
                Mark as Enough
              </button>
            </div>
          </div>
        </div>

        <!-- Enough Products -->
        <div v-if="groupedByBar.bars[barId].some(p => p.status === 'ENOUGH')" class="mb-6">
          <h3 class="text-lg font-semibold text-green-700 mb-3 flex items-center gap-2">
            <span class="inline-block w-3 h-3 bg-green-600 rounded-full"></span>
            Sufficient
          </h3>
          <div class="space-y-3 pl-5">
            <div
              v-for="item in groupedByBar.bars[barId].filter(p => p.status === 'ENOUGH')"
              :key="`${item.bar.id}-${item.product.id}`"
              class="border-l-4 border-green-500 bg-green-50 p-4 rounded flex justify-between items-center"
            >
              <div class="flex-1">
                <div class="font-semibold text-lg">{{ item.product.name }}</div>
                <div class="text-xs text-gray-600 mt-1">
                  Category: {{ item.product.category?.name || 'Unknown' }}
                </div>
              </div>
              <button
                @click="markAsEnough(item.bar.id, item.product.id)"
                class="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 ml-4 whitespace-nowrap"
                disabled
              >
                Sufficient
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
