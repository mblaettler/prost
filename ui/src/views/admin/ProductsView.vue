<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../../api';

const products = ref<any[]>([]);
const categories = ref<any[]>([]);
const newName = ref('');
const selectedCategory = ref('');
const error = ref('');

const fetchData = async () => {
  try {
    const [p, c] = await Promise.all([api.products.list(), api.categories.list()]);
    products.value = p;
    categories.value = c;
  } catch (err: any) {
    error.value = err.message;
  }
};

const addProduct = async () => {
  if (!newName.value || !selectedCategory.value) return;
  try {
    await api.products.create({ name: newName.value, category_id: selectedCategory.value });
    newName.value = '';
    await fetchData();
  } catch (err: any) {
    error.value = err.message;
  }
};

const deleteProduct = async (id: string) => {
  try {
    await api.products.delete(id);
    await fetchData();
  } catch (err: any) {
    error.value = err.message;
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Products</h1>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div class="mb-6 flex gap-2">
      <input
        v-model="newName"
        class="border p-2 rounded w-full max-w-xs"
        placeholder="Product name"
      />
      <select v-model="selectedCategory" class="border p-2 rounded">
        <option value="" disabled>Select Category</option>
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
      </select>
      <button
        @click="addProduct"
        class="bg-amber-600 text-white px-4 py-2 rounded hover:bg-amber-700"
      >
        Add
      </button>
    </div>

    <ul class="space-y-2">
      <li v-for="p in products" :key="p.id" class="border p-4 rounded flex justify-between items-center bg-white shadow-sm">
        <div>
          <span class="font-semibold">{{ p.name }}</span>
          <span class="ml-2 text-sm text-gray-500">({{ categories.find(c => c.id === p.category_id)?.name || 'Unknown' }})</span>
        </div>
        <button
          @click="deleteProduct(p.id)"
          class="text-red-500 hover:text-red-700"
        >
          Delete
        </button>
      </li>
    </ul>
  </div>
</template>
