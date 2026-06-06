<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../../api';

const users = ref<any[]>([]);
const newName = ref('');
const newPassword = ref('');
const newRole = ref('');
const error = ref('');

const roles = [
  { id: 'admin', name: 'Admin' },
  { id: 'bar', name: 'Bar' },
  { id: 'deliverer', name: 'Deliverer' },
]

const fetchUsers = async () => {
  try {
    users.value = await api.users.list();
  } catch (err: any) {
    error.value = err.message;
  }
};

const addUser = async () => {
  if (!newName.value || !newPassword.value || !newRole.value) return;
  try {
    await api.users.create({
        name: newName.value,
        role: newRole.value,
        password: newPassword.value
    });
    newName.value = '';
    newPassword.value = '';
    await fetchUsers();
  } catch (err: any) {
    error.value = err.message;
  }
};

const deleteUser = async (id: string) => {
  try {
    await api.users.delete(id);
    await fetchUsers();
  } catch (err: any) {
    error.value = err.message;
  }
};

onMounted(fetchUsers);
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4 capitalize">{{ type }}</h1>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <div class="mb-6 flex gap-2">
      <input
        v-model="newName"
        class="border p-2 rounded w-full max-w-xs"
        placeholder="Name"
      />
      <input
        v-model="newPassword"
        type="password"
        class="border p-2 rounded w-full max-w-xs"
        placeholder="Password"
      />
      <select v-model="newRole" class="border p-2 rounded">
        <option value="" disabled>Select Role</option>
        <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
      </select>
      <button
        @click="addUser"
        class="bg-amber-600 text-white px-4 py-2 rounded hover:bg-amber-700"
      >
        Add
      </button>
    </div>

    <ul class="space-y-2">
      <li v-for="user in users" :key="user.id" class="border p-4 rounded flex justify-between items-center bg-white shadow-sm">
        <div>
          <span class="font-semibold">{{ user.name }}</span>
          <span class="ml-2 text-sm text-gray-500">({{ user.role }})</span>
        </div>
        <button
          @click="deleteUser(user.id)"
          class="text-red-500 hover:text-red-700"
        >
          Delete
        </button>
      </li>
    </ul>
  </div>
</template>
