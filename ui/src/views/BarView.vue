<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../api';

const productStates = ref<any[]>([]);
const error = ref('');
const loading = ref(false);

const fetchData = async () => {
  loading.value = true;
  try {
    productStates.value = await api.bar.listStates();
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
  <div class="p-6 max-w-4xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-bold text-gray-900">🍺 Bar Management</h1>
      <button
        @click="fetchData"
        class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md text-sm transition"
        :disabled="loading"
      >
        {{ loading ? 'Refreshing...' : 'Refresh' }}
      </button>
    </div>

    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div class="grid grid-cols-1 gap-4">
      <div v-for="ps in productStates" :key="ps.product.id"
           class="border rounded-lg p-4 flex flex-col sm:flex-row justify-between items-center bg-white shadow-sm transition-all"
           :class="{'border-red-500 bg-red-50': ps.status === 'EMERGENCY', 'border-amber-500 bg-amber-50': ps.status === 'REQUIRED'}">
        <div class="mb-4 sm:mb-0">
          <h3 class="text-xl font-semibold text-gray-800">{{ ps.product.name }}</h3>
          <p class="text-sm text-gray-500">Current Status:
            <span class="font-bold" :class="{
              'text-green-600': ps.status === 'ENOUGH',
              'text-amber-600': ps.status === 'REQUIRED',
              'text-red-600': ps.status === 'EMERGENCY'
            }">{{ ps.status }}</span>
          </p>
        </div>

        <div class="flex gap-2">
          <button
            @click="setState(ps.product.id, 'enough')"
            class="px-4 py-2 rounded text-sm font-medium transition"
            :class="ps.status === 'ENOUGH' ? 'bg-green-600 text-white' : 'bg-green-100 text-green-700 hover:bg-green-200'"
          >
            Enough
          </button>
          <button
            @click="setState(ps.product.id, 'required')"
            class="px-4 py-2 rounded text-sm font-medium transition"
            :class="ps.status === 'REQUIRED' ? 'bg-amber-600 text-white' : 'bg-amber-100 text-amber-700 hover:bg-amber-200'"
          >
            Required
          </button>
          <button
            @click="setState(ps.product.id, 'emergency')"
            class="px-4 py-2 rounded text-sm font-medium transition"
            :class="ps.status === 'EMERGENCY' ? 'bg-red-600 text-white' : 'bg-red-100 text-red-700 hover:bg-red-200'"
          >
            Emergency
          </button>
        </div>
      </div>
    </div>

    <div v-if="productStates.length === 0 && !loading" class="text-center py-12 text-gray-500">
      No products found. Add some in the admin panel!
    </div>
  </div>
</template>
