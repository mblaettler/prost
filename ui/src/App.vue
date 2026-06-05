<script setup lang="ts">
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router'
import { api } from './api'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()

const isAuthenticated = computed(() => api.isAuthenticated())
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
const isLoginRoute = computed(() => route.name === 'login')

const logout = () => {
  api.clearCredentials()
  router.push('/admin/login')
}
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <nav v-if="isAdminRoute && !isLoginRoute" class="bg-white shadow-md">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center font-bold text-xl text-amber-700">
              🍺 Prost Config
            </div>
            <div class="hidden sm:-my-px sm:ml-6 sm:flex sm:space-x-8">
              <RouterLink to="/admin" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" exact-active-class="!border-amber-500 !text-gray-900">
                Home
              </RouterLink>
              <RouterLink to="/admin/categories" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" active-class="!border-amber-500 !text-gray-900">
                Categories
              </RouterLink>
              <RouterLink to="/admin/products" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" active-class="!border-amber-500 !text-gray-900">
                Products
              </RouterLink>
              <RouterLink to="/admin/users" class="border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium" active-class="!border-amber-500 !text-gray-900">
                Users
              </RouterLink>
            </div>
          </div>
          <div class="flex items-center">
            <RouterLink to="/" class="text-gray-500 hover:text-gray-700 px-3 py-2 text-sm font-medium">
              Back to Home
            </RouterLink>
            <button @click="logout" class="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <RouterView />
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  background-color: #f3f4f6;
}
</style>
