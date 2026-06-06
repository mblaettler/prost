<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="px-4 py-5 sm:p-6">
      <h2 class="text-3xl font-bold text-gray-900 mb-4">🍺 Welcome to Prost Admin</h2>
      <p class="text-lg text-gray-600 mb-8">
        Use this interface to configure product categories, products, and users.
      </p>
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <RouterLink to="/admin/categories" class="block p-6 bg-amber-50 hover:bg-amber-100 rounded-lg border border-amber-200">
          <h3 class="text-xl font-semibold text-amber-800">Manage Categories</h3>
          <p class="mt-2 text-amber-700">Add or remove product categories.</p>
        </RouterLink>
        <RouterLink to="/admin/products" class="block p-6 bg-orange-50 hover:bg-orange-100 rounded-lg border border-orange-200">
          <h3 class="text-xl font-semibold text-orange-800">Manage Products</h3>
          <p class="mt-2 text-orange-700">Define products and assign them to categories.</p>
        </RouterLink>
        <RouterLink to="/admin/users" class="block p-6 bg-yellow-50 hover:bg-yellow-100 rounded-lg border border-yellow-200">
          <h3 class="text-xl font-semibold text-yellow-800">Manage Orderers</h3>
          <p class="mt-2 text-yellow-700">Register and manage users.</p>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
