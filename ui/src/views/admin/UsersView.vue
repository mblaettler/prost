<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { api } from '../../api';
import AdminLayout from '../../components/AdminLayout.vue';

const { t } = useI18n();
const users = ref<any[]>([]);
const newName = ref('');
const newPassword = ref('');
const newRole = ref('');
const error = ref('');

const roles = computed(() =>
  (['admin', 'bar', 'deliverer'] as const).map((id) => ({ id, name: t(`roles.${id}`) }))
);

const roleName = (role: string) =>
  roles.value.find((r) => r.id === role)?.name ?? role;

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
      password: newPassword.value,
    });
    newName.value = '';
    newPassword.value = '';
    newRole.value = '';
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
  <AdminLayout>
    <template #title>{{ t('admin.users') }}</template>

    <div class="max-w-4xl">
      <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
        {{ error }}
      </div>

      <!-- Add New User -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">{{ t('admin.usersView.addNew') }}</h3>
        <div class="flex gap-3">
          <input
            v-model="newName"
            class="flex-1 border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            :placeholder="t('admin.usersView.usernamePlaceholder')"
          />
          <input
            v-model="newPassword"
            type="password"
            class="flex-1 border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
            :placeholder="t('admin.usersView.passwordPlaceholder')"
          />
          <select
            v-model="newRole"
            class="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-amber-500"
          >
            <option value="" disabled>{{ t('admin.usersView.selectRole') }}</option>
            <option v-for="role in roles" :key="role.id" :value="role.id">{{ role.name }}</option>
          </select>
          <button
            @click="addUser"
            class="bg-amber-600 text-white px-6 py-3 rounded-lg hover:bg-amber-700 transition-colors font-medium"
          >
            {{ t('admin.usersView.add') }}
          </button>
        </div>
      </div>

      <!-- Users List -->
      <div class="bg-white rounded-lg shadow-sm overflow-hidden">
        <div v-if="users.length === 0" class="p-8 text-center text-gray-500">
          <p class="text-lg">{{ t('admin.usersView.empty') }}</p>
        </div>
        <ul v-else class="divide-y">
          <li v-for="user in users" :key="user.id" class="p-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
            <div>
              <span class="font-semibold text-gray-900">{{ user.name }}</span>
              <span class="ml-3 text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded">
                {{ roleName(user.role) }}
              </span>
            </div>
            <button
              @click="deleteUser(user.id)"
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

