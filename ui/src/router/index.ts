import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PublicHomeView from '../views/PublicHomeView.vue'
import CategoriesView from '../views/CategoriesView.vue'
import ProductsView from '../views/ProductsView.vue'
import UsersView from '../views/UsersView.vue'
import LoginView from '../views/LoginView.vue'
import { api } from '../api'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: PublicHomeView,
    },
    {
      path: '/admin/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/admin',
      children: [
        {
          path: '',
          name: 'admin-home',
          component: HomeView,
        },
        {
          path: 'categories',
          name: 'categories',
          component: CategoriesView,
        },
        {
          path: 'products',
          name: 'products',
          component: ProductsView,
        },
        {
          path: 'users',
          name: 'users',
          component: UsersView,
        },
      ]
    },
  ],
})

router.beforeEach((to, from, next) => {
  if (to.path.startsWith('/admin') && to.name !== 'login' && !api.isAuthenticated()) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router
