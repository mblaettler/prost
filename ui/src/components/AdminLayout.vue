<script setup lang="ts">
import { computed } from 'vue';
import { RouterLink, useRoute } from 'vue-router';
import { api } from '../api';
import { useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const menuItems = [
  { name: 'Dashboard', path: '/admin', icon: '🏠' },
  { name: 'Categories', path: '/admin/categories', icon: '📂' },
  { name: 'Products', path: '/admin/products', icon: '📦' },
  { name: 'Users', path: '/admin/users', icon: '👥' },
];

const isActive = (path: string) => {
  return route.path === path;
};

const logout = () => {
  api.clearCredentials();
  router.push('/login');
};
</script>

<template>
  <div class="min-h-screen flex bg-gray-100">
    <!-- Sidebar -->
    <div class="w-64 bg-white shadow-lg">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-amber-700">🍺 Prost</h1>
        <p class="text-sm text-gray-600 mt-1">Admin Panel</p>
      </div>

      <!-- Menu -->
      <nav class="mt-6">
        <div v-for="item in menuItems" :key="item.path" class="mb-2">
          <RouterLink
            :to="item.path"
            :class="[
              'flex items-center px-6 py-3 text-gray-700 hover:bg-amber-50 hover:text-amber-700 transition-colors',
              isActive(item.path) ? 'bg-amber-100 text-amber-700 border-r-4 border-amber-700' : ''
            ]"
          >
            <span class="text-xl mr-3">{{ item.icon }}</span>
            <span class="font-medium">{{ item.name }}</span>
          </RouterLink>
        </div>
      </nav>

      <!-- Logout Button -->
      <div class="absolute bottom-0 w-64 p-6 border-t">
        <button
          @click="logout"
          class="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium text-sm"
        >
          Logout
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col">
      <!-- Top Bar -->
      <div class="bg-white shadow-sm border-b">
        <div class="px-8 py-4">
          <h2 class="text-lg font-semibold text-gray-900">
            <slot name="title">Admin Dashboard</slot>
          </h2>
        </div>
      </div>

      <!-- Content Area -->
      <main class="flex-1 overflow-auto p-8">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transitions */
a {
  transition: all 0.2s ease;
}
</style>
