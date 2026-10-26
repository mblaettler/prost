<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { useI18n } from 'vue-i18n';
import AdminLayout from '../../components/AdminLayout.vue';

const { t } = useI18n();
</script>

<template>
  <AdminLayout>
    <template #title>{{ t('common.dashboard') }}</template>

    <div>
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ t('admin.home.welcome') }}</h2>
        <p class="text-gray-600">{{ t('admin.home.intro') }}</p>
      </div>

      <!-- Quick Access Cards -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <RouterLink
          to="/admin/categories"
          class="block p-6 bg-gradient-to-br from-amber-50 to-amber-100 hover:from-amber-100 hover:to-amber-200 rounded-lg border border-amber-200 transition-all transform hover:scale-105 cursor-pointer"
        >
          <div class="text-3xl mb-2">📂</div>
          <h3 class="text-xl font-semibold text-amber-900">{{ t('admin.categories') }}</h3>
          <p class="mt-2 text-amber-800">{{ t('admin.home.categoriesDescription') }}</p>
        </RouterLink>

        <RouterLink
          to="/admin/products"
          class="block p-6 bg-gradient-to-br from-orange-50 to-orange-100 hover:from-orange-100 hover:to-orange-200 rounded-lg border border-orange-200 transition-all transform hover:scale-105 cursor-pointer"
        >
          <div class="text-3xl mb-2">📦</div>
          <h3 class="text-xl font-semibold text-orange-900">{{ t('admin.products') }}</h3>
          <p class="mt-2 text-orange-800">{{ t('admin.home.productsDescription') }}</p>
        </RouterLink>

        <RouterLink
          to="/admin/users"
          class="block p-6 bg-gradient-to-br from-yellow-50 to-yellow-100 hover:from-yellow-100 hover:to-yellow-200 rounded-lg border border-yellow-200 transition-all transform hover:scale-105 cursor-pointer"
        >
          <div class="text-3xl mb-2">👥</div>
          <h3 class="text-xl font-semibold text-yellow-900">{{ t('admin.users') }}</h3>
          <p class="mt-2 text-yellow-800">{{ t('admin.home.usersDescription') }}</p>
        </RouterLink>
      </div>

      <!-- Info Section -->
      <div class="mt-12 bg-white rounded-lg shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">{{ t('admin.home.systemInformation') }}</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="border-l-4 border-amber-500 pl-4">
            <p class="text-sm text-gray-600">{{ t('admin.home.currentRole') }}</p>
            <p class="text-lg font-semibold text-gray-900">{{ t('admin.home.administrator') }}</p>
          </div>
          <div class="border-l-4 border-blue-500 pl-4">
            <p class="text-sm text-gray-600">{{ t('admin.home.systemStatus') }}</p>
            <p class="text-lg font-semibold text-green-600">{{ t('admin.home.operational') }}</p>
          </div>
          <div class="border-l-4 border-purple-500 pl-4">
            <p class="text-sm text-gray-600">{{ t('admin.home.lastUpdated') }}</p>
            <p class="text-lg font-semibold text-gray-900">{{ t('admin.home.justNow') }}</p>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

