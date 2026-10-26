<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { api } from '../api';

const username = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();
const { t } = useI18n();

const login = async () => {
    error.value = '';

    try {
        await api.login(username.value, password.value);
        const userRole = api.getUserRole();
        
        // Redirect based on user role
        if (userRole === 'admin') {
            router.push('/admin');
        } else if (userRole === 'bar') {
            router.push('/bar');
        } else if (userRole === 'deliverer') {
            router.push('/deliverer');
        } else {
            // Fallback in case role is unknown
            router.push('/');
        }
    } catch (e) {
        api.clearCredentials();
        error.value = t('login.invalidCredentials');
    }
};
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-amber-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-amber-900">
          {{ t('login.title') }}
        </h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="login">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">{{ t('login.username') }}</label>
            <input id="username" v-model="username" name="username" type="text" required
                   class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-amber-500 focus:border-amber-500 focus:z-10 sm:text-sm"
                   :placeholder="t('login.username')" />
          </div>
          <div>
            <label for="password" class="sr-only">{{ t('login.password') }}</label>
            <input id="password" v-model="password" name="password" type="password" required
                   class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-amber-500 focus:border-amber-500 focus:z-10 sm:text-sm"
                   :placeholder="t('login.password')" />
          </div>
        </div>

        <div v-if="error" class="text-red-500 text-sm text-center">
          {{ error }}
        </div>

        <div>
          <button type="submit"
                  class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-amber-600 hover:bg-amber-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-amber-500">
            {{ t('login.signIn') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
