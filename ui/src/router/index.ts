import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/admin/HomeView.vue'
import PublicHomeView from '../views/PublicHomeView.vue'
import CategoriesView from '../views/admin/CategoriesView.vue'
import ProductsView from '../views/admin/ProductsView.vue'
import UsersView from '../views/admin/UsersView.vue'
import BarView from '../views/bar/BarView.vue'
import DelivererView from '../views/deliverer/DelivererView.vue'
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
      path: '/bar',
      name: 'bar',
      component: BarView,
    },
    {
      path: '/deliverer',
      name: 'deliverer',
      component: DelivererView,
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
  const isProtected = to.path.startsWith('/admin') || to.path.startsWith('/bar') || to.path.startsWith('/deliverer');
  if (isProtected && to.name !== 'login' && !api.isAuthenticated()) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router
