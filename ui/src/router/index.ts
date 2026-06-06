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
      component: LoginView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
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
  const isAuthenticated = api.isAuthenticated();
  const userRole = api.getUserRole();
  
  // Protect routes that require authentication
  const protectedRoutes = ['/admin', '/bar', '/deliverer'];
  const isProtectedRoute = protectedRoutes.some(route => to.path.startsWith(route));
  
  if (isProtectedRoute && !isAuthenticated) {
    next({ name: 'login' });
    return;
  }

  // Check role-based access
  if (isProtectedRoute && isAuthenticated) {
    if (to.path.startsWith('/admin') && userRole !== 'admin') {
      next({ name: userRole === 'bar' ? 'bar' : 'deliverer' });
      return;
    }
    if (to.path.startsWith('/bar') && userRole !== 'bar') {
      next({ name: userRole === 'admin' ? 'admin-home' : 'deliverer' });
      return;
    }
    if (to.path.startsWith('/deliverer') && userRole !== 'deliverer') {
      next({ name: userRole === 'admin' ? 'admin-home' : 'bar' });
      return;
    }
  }

  next();
});

export default router
