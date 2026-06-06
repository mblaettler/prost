<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../../api';
import AdminLayout from '../../components/AdminLayout.vue';

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
    selectedCategory.value = '';
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
  <AdminLayout>
    <template #title>Products</template>

    <div class="max-w-4xl">
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Add New Product -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Add New Product</h3>
        <div class="flex gap-3">
          <input
            v-model="newName"
            class="flex-1 border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            placeholder="Product name"
          />
          <select
            v-model="selectedCategory"
            class="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="" disabled>Select Category</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
          <button
            @click="addProduct"
            class="bg-amber-600 text-white px-6 py-3 rounded-lg hover:bg-amber-700 transition-colors font-medium"
          >
            Add Product
          </button>
        </div>
      </div>

      <!-- Products List -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div v-if="products.length === 0" class="p-8 text-center text-gray-500">
          <p class="text-lg">No products yet. Create one to get started!</p>
        </div>
        <ul v-else class="divide-y">
          <li v-for="p in products" :key="p.id" class="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
            <div>
              <span class="font-semibold text-gray-900">{{ p.name }}</span>
              <span class="ml-3 text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded">
                {{ categories.find(c => c.id === p.category_id)?.name || 'Unknown' }}
              </span>
            </div>
            <button
              @click="deleteProduct(p.id)"
              class="text-red-500 hover:text-red-700 hover:bg-red-50 px-3 py-2 rounded transition-colors"
            >
              Delete
            </button>
          </li>
        </ul>
      </div>
    </div>
  </AdminLayout>
</template>

