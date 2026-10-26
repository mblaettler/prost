<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { api } from '../../api';
import AdminLayout from '../../components/AdminLayout.vue';

const { t } = useI18n();
const categories = ref<any[]>([]);
const newName = ref('');
const error = ref('');

const fetchCategories = async () => {
  try {
    const c = await api.categories.list();
    categories.value = c.sort((a: { name: string }, b: { name: string }) => a.name.localeCompare(b.name));
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
  <AdminLayout>
    <template #title>{{ t('admin.categoriesView.title') }}</template>
    
    <div class="max-w-4xl">
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Add New Category -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">{{ t('admin.categoriesView.addNew') }}</h3>
        <div class="flex gap-3">
          <input
            v-model="newName"
            class="flex-1 border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            :placeholder="t('admin.categoriesView.namePlaceholder')"
          />
          <button
            @click="addCategory"
            class="bg-amber-600 text-white px-6 py-3 rounded-lg hover:bg-amber-700 transition-colors font-medium"
          >
            {{ t('admin.categoriesView.add') }}
          </button>
        </div>
      </div>

      <!-- Categories List -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div v-if="categories.length === 0" class="p-8 text-center text-gray-500">
          <p class="text-lg">{{ t('admin.categoriesView.empty') }}</p>
        </div>
        <ul v-else class="divide-y">
          <li v-for="cat in categories" :key="cat.id" class="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
            <span class="font-semibold text-gray-900">{{ cat.name }}</span>
            <button
              @click="deleteCategory(cat.id)"
              class="text-red-500 hover:text-red-700 hover:bg-red-50 px-3 py-2 rounded transition-colors"
            >
              {{ t('common.delete') }}
            </button>
          </li>
        </ul>
      </div>
    </div>
  </AdminLayout>
</template>

