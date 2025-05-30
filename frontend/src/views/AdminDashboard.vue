<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1>🛠️ Admin Dashboard</h1>
        <p class="subtitle">Manage users and handicaps</p>
      </div>
    </div>

    <!-- Admin Navigation -->
    <div class="admin-nav">
      <button 
        @click="activeTab = 'users'"
        :class="['nav-btn', { active: activeTab === 'users' }]"
      >
        👥 User Management
      </button>
      <button 
        @click="activeTab = 'handicaps'"
        :class="['nav-btn', { active: activeTab === 'handicaps' }]"
      >
        ⛳ Handicap Management
      </button>
    </div>

    <!-- User Management Tab -->
    <div v-if="activeTab === 'users'" class="tab-content">
      <UserManagement />
    </div>

    <!-- Handicap Management Tab -->
    <div v-if="activeTab === 'handicaps'" class="tab-content">
      <HandicapManagement />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'
import UserManagement from '../components/UserManagement.vue'
import HandicapManagement from '../components/HandicapManagement.vue'

export default {
  name: 'AdminDashboard',
  components: {
    UserManagement,
    HandicapManagement
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    const activeTab = ref('users')

    onMounted(() => {
      // Check if user is admin
      if (!authStore.user?.is_admin) {
        router.push('/dashboard')
      }
    })

    return {
      activeTab
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 2rem;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 3rem;
}

.header-content h1 {
  font-size: 3rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 1.2rem;
  color: #64748b;
  margin: 0;
}

.admin-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

.nav-btn {
  padding: 1rem 2rem;
  border: 2px solid #e2e8f0;
  background: white;
  color: #64748b;
  font-size: 1.1rem;
  font-weight: 500;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 200px;
}

.nav-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
  transform: translateY(-2px);
}

.nav-btn.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.3);
}

.tab-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  
  .header-content h1 {
    font-size: 2rem;
  }
  
  .nav-btn {
    min-width: auto;
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
}
</style> 