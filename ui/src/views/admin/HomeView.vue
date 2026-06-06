<script setup lang="ts">
import { RouterLink } from 'vue-router';
import AdminLayout from '../../components/AdminLayout.vue';
</script>

<template>
  <AdminLayout>
    <template #title>Dashboard</template>

    <div>
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-2">Welcome to Prost Admin</h2>
        <p class="text-gray-600">Use this interface to configure product categories, products, and users.</p>
      </div>

      <!-- Quick Access Cards -->
      <div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        <RouterLink
          to="/admin/categories"
          class="block p-6 bg-gradient-to-br from-amber-50 to-amber-100 hover:from-amber-100 hover:to-amber-200 rounded-lg border border-amber-200 transition-all transform hover:scale-105 cursor-pointer"
        >
          <div class="text-3xl mb-2">📂</div>
          <h3 class="text-xl font-semibold text-amber-900">Categories</h3>
          <p class="mt-2 text-amber-800">Manage product categories</p>
        </RouterLink>

        <RouterLink
          to="/admin/products"
          class="block p-6 bg-gradient-to-br from-orange-50 to-orange-100 hover:from-orange-100 hover:to-orange-200 rounded-lg border border-orange-200 transition-all transform hover:scale-105 cursor-pointer"
        >
          <div class="text-3xl mb-2">📦</div>
          <h3 class="text-xl font-semibold text-orange-900">Products</h3>
          <p class="mt-2 text-orange-800">Define and manage products</p>
        </RouterLink>

        <RouterLink
          to="/admin/users"
          class="block p-6 bg-gradient-to-br from-yellow-50 to-yellow-100 hover:from-yellow-100 hover:to-yellow-200 rounded-lg border border-yellow-200 transition-all transform hover:scale-105 cursor-pointer"
        >
          <div class="text-3xl mb-2">👥</div>
          <h3 class="text-xl font-semibold text-yellow-900">Users</h3>
          <p class="mt-2 text-yellow-800">Create and manage users</p>
        </RouterLink>
      </div>

      <!-- Info Section -->
      <div class="mt-12 bg-white rounded-lg shadow-sm p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">System Information</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="border-l-4 border-amber-500 pl-4">
            <p class="text-sm text-gray-600">Current Role</p>
            <p class="text-lg font-semibold text-gray-900">Administrator</p>
          </div>
          <div class="border-l-4 border-blue-500 pl-4">
            <p class="text-sm text-gray-600">System Status</p>
            <p class="text-lg font-semibold text-green-600">Operational</p>
          </div>
          <div class="border-l-4 border-purple-500 pl-4">
            <p class="text-sm text-gray-600">Last Updated</p>
            <p class="text-lg font-semibold text-gray-900">Just now</p>
          </div>
        </div>
      </div>
    </div>
  </AdminLayout>
</template>

