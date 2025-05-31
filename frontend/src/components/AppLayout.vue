<template>
  <div class="app-layout" :class="{ 'sidebar-open': showSidebar }">
    <!-- Header with Hamburger Menu -->
    <header class="app-header">
      <div class="header-content">
        <button @click="toggleSidebar" class="menu-toggle">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="3" y1="6" x2="21" y2="6"></line>
            <line x1="3" y1="12" x2="21" y2="12"></line>
            <line x1="3" y1="18" x2="21" y2="18"></line>
          </svg>
        </button>
        
        <div class="logo-section">
          <h1 class="logo">RGS</h1>
          <span class="tagline">Rykket's Golf Service</span>
        </div>
      </div>
    </header>

    <div class="app-body">
      <!-- Sidebar Navigation -->
      <nav class="sidebar" :class="{ 'sidebar-visible': showSidebar }">
        <div class="sidebar-content">
          <!-- Main Navigation -->
          <div class="nav-section">
            <router-link 
              to="/dashboard" 
              class="nav-item" 
              :class="{ active: $route.path === '/dashboard' }"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                <polyline points="9,22 9,12 15,12 15,22"></polyline>
              </svg>
              <span>Dashboard</span>
            </router-link>

            <!-- Admin Dashboard - Only for Admins -->
            <!-- Debug: {{ authStore.currentUser }} -->
            <router-link 
              v-if="authStore.currentUser?.is_admin" 
              to="/admin-dashboard" 
              class="nav-item" 
              :class="{ active: $route.path === '/admin-dashboard' }"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              <span>Admin Dashboard</span>
            </router-link>

            <router-link 
              to="/profile" 
              class="nav-item" 
              :class="{ active: $route.path === '/profile' }"
            >
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>Profile</span>
            </router-link>

            <div class="nav-item" @click="toggleRoundsSubmenu">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14,2 14,8 20,8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
              <span>Rounds</span>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ rotated: showRoundsSubmenu }" class="submenu-arrow">
                <polyline points="6,9 12,15 18,9"></polyline>
              </svg>
            </div>

            <!-- Rounds Submenu -->
            <div v-show="showRoundsSubmenu" class="submenu">
              <a href="#" class="submenu-item">New Round</a>
              <a href="#" class="submenu-item">Round History</a>
              <a href="#" class="submenu-item">Statistics</a>
            </div>
          </div>

          <!-- User Section with Separator -->
          <div class="user-section">
            <div class="user-separator"></div>
            <div class="user-info">
              <div class="user-avatar">
                {{ userInitials }}
              </div>
              <div class="user-details">
                <span class="user-name">{{ fullName }}</span>
                <span class="user-email">{{ authStore.currentUser?.email }}</span>
              </div>
              <button @click="toggleUserMenu" class="user-menu-toggle">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" :class="{ rotated: showUserMenu }">
                  <polyline points="6,9 12,15 18,9"></polyline>
                </svg>
              </button>
            </div>

            <!-- User Menu -->
            <div v-show="showUserMenu" class="user-menu">
              <button @click="handleLogout" class="user-menu-item logout">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                  <polyline points="16,17 21,12 16,7"></polyline>
                  <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <!-- Main Content -->
      <main class="app-main" :class="{ 'content-pushed': showSidebar }">
        <slot />
      </main>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

export default {
  name: 'AppLayout',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const showSidebar = ref(false)
    const showRoundsSubmenu = ref(false)
    const showUserMenu = ref(false)
    
    const fullName = computed(() => {
      const user = authStore.currentUser
      if (user) {
        return `${user.first_name} ${user.last_name}`
      }
      return 'User'
    })
    
    const userInitials = computed(() => {
      const user = authStore.currentUser
      if (user) {
        const first = user.first_name?.[0] || ''
        const last = user.last_name?.[0] || ''
        return `${first}${last}`.toUpperCase()
      }
      return 'U'
    })
    
    const toggleSidebar = () => {
      console.log('Toggle sidebar clicked, current state:', showSidebar.value)
      showSidebar.value = !showSidebar.value
      console.log('New state:', showSidebar.value)
    }
    
    const closeSidebar = () => {
      showSidebar.value = false
      showRoundsSubmenu.value = false
      showUserMenu.value = false
    }
    
    const toggleRoundsSubmenu = () => {
      showRoundsSubmenu.value = !showRoundsSubmenu.value
    }
    
    const toggleUserMenu = () => {
      showUserMenu.value = !showUserMenu.value
    }
    
    const handleLogout = async () => {
      await authStore.logout()
      router.push('/')
    }
    
    return {
      authStore,
      showSidebar,
      showRoundsSubmenu,
      showUserMenu,
      fullName,
      userInitials,
      toggleSidebar,
      closeSidebar,
      toggleRoundsSubmenu,
      toggleUserMenu,
      handleLogout
    }
  }
}
</script>

<style>
/* Component-specific styles only - theme variables are now global */
</style>

<style scoped>
.app-layout {
  min-height: 100vh;
  background: var(--theme-bg-main);
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--theme-bg-header);
  border-bottom: 2px solid var(--theme-border);
  padding: 0;
  box-shadow: 0 4px 12px var(--theme-shadow-strong);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 64px;
}

.header-content {
  max-width: none;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
  height: 64px;
}

.menu-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 1rem;
  transition: background 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--theme-text-secondary);
  flex-shrink: 0;
  height: 64px;
  min-width: 64px;
}

.menu-toggle:hover {
  background: var(--theme-nav-hover);
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  justify-content: center;
  margin-right: 64px; /* Offset for hamburger button to center logo */
}

.logo {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  color: var(--theme-text-primary);
}

.tagline {
  font-size: 0.9rem;
  color: var(--theme-text-secondary);
  font-weight: 400;
}

.app-body {
  display: flex;
  flex-direction: row;
  flex: 1;
  position: relative;
  margin-top: 64px;
}

.sidebar {
  width: 300px;
  background: var(--theme-bg-sidebar);
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px var(--theme-shadow);
  position: fixed;
  left: 0;
  top: 64px;
  height: calc(100vh - 64px);
  transform: translateX(-100%);
  transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  z-index: 40;
}

.sidebar.sidebar-visible {
  transform: translateX(0);
}

.app-main {
  flex: 1;
  transition: margin-left 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  margin-left: 0;
  min-height: calc(100vh - 64px);
}

.app-main.content-pushed {
  margin-left: 300px;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 0;
  overflow-y: auto;
}

.nav-section {
  display: flex;
  flex-direction: column;
  gap: 0;
  flex: 1;
  padding: 1rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  text-decoration: none;
  color: var(--theme-text-secondary);
  transition: all 0.2s ease;
  cursor: pointer;
  background: none;
  border: none;
  font-size: 0.95rem;
  font-weight: 500;
  width: 100%;
  text-align: left;
  position: relative;
  overflow: hidden;
}

.nav-item:hover {
  background: var(--theme-nav-hover);
  color: var(--theme-text-primary);
}

.nav-item.active {
  background: var(--theme-nav-active-bg);
  color: var(--theme-nav-active-text);
  position: relative;
  font-weight: 600;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: var(--theme-primary);
}

/* Click ripple animation */
.nav-item::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.4s ease, height 0.4s ease;
  pointer-events: none;
  opacity: 0;
}

.nav-item:active::after {
  width: 300px;
  height: 300px;
  opacity: 1;
  transition: width 0.1s ease, height 0.1s ease, opacity 0.1s ease;
}

.nav-item svg {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
}

.nav-item span {
  flex: 1;
}

.submenu-arrow {
  margin-left: auto;
  transition: transform 0.2s ease;
}

.submenu-arrow.rotated {
  transform: rotate(180deg);
}

.submenu {
  padding: 0.5rem 0;
  display: flex;
  flex-direction: column;
  gap: 0;
  background: rgba(0, 0, 0, 0.02);
}

.submenu-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 3rem;
  text-decoration: none;
  color: var(--theme-text-muted);
  transition: all 0.2s ease;
  font-size: 0.9rem;
}

.submenu-item:hover {
  background: var(--theme-nav-hover);
  color: var(--theme-text-secondary);
}

.user-section {
  padding: 0 1rem 1rem;
}

.user-separator {
  height: 1px;
  background: var(--theme-border);
  margin: 1rem 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 8px;
  transition: background 0.2s ease;
}

.user-info:hover {
  background: var(--theme-nav-hover);
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--theme-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.user-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: var(--theme-text-primary);
  font-size: 0.9rem;
}

.user-email {
  font-size: 0.8rem;
  color: var(--theme-text-secondary);
}

.user-menu-toggle {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background 0.2s ease;
  color: var(--theme-text-muted);
}

.user-menu-toggle:hover {
  background: var(--theme-border);
}

.user-menu-toggle svg.rotated {
  transform: rotate(180deg);
}

.user-menu {
  margin-top: 0.5rem;
  padding: 0.5rem 0;
  border-top: 1px solid var(--theme-border);
}

.user-menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem 1rem;
  background: none;
  border: none;
  text-decoration: none;
  color: var(--theme-text-secondary);
  border-radius: 4px;
  transition: all 0.2s ease;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  text-align: left;
}

.user-menu-item:hover {
  background: var(--theme-nav-hover);
  color: var(--theme-text-primary);
}

.user-menu-item.logout:hover {
  background: #fef2f2;
  color: var(--theme-error);
}

.mobile-overlay {
  display: none;
}

@media (max-width: 768px) {
  .mobile-overlay {
    display: block;
    position: fixed;
    top: 64px;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 500;
  }
  
  .header-content {
    padding: 0;
  }
  
  .logo {
    font-size: 1.5rem;
  }
  
  .tagline {
    font-size: 0.8rem;
  }
  
  .sidebar {
    width: 85vw;
    z-index: 1000;
  }
  
  .app-main.content-pushed {
    margin-left: 0;
  }
}

@media (min-width: 769px) {
  /* Desktop behavior - close button hidden since we have push layout */
  .close-btn {
    display: none;
  }
}
</style> 