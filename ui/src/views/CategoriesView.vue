<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../api';

const categories = ref<any[]>([]);
const newName = ref('');
const error = ref('');

const fetchCategories = async () => {
  try {
    categories.value = await api.categories.list();
  } catch (err: any) {
    error.value = err.message;
  }
};

const addCategory = async () => {
  if (!newName.value) return;
  try {
    await api.categories.create(newName.value);
    newName.value = '';
    await fetchCategories();
  } catch (err: any) {
    error.value = err.message;
  }
};

const deleteCategory = async (id: string) => {
  try {
    await api.categories.delete(id);
    await fetchCategories();
  } catch (err: any) {
    error.value = err.message;
  }
};

onMounted(fetchCategories);
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">Product Categories</h1>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div class="mb-6 flex gap-2">
      <input
        v-model="newName"
        class="border p-2 rounded w-full max-w-xs"
        placeholder="Category name"
      />
      <button
        @click="addCategory"
        class="bg-amber-600 text-white px-4 py-2 rounded hover:bg-amber-700"
      >
        Add
      </button>
    </div>

    <ul class="space-y-2">
      <li v-for="cat in categories" :key="cat.id" class="border p-4 rounded flex justify-between items-center bg-white shadow-sm">
        <span class="font-semibold">{{ cat.name }}</span>
        <button
          @click="deleteCategory(cat.id)"
          class="text-red-500 hover:text-red-700"
        >
          Delete
        </button>
      </li>
    </ul>
  </div>
</template>
