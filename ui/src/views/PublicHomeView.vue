<template>
  <div class="min-h-screen flex items-center justify-center bg-amber-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full text-center">
      <h1 class="text-4xl font-extrabold text-amber-700 mb-6">🍺 Prost</h1>
      <p class="text-xl text-gray-700 mb-8">
        Welcome to the Prost system. Please choose an option below.
      </p>
      <div class="space-y-4">
        <RouterLink to="/admin" class="block w-full py-3 px-4 border border-transparent text-lg font-medium rounded-md text-white bg-amber-600 hover:bg-amber-700">
          Admin Interface
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
