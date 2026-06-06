<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { api } from '../../api';
import DelivererLayout from '../../components/DelivererLayout.vue';
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
    const barProducts = grouped[barId];
    if (barProducts) {
      barProducts.sort((a, b) => {
        return (statusPriority[a.status] ?? 999) - (statusPriority[b.status] ?? 999);
      });
    }
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

onMounted(fetchNotEnoughProducts);
</script>

<template>
  <DelivererLayout>
    <template #title>Delivery Management</template>

    <template #top-actions>
      <button
        @click="fetchNotEnoughProducts"
        :disabled="loading"
        class="bg-amber-600 text-white px-4 py-2 rounded-lg hover:bg-amber-700 transition-colors font-medium text-sm whitespace-nowrap disabled:bg-gray-400"
      >
        {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
    </template>

    <div class="max-w-6xl">
      <!-- Error Message -->
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg mb-6">
        {{ error }}
      </div>

      <!-- No Products Message -->
      <div v-if="notEnoughProducts.length === 0 && !loading" class="text-center py-12 bg-white rounded-lg shadow-sm">
        <p class="text-2xl text-gray-600">✓ All set!</p>
        <p class="text-gray-500 mt-2">All products are sufficiently stocked in all bars</p>
      </div>

      <!-- Bar Cards -->
      <div v-else class="space-y-6">
        <div
          v-for="barId in groupedByBar.order"
          :key="barId"
          class="bg-white rounded-lg shadow-sm overflow-hidden"
        >
          <!-- Bar Header -->
          <div class="bg-gradient-to-r from-amber-50 to-amber-100 px-6 py-4 border-b border-amber-200">
            <div class="flex items-center justify-between">
              <h2 class="text-xl font-bold text-amber-900">
                🏪 {{ groupedByBar.bars[barId]![0]!.bar.name }}
              </h2>
              <span class="bg-amber-700 text-white px-3 py-1 rounded-full text-sm font-medium">
                {{ groupedByBar.bars[barId]!.length }} item{{ groupedByBar.bars[barId]!.length !== 1 ? 's' : '' }}
              </span>
            </div>
          </div>

          <!-- Products by Status -->
          <div class="divide-y">
            <!-- Emergency Products -->
            <div v-if="groupedByBar.bars[barId]!.some(p => p.status === 'EMERGENCY')" class="p-6">
              <h3 class="text-lg font-semibold text-red-700 mb-4 flex items-center gap-2">
                <span class="inline-block w-3 h-3 bg-red-600 rounded-full"></span>
                🚨 Emergency
              </h3>
              <div class="space-y-3">
                <div
                  v-for="item in groupedByBar.bars[barId]!.filter(p => p.status === 'EMERGENCY')"
                  :key="`${item.bar.id}-${item.product.id}`"
                  class="border-l-4 border-red-500 bg-red-50 p-4 rounded flex justify-between items-start gap-4 hover:bg-red-100 transition"
                >
                  <div class="flex-1">
                    <div class="font-semibold text-lg text-red-900">{{ item.product.name }}</div>
                    <div class="text-xs text-gray-600 mt-1">
                      📂 {{ item.product.category?.name || 'Unknown' }}
                    </div>
                  </div>
                  <button
                    @click="markAsEnough(item.bar.id, item.product.id)"
                    class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium text-sm whitespace-nowrap"
                  >
                    ✓ Mark as Enough
                  </button>
                </div>
              </div>
            </div>

            <!-- Required Products -->
            <div v-if="groupedByBar.bars[barId]!.some(p => p.status === 'REQUIRED')" class="p-6">
              <h3 class="text-lg font-semibold text-amber-700 mb-4 flex items-center gap-2">
                <span class="inline-block w-3 h-3 bg-amber-600 rounded-full"></span>
                ⚠ Required
              </h3>
              <div class="space-y-3">
                <div
                  v-for="item in groupedByBar.bars[barId]!.filter(p => p.status === 'REQUIRED')"
                  :key="`${item.bar.id}-${item.product.id}`"
                  class="border-l-4 border-amber-500 bg-amber-50 p-4 rounded flex justify-between items-start gap-4 hover:bg-amber-100 transition"
                >
                  <div class="flex-1">
                    <div class="font-semibold text-lg text-amber-900">{{ item.product.name }}</div>
                    <div class="text-xs text-gray-600 mt-1">
                      📂 {{ item.product.category?.name || 'Unknown' }}
                    </div>
                  </div>
                  <button
                    @click="markAsEnough(item.bar.id, item.product.id)"
                    class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors font-medium text-sm whitespace-nowrap"
                  >
                    ✓ Mark as Enough
                  </button>
                </div>
              </div>
            </div>

            <!-- Sufficient Products -->
            <div v-if="groupedByBar.bars[barId]!.some(p => p.status === 'ENOUGH')" class="p-6">
              <h3 class="text-lg font-semibold text-green-700 mb-4 flex items-center gap-2">
                <span class="inline-block w-3 h-3 bg-green-600 rounded-full"></span>
                ✓ Sufficient Stock
              </h3>
              <div class="space-y-3">
                <div
                  v-for="item in groupedByBar.bars[barId]!.filter(p => p.status === 'ENOUGH')"
                  :key="`${item.bar.id}-${item.product.id}`"
                  class="border-l-4 border-green-500 bg-green-50 p-4 rounded flex justify-between items-start gap-4"
                >
                  <div class="flex-1">
                    <div class="font-semibold text-lg text-green-900">{{ item.product.name }}</div>
                    <div class="text-xs text-gray-600 mt-1">
                      📂 {{ item.product.category?.name || 'Unknown' }}
                    </div>
                  </div>
                  <button
                    disabled
                    class="bg-gray-300 text-gray-600 px-4 py-2 rounded-lg font-medium text-sm whitespace-nowrap cursor-not-allowed"
                  >
                    ✓ Sufficient
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DelivererLayout>
</template>

