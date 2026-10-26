<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { api } from '../../api';
import AdminLayout from '../../components/AdminLayout.vue';
import type { Product } from '../../types';

const { t } = useI18n();
const products = ref<any[]>([]);
const categories = ref<any[]>([]);
const newName = ref('');
const selectedCategory = ref('');
const newFavourite = ref(false);
const error = ref('');

const categoryName = (categoryId: string) => categories.value.find((c) => c.id === categoryId)?.name || t('common.unknown');

// Grouped by category, alphabetical within each category
const sortedProducts = computed(() =>
  [...products.value].sort(
    (a, b) =>
      categoryName(a.category_id).localeCompare(categoryName(b.category_id)) || a.name.localeCompare(b.name)
  )
);

const fetchData = async () => {
  try {
    const [p, c] = await Promise.all([api.products.list(), api.categories.list()]);
    products.value = p;
    categories.value = c.sort((a: { name: string }, b: { name: string }) => a.name.localeCompare(b.name));
  } catch (err: any) {
    error.value = err.message;
  }
};

const addProduct = async () => {
  if (!newName.value || !selectedCategory.value) return;
  try {
    await api.products.create({ name: newName.value, category_id: selectedCategory.value, favourite: newFavourite.value });
    newName.value = '';
    selectedCategory.value = '';
    newFavourite.value = false;
    await fetchData();
  } catch (err: any) {
    error.value = err.message;
  }
};

const toggleFavourite = async (p: Product) => {
  try {
    await api.products.update(p.id, { name: p.name, category_id: p.category_id, favourite: !p.favourite });
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
    <template #title>{{ t('admin.products') }}</template>

    <div class="max-w-4xl">
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Add New Product -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">{{ t('admin.productsView.addNew') }}</h3>
        <div class="flex gap-3">
          <input
            v-model="newName"
            class="flex-1 border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            :placeholder="t('admin.productsView.namePlaceholder')"
          />
          <select
            v-model="selectedCategory"
            class="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="" disabled>{{ t('admin.productsView.selectCategory') }}</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
          <button
            type="button"
            @click="newFavourite = !newFavourite"
            class="text-2xl px-2 transition-colors"
            :class="newFavourite ? 'text-amber-500 hover:text-amber-600' : 'text-gray-300 hover:text-amber-400'"
            :title="newFavourite ? t('admin.productsView.removeFavourite') : t('admin.productsView.markFavourite')"
          >
            {{ newFavourite ? '★' : '☆' }}
          </button>
          <button
            @click="addProduct"
            class="bg-amber-600 text-white px-6 py-3 rounded-lg hover:bg-amber-700 transition-colors font-medium"
          >
            {{ t('admin.productsView.add') }}
          </button>
        </div>
      </div>

      <!-- Products List -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div v-if="products.length === 0" class="p-8 text-center text-gray-500">
          <p class="text-lg">{{ t('admin.productsView.empty') }}</p>
        </div>
        <ul v-else class="divide-y">
          <li v-for="p in sortedProducts" :key="p.id" class="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
            <div class="flex items-center">
              <button
                @click="toggleFavourite(p)"
                class="text-xl mr-3 transition-colors"
                :class="p.favourite ? 'text-amber-500 hover:text-amber-600' : 'text-gray-300 hover:text-amber-400'"
                :title="p.favourite ? t('admin.productsView.removeFavourite') : t('admin.productsView.markFavourite')"
              >
                {{ p.favourite ? '★' : '☆' }}
              </button>
              <span class="font-semibold text-gray-900">{{ p.name }}</span>
              <span class="ml-3 text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded">
                {{ categoryName(p.category_id) }}
              </span>
            </div>
            <button
              @click="deleteProduct(p.id)"
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

