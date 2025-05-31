<template>
  <AppLayout>
    <div class="admin-dashboard">
      <div class="admin-header">
        <h1 class="admin-title">Admin Dashboard</h1>
        <p class="admin-subtitle">Manage users, courses, clubs, and system settings</p>
      </div>

      <div class="admin-grid">
        <div class="admin-card" @click="navigateTo('/admin/users')">
          <div class="admin-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <div class="admin-content">
            <h3 class="admin-card-title">User Management</h3>
            <p class="admin-card-description">Manage user accounts, permissions, and handicaps</p>
            <div class="admin-stats">
              <span class="stat-item">{{ userStats.total }} Users</span>
              <span class="stat-item">{{ userStats.admins }} Admins</span>
            </div>
          </div>
          <div class="admin-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9,18 15,12 9,6"></polyline>
            </svg>
          </div>
        </div>

        <div class="admin-card" @click="navigateTo('/admin/courses')">
          <div class="admin-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
            </svg>
          </div>
          <div class="admin-content">
            <h3 class="admin-card-title">Course Management</h3>
            <p class="admin-card-description">Add and manage golf courses and their layouts</p>
            <div class="admin-stats">
              <span class="stat-item">{{ courseStats.total }} Courses</span>
              <span class="stat-item">{{ courseStats.holes }} Total Holes</span>
            </div>
          </div>
          <div class="admin-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9,18 15,12 9,6"></polyline>
            </svg>
          </div>
        </div>

        <div class="admin-card" @click="navigateTo('/admin/clubs')">
          <div class="admin-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path>
            </svg>
          </div>
          <div class="admin-content">
            <h3 class="admin-card-title">Club Management</h3>
            <p class="admin-card-description">Manage golf clubs and their memberships</p>
            <div class="admin-stats">
              <span class="stat-item">{{ clubStats.total }} Clubs</span>
              <span class="stat-item">{{ clubStats.members }} Members</span>
            </div>
          </div>
          <div class="admin-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9,18 15,12 9,6"></polyline>
            </svg>
          </div>
        </div>

        <div class="admin-card" @click="navigateTo('/admin/tee-sets')">
          <div class="admin-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
          </div>
          <div class="admin-content">
            <h3 class="admin-card-title">Tee Set Management</h3>
            <p class="admin-card-description">Configure tee sets and course ratings</p>
            <div class="admin-stats">
              <span class="stat-item">{{ teeStats.total }} Tee Sets</span>
              <span class="stat-item">{{ teeStats.courses }} Courses</span>
            </div>
          </div>
          <div class="admin-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9,18 15,12 9,6"></polyline>
            </svg>
          </div>
        </div>
      </div>

      <!-- Quick Stats Section -->
      <div class="quick-stats">
        <h2 class="section-title">System Overview</h2>
        <div class="stats-row">
          <div class="quick-stat-card">
            <div class="quick-stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
              </svg>
            </div>
            <div class="quick-stat-content">
              <h3 class="quick-stat-number">{{ systemStats.totalUsers }}</h3>
              <p class="quick-stat-label">Total Users</p>
              <span class="quick-stat-change positive">+{{ systemStats.newUsers }} this month</span>
            </div>
          </div>

          <div class="quick-stat-card">
            <div class="quick-stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14,2 14,8 20,8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
            </div>
            <div class="quick-stat-content">
              <h3 class="quick-stat-number">{{ systemStats.totalRounds }}</h3>
              <p class="quick-stat-label">Rounds Played</p>
              <span class="quick-stat-change positive">+{{ systemStats.newRounds }} this week</span>
            </div>
          </div>

          <div class="quick-stat-card">
            <div class="quick-stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M12 6v6l4 2"></path>
              </svg>
            </div>
            <div class="quick-stat-content">
              <h3 class="quick-stat-number">{{ systemStats.activeUsers }}</h3>
              <p class="quick-stat-label">Active Users</p>
              <span class="quick-stat-change neutral">Last 30 days</span>
            </div>
          </div>

          <div class="quick-stat-card">
            <div class="quick-stat-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
            </div>
            <div class="quick-stat-content">
              <h3 class="quick-stat-number">{{ systemStats.avgScore }}</h3>
              <p class="quick-stat-label">Avg Score</p>
              <span class="quick-stat-change negative">+{{ systemStats.scoreChange }} vs last month</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

export default {
  name: 'AdminDashboard',
  components: {
    AppLayout
  },
  setup() {
    const router = useRouter()
    
    // Mock data - replace with actual API calls
    const userStats = ref({
      total: 0,
      admins: 0
    })
    
    const courseStats = ref({
      total: 0,
      holes: 0
    })
    
    const clubStats = ref({
      total: 0,
      members: 0
    })
    
    const teeStats = ref({
      total: 0,
      courses: 0
    })
    
    const systemStats = ref({
      totalUsers: 0,
      newUsers: 0,
      totalRounds: 0,
      newRounds: 0,
      activeUsers: 0,
      avgScore: 0,
      scoreChange: 0
    })
    
    const navigateTo = (path) => {
      router.push(path)
    }
    
    const loadStats = async () => {
      // Mock data - replace with actual API calls
      userStats.value = {
        total: 156,
        admins: 3
      }
      
      courseStats.value = {
        total: 12,
        holes: 216
      }
      
      clubStats.value = {
        total: 8,
        members: 1240
      }
      
      teeStats.value = {
        total: 48,
        courses: 12
      }
      
      systemStats.value = {
        totalUsers: 156,
        newUsers: 12,
        totalRounds: 1847,
        newRounds: 23,
        activeUsers: 89,
        avgScore: 84.2,
        scoreChange: 1.3
      }
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      userStats,
      courseStats,
      clubStats,
      teeStats,
      systemStats,
      navigateTo
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 2rem;
}

.admin-header {
  text-align: center;
  margin-bottom: 3rem;
}

.admin-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.admin-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
  font-weight: 400;
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.admin-card {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.admin-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  transform: translateY(-1px);
  border-color: #2563eb;
}

.admin-icon {
  background: #f1f5f9;
  color: #2563eb;
  padding: 1rem;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.admin-content {
  flex: 1;
}

.admin-card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.admin-card-description {
  color: #64748b;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.admin-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  font-size: 0.8rem;
  color: #475569;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
}

.admin-arrow {
  color: #64748b;
  flex-shrink: 0;
}

.quick-stats {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 1.5rem 0;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.quick-stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.quick-stat-card:hover {
  background: #f1f5f9;
}

.quick-stat-icon {
  background: #2563eb;
  color: white;
  padding: 0.75rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.quick-stat-content {
  flex: 1;
}

.quick-stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.quick-stat-label {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0 0 0.25rem 0;
}

.quick-stat-change {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.125rem 0.375rem;
  border-radius: 3px;
}

.quick-stat-change.positive {
  background: #dcfce7;
  color: #166534;
}

.quick-stat-change.negative {
  background: #fef2f2;
  color: #dc2626;
}

.quick-stat-change.neutral {
  background: #f3f4f6;
  color: #6b7280;
}

@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  
  .admin-header {
    margin-bottom: 2rem;
  }
  
  .admin-title {
    font-size: 2rem;
  }
  
  .admin-subtitle {
    font-size: 1rem;
  }
  
  .admin-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .admin-card {
    padding: 1.5rem;
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .admin-content {
    text-align: center;
  }
  
  .admin-stats {
    justify-content: center;
  }
  
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  
  .quick-stat-card {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .quick-stat-number {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .admin-dashboard {
    padding: 0.5rem;
  }
  
  .admin-title {
    font-size: 1.75rem;
  }
  
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .quick-stats {
    padding: 1.5rem;
  }
}
</style> 