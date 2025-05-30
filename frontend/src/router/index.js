import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import Welcome from '@/views/Welcome.vue'
import Dashboard from '@/views/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Welcome',
    component: Welcome,
    meta: { requiresGuest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth if not already done
  if (authStore.token && !authStore.user) {
    authStore.initializeAuth()
  }
  
  // Check if route requires authentication
  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      next({ name: 'Welcome' })
      return
    }
  }
  
  // Check if route requires guest (not authenticated)
  if (to.meta.requiresGuest) {
    if (authStore.isLoggedIn) {
      next({ name: 'Dashboard' })
      return
    }
  }
  
  next()
})

export default router 