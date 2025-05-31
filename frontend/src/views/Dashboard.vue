<template>
  <AppLayout>
    <div class="welcome-section">
      <h2 class="welcome-title">Welcome back, {{ firstName }}!</h2>
      <p class="welcome-subtitle">Ready to manage your golf rounds?</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 6v6l4 2"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">0</h3>
          <p class="stat-label">Rounds Played</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">--</h3>
          <p class="stat-label">Average Score</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">0</h3>
          <p class="stat-label">Playing Partners</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="22,12 18,12 15,21 9,3 6,12 2,12"></polyline>
          </svg>
        </div>
        <div class="stat-content">
          <h3 class="stat-number">{{ currentHandicap || '--' }}</h3>
          <p class="stat-label">Current Handicap</p>
        </div>
      </div>
    </div>
    
    <div class="action-grid">
      <div class="action-card">
        <div class="action-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="3"></circle>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
          </svg>
        </div>
        <div class="action-content">
          <h3 class="action-title">New Round</h3>
          <p class="action-description">Start tracking a new golf round</p>
          <button class="action-button primary">Start Round</button>
        </div>
      </div>
      
      <div class="action-card">
        <div class="action-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14,2 14,8 20,8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10,9 9,9 8,9"></polyline>
          </svg>
        </div>
        <div class="action-content">
          <h3 class="action-title">View History</h3>
          <p class="action-description">Review your past rounds and scores</p>
          <button class="action-button secondary">View Rounds</button>
        </div>
      </div>
      
      <div class="action-card">
        <div class="action-icon">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <div class="action-content">
          <h3 class="action-title">Profile</h3>
          <p class="action-description">Update your profile and preferences</p>
          <router-link to="/profile" class="action-button secondary">Edit Profile</router-link>
        </div>
      </div>
    </div>
    
    <div class="recent-activity">
      <h3 class="section-title">Recent Activity</h3>
      <div class="activity-placeholder">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
          <line x1="9" y1="9" x2="9.01" y2="9"></line>
          <line x1="15" y1="9" x2="15.01" y2="9"></line>
        </svg>
        <h4>Welcome to RGS!</h4>
        <p>Start by recording your first golf round to see your activity here.</p>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '@/store/auth'
import AppLayout from '@/components/AppLayout.vue'

export default {
  name: 'Dashboard',
  components: {
    AppLayout
  },
  setup() {
    const authStore = useAuthStore()
    
    const firstName = computed(() => {
      return authStore.currentUser?.first_name || 'User'
    })
    
    const currentHandicap = computed(() => {
      const user = authStore.currentUser
      if (user && user.current_handicap !== null) {
        return user.current_handicap
      }
      return null
    })
    
    return {
      firstName,
      currentHandicap
    }
  }
}
</script>

<style scoped>
.welcome-section {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
}

.welcome-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--theme-text-primary);
  margin: 0 0 0.5rem 0;
}

.welcome-subtitle {
  font-size: 1.1rem;
  color: var(--theme-text-secondary);
  margin: 0;
  font-weight: 400;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin: 0 2rem 3rem 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px var(--theme-shadow);
  border: 1px solid var(--theme-border);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: 0 4px 6px var(--theme-shadow-strong);
  transform: translateY(-1px);
}

.stat-icon {
  background: var(--theme-primary);
  color: white;
  padding: 0.75rem;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--theme-text-primary);
  margin: 0 0 0.25rem 0;
}

.stat-label {
  font-size: 0.9rem;
  color: var(--theme-text-secondary);
  margin: 0;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin: 0 2rem 3rem 2rem;
}

.action-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px var(--theme-shadow);
  border: 1px solid var(--theme-border);
  text-align: center;
  transition: all 0.2s ease;
}

.action-card:hover {
  box-shadow: 0 4px 6px var(--theme-shadow-strong);
  transform: translateY(-1px);
}

.action-icon {
  background: var(--theme-border-light);
  color: var(--theme-primary);
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem auto;
}

.action-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--theme-text-primary);
  margin: 0 0 0.5rem 0;
}

.action-description {
  color: var(--theme-text-secondary);
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
}

.action-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  text-decoration: none;
  display: inline-block;
}

.action-button.primary {
  background: var(--theme-primary);
  color: white;
}

.action-button.primary:hover {
  background: var(--theme-primary-dark);
}

.action-button.secondary {
  background: var(--theme-border-light);
  color: var(--theme-text-secondary);
  border: 1px solid var(--theme-border);
}

.action-button.secondary:hover {
  background: var(--theme-border);
  color: var(--theme-text-primary);
}

.recent-activity {
  background: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 1px 3px var(--theme-shadow);
  border: 1px solid var(--theme-border);
  margin: 0 2rem;
}

.section-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--theme-text-primary);
  margin: 0 0 1.5rem 0;
}

.activity-placeholder {
  text-align: center;
  padding: 3rem 1rem;
  color: var(--theme-text-secondary);
}

.activity-placeholder svg {
  margin-bottom: 1rem;
  opacity: 0.6;
}

.activity-placeholder h4 {
  font-size: 1.1rem;
  color: var(--theme-text-secondary);
  margin: 0 0 0.5rem 0;
}

.activity-placeholder p {
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .welcome-section {
    padding: 1rem;
    margin-bottom: 2rem;
  }
  
  .welcome-title {
    font-size: 2rem;
  }
  
  .welcome-subtitle {
    font-size: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin: 0 1rem 2rem 1rem;
  }
  
  .stat-card {
    padding: 1rem;
    flex-direction: column;
    text-align: center;
    gap: 0.75rem;
  }
  
  .stat-icon {
    align-self: center;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  .stat-label {
    font-size: 0.8rem;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    margin: 0 1rem 2rem 1rem;
  }
  
  .action-card {
    padding: 1.5rem;
  }
  
  .action-icon {
    width: 56px;
    height: 56px;
    margin-bottom: 1rem;
  }
  
  .action-title {
    font-size: 1.1rem;
  }
  
  .action-description {
    font-size: 0.9rem;
  }
  
  .action-button {
    padding: 1rem 1.5rem;
    width: 100%;
  }
  
  .recent-activity {
    padding: 1.5rem;
    margin: 0 1rem;
  }
  
  .section-title {
    font-size: 1.2rem;
  }
  
  .activity-placeholder {
    padding: 2rem 1rem;
  }
  
  .activity-placeholder h4 {
    font-size: 1rem;
  }
  
  .activity-placeholder p {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .welcome-section {
    padding: 0.5rem;
  }
  
  .welcome-title {
    font-size: 1.75rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
    margin: 0 0.5rem 1.5rem 0.5rem;
  }
  
  .stat-card {
    padding: 0.75rem;
  }
  
  .action-grid {
    gap: 0.75rem;
    margin: 0 0.5rem 1.5rem 0.5rem;
  }
  
  .action-card {
    padding: 1.25rem;
  }
  
  .recent-activity {
    padding: 1.25rem;
    margin: 0 0.5rem;
  }
  
  .activity-placeholder {
    padding: 1.5rem 0.5rem;
  }
}
</style> 