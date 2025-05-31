import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import Welcome from '@/views/Welcome.vue'
import Dashboard from '@/views/Dashboard.vue'
import Profile from '@/views/Profile.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'

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
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/admin-dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, requiresAdmin: true }
  }
  // Admin routes (commented out until components are created)
  // {
  //   path: '/admin/users',
  //   name: 'AdminUsers',
  //   component: () => import('@/views/admin/AdminUsers.vue'),
  //   meta: { requiresAuth: true, requiresAdmin: true }
  // },
  // {
  //   path: '/admin/courses',
  //   name: 'AdminCourses', 
  //   component: () => import('@/views/admin/AdminCourses.vue'),
  //   meta: { requiresAuth: true, requiresAdmin: true }
  // },
  // {
  //   path: '/admin/clubs',
  //   name: 'AdminClubs',
  //   component: () => import('@/views/admin/AdminClubs.vue'),
  //   meta: { requiresAuth: true, requiresAdmin: true }
  // },
  // {
  //   path: '/admin/tee-sets',
  //   name: 'AdminTeeSets',
  //   component: () => import('@/views/admin/AdminTeeSets.vue'),
  //   meta: { requiresAuth: true, requiresAdmin: true }
  // }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Initialize auth if needed
  if (authStore.token && !authStore.user) {
    authStore.initializeAuth()
  }
  
  const isAuthenticated = authStore.isAuthenticated
  const user = authStore.currentUser
  
  // Check authentication requirements
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/')
    return
  }
  
  // Check guest-only routes
  if (to.meta.requiresGuest && isAuthenticated) {
    next('/dashboard')
    return
  }
  
  // Check admin requirements
  if (to.meta.requiresAdmin && (!user || !user.is_admin)) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router 