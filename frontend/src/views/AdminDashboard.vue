<template>
  <AppLayout>
    <div class="admin-dashboard">
      <div class="admin-header">
        <h1 class="admin-title">Admin Dashboard</h1>
        <p class="admin-subtitle">Manage users, courses, clubs, and tournaments</p>
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
              <span class="stat-item">{{ userStats.total || 0 }} Users</span>
              <span class="stat-item">{{ userStats.admins || 0 }} Admins</span>
              <span class="stat-item">{{ userStats.handicaps || 0 }} Handicaps</span>
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
              <span class="stat-item">{{ clubStats.total || 0 }} Clubs</span>
              <span class="stat-item">{{ clubStats.members || 0 }} Members</span>
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
            <p class="admin-card-description">Manage golf courses, holes, and tee sets</p>
            <div class="admin-stats">
              <span class="stat-item">{{ courseStats.total || 0 }} Courses</span>
              <span class="stat-item">{{ courseStats.holes || 0 }} Holes</span>
              <span class="stat-item">{{ courseStats.teeSets || 0 }} Tee Sets</span>
            </div>
          </div>
          <div class="admin-arrow">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9,18 15,12 9,6"></polyline>
            </svg>
          </div>
        </div>

        <div class="admin-card tournament-coming-soon" @click="navigateTo('/admin/tournaments')">
          <div class="admin-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"></path>
              <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"></path>
              <path d="M4 22h16"></path>
              <path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"></path>
              <path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"></path>
              <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"></path>
            </svg>
          </div>
          <div class="admin-content">
            <h3 class="admin-card-title">Tournament Management</h3>
            <p class="admin-card-description">Organize and manage tournaments (Coming in Phase 2)</p>
            <div class="admin-stats">
              <span class="stat-item coming-soon">Phase 2</span>
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
import { useAuthStore } from '@/store/auth'
import AppLayout from '@/components/AppLayout.vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export default {
  name: 'AdminDashboard',
  components: {
    AppLayout
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // Stats data
    const userStats = ref({
      total: 0,
      admins: 0,
      handicaps: 0
    })
    
    const courseStats = ref({
      total: 0,
      holes: 0,
      teeSets: 0
    })
    
    const clubStats = ref({
      total: 0,
      members: 0
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
    
    const loading = ref(true)
    const error = ref(null)
    
    const navigateTo = (path) => {
      // Navigate to User Management (implemented)
      if (path === '/admin/users') {
        router.push(path)
      } 
      // For tournament management (Phase 2)
      else if (path === '/admin/tournaments') {
        alert(`Tournament Management is coming in Phase 2! This will include tournament creation, player registration, scoring, and results management.`)
      } 
      // For other admin pages not yet implemented
      else {
        alert(`Admin page "${path}" is coming soon! This will be implemented in the next phase.`)
      }
    }
    
    const loadUserStats = async () => {
      try {
        // This would be an admin endpoint to get user statistics
        // For now, using mock data until backend admin endpoints are ready
        userStats.value = {
          total: 23,
          admins: 2,
          handicaps: 45
        }
      } catch (error) {
        console.error('Failed to load user stats:', error)
      }
    }
    
    const loadCourseStats = async () => {
      try {
        // Mock data - replace with real API call when course endpoints are ready
        courseStats.value = {
          total: 5,
          holes: 90,
          teeSets: 20
        }
      } catch (error) {
        console.error('Failed to load course stats:', error)
      }
    }
    
    const loadClubStats = async () => {
      try {
        // Mock data - replace with real API call when club endpoints are ready
        clubStats.value = {
          total: 3,
          members: 156
        }
      } catch (error) {
        console.error('Failed to load club stats:', error)
      }
    }
    
    const loadSystemStats = async () => {
      try {
        // Combine various stats for system overview
        systemStats.value = {
          totalUsers: userStats.value.total,
          newUsers: 3,
          totalRounds: 127,
          newRounds: 8,
          activeUsers: 15,
          avgScore: 87.2,
          scoreChange: 2.1
        }
      } catch (error) {
        console.error('Failed to load system stats:', error)
      }
    }
    
    const loadAllStats = async () => {
      loading.value = true
      error.value = null
      
      try {
        await Promise.all([
          loadUserStats(),
          loadCourseStats(),
          loadClubStats()
        ])
        
        // Load system stats after individual stats are loaded
        await loadSystemStats()
      } catch (err) {
        error.value = 'Failed to load dashboard data'
        console.error('Error loading admin dashboard data:', err)
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      // Check if user is admin
      if (!authStore.currentUser?.is_admin) {
        router.push('/dashboard')
        return
      }
      
      loadAllStats()
    })
    
    return {
      userStats,
      courseStats,
      clubStats,
      systemStats,
      loading,
      error,
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
  color: var(--theme-text-primary);
  margin: 0 0 0.5rem 0;
}

.admin-subtitle {
  font-size: 1.1rem;
  color: var(--theme-text-secondary);
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
  background: var(--theme-bg-card);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: var(--theme-shadow);
  border: 1px solid var(--theme-border);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.admin-card:hover {
  box-shadow: var(--theme-shadow-strong);
  transform: translateY(-1px);
  border-color: var(--theme-primary);
}

.admin-card.tournament-coming-soon {
  opacity: 0.7;
  border-style: dashed;
}

.admin-card.tournament-coming-soon:hover {
  opacity: 0.8;
  transform: none;
  border-color: var(--theme-border);
}

.admin-card.tournament-coming-soon .admin-icon {
  background: var(--theme-border-light);
  color: var(--theme-text-muted);
}

.admin-card.tournament-coming-soon .admin-card-title {
  color: var(--theme-text-secondary);
}

.admin-card.tournament-coming-soon .admin-card-description {
  color: var(--theme-text-muted);
}

.admin-icon {
  background: var(--theme-bg-card-alt);
  color: var(--theme-primary);
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
  color: var(--theme-text-primary);
  margin: 0 0 0.5rem 0;
}

.admin-card-description {
  color: var(--theme-text-secondary);
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.admin-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  font-size: 0.8rem;
  color: var(--theme-text-muted);
  background: var(--theme-bg-card-alt);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
}

.admin-arrow {
  color: var(--theme-text-secondary);
  flex-shrink: 0;
}

.quick-stats {
  background: var(--theme-bg-card);
  border-radius: 8px;
  padding: 2rem;
  box-shadow: var(--theme-shadow);
  border: 1px solid var(--theme-border);
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--theme-text-primary);
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
  background: var(--theme-bg-card-alt);
  border-radius: 6px;
  border: 1px solid var(--theme-border);
  transition: all 0.2s ease;
}

.quick-stat-card:hover {
  background: var(--theme-nav-hover);
}

.quick-stat-icon {
  background: var(--theme-primary);
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
  color: var(--theme-text-primary);
  margin: 0 0 0.25rem 0;
}

.quick-stat-label {
  font-size: 0.9rem;
  color: var(--theme-text-secondary);
  margin: 0 0 0.25rem 0;
}

.quick-stat-change {
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.125rem 0.375rem;
  border-radius: 3px;
}

.quick-stat-change.positive {
  background: var(--theme-success-light);
  color: var(--theme-success);
}

.quick-stat-change.negative {
  background: var(--theme-error-light);
  color: var(--theme-error);
}

.quick-stat-change.neutral {
  background: var(--theme-bg-card-alt);
  color: var(--theme-text-muted);
}

.stat-item.coming-soon {
  background: var(--theme-warning-light);
  color: var(--theme-warning);
  font-weight: 600;
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