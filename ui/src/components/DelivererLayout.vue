<script setup lang="ts">
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from '../api';

const route = useRoute();
const router = useRouter();
const isSidebarOpen = ref(false);

const menuItems = [
  { name: 'Dashboard', path: '/deliverer', icon: '🏠' },
];

const isActive = (path: string) => {
  return route.path === path;
};

const logout = () => {
  api.clearCredentials();
  router.push('/login');
};

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};

const closeSidebar = () => {
  isSidebarOpen.value = false;
};


</script>

<template>
  <div class="min-h-screen flex flex-row bg-gray-100">
    <!-- Sidebar Overlay (Mobile) -->
    <div
      v-if="isSidebarOpen"
      @click="closeSidebar"
      class="md:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
    />

    <!-- Sidebar -->
    <div
      :class="[
        'bg-white shadow-lg transition-all duration-300 flex flex-col',
        isSidebarOpen ? 'w-64 fixed left-0 top-16 bottom-0 z-40 md:static md:top-auto' : 'w-0 md:w-64 overflow-hidden',
      ]"
    >
      <div class="p-6">
        <h1 class="text-2xl font-bold text-amber-700">🍺 Prost</h1>
        <p class="text-sm text-gray-600 mt-1">Deliverer Panel</p>
      </div>

      <!-- Menu -->
      <nav class="mt-6 flex-1">
        <div v-for="item in menuItems" :key="item.path" class="mb-2">
          <router-link
            :to="item.path"
            @click="closeSidebar"
            :class="[
              'flex items-center px-6 py-3 text-gray-700 hover:bg-amber-50 hover:text-amber-700 transition-colors whitespace-nowrap',
              isActive(item.path) ? 'bg-amber-100 text-amber-700 border-r-4 border-amber-700' : ''
            ]"
          >
            <span class="text-xl mr-3">{{ item.icon }}</span>
            <span class="font-medium">{{ item.name }}</span>
          </router-link>
        </div>
      </nav>

      <!-- Logout Button -->
      <div class="p-6 border-t mt-auto">
        <button
          @click="logout"
          class="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium text-sm"
        >
          Logout
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-w-0 w-full">
      <!-- Top Bar -->
      <div class="bg-white shadow-sm border-b sticky top-0 z-20">
        <div class="px-4 md:px-8 py-4 flex items-center justify-between gap-4">
          <!-- Left Side: Menu Button + Title -->
          <div class="flex items-center gap-4 min-w-0 flex-1">
            <!-- Hamburger Menu Button (Mobile Only) -->
            <button
              @click="toggleSidebar"
              class="md:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors flex-shrink-0"
              title="Toggle menu"
            >
              <svg
                class="w-6 h-6 text-gray-700"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <!-- Title -->
            <h2 class="text-lg font-semibold text-gray-900 truncate">
              <slot name="title">Deliverer Dashboard</slot>
            </h2>
          </div>

          <!-- Right Side: Action Buttons -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <slot name="top-actions" />
          </div>
        </div>
      </div>

      <!-- Content Area -->
      <main class="flex-1 overflow-auto p-4 md:p-8">
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
