<template>
  <AppLayout>
    <div class="profile-container">
      <div class="profile-header">
        <div class="profile-avatar">
          {{ userInitials }}
        </div>
        <div class="profile-info">
          <h1 class="profile-name">{{ fullName }}</h1>
          <p class="profile-email">{{ authStore.currentUser?.email }}</p>
          <small class="email-note">Email changes can be made in Account Settings</small>
          <span class="profile-status" :class="{ active: authStore.currentUser?.is_active }">
            {{ authStore.currentUser?.is_active ? 'Active' : 'Inactive' }}
          </span>
        </div>
      </div>

      <!-- Personal Information Section -->
      <div class="profile-section">
        <div class="section-header" @click="toggleSection('personal')">
          <h2 class="section-title">Personal Information</h2>
          <svg 
            width="20" 
            height="20" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            :class="{ rotated: expandedSections.personal }"
            class="section-arrow"
          >
            <polyline points="6,9 12,15 18,9"></polyline>
          </svg>
        </div>
        
        <transition name="slide" mode="out-in">
          <div v-if="expandedSections.personal" class="section-content">
            <form @submit.prevent="updateProfile" class="profile-form">
              <div class="form-grid">
                <div class="form-group">
                  <label for="first_name">First Name</label>
                  <input
                    id="first_name"
                    v-model="editForm.first_name"
                    type="text"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="last_name">Last Name</label>
                  <input
                    id="last_name"
                    v-model="editForm.last_name"
                    type="text"
                    required
                  />
                </div>

                <div class="form-group">
                  <label for="sex">Gender</label>
                  <select id="sex" v-model="editForm.sex">
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="country">Country</label>
                  <input
                    id="country"
                    v-model="editForm.country"
                    type="text"
                  />
                </div>

                <div class="form-group">
                  <label for="city">City</label>
                  <input
                    id="city"
                    v-model="editForm.city"
                    type="text"
                  />
                </div>

                <div class="form-group full-width">
                  <label for="address">Address</label>
                  <input
                    id="address"
                    v-model="editForm.address"
                    type="text"
                  />
                </div>

                <div class="form-group">
                  <label for="postal_code">Postal Code</label>
                  <input
                    id="postal_code"
                    v-model="editForm.postal_code"
                    type="text"
                  />
                </div>

                <div class="form-group">
                  <label for="timezone">Timezone</label>
                  <select id="timezone" v-model="editForm.timezone">
                    <option value="UTC">UTC</option>
                    <option value="America/New_York">Eastern Time</option>
                    <option value="America/Chicago">Central Time</option>
                    <option value="America/Denver">Mountain Time</option>
                    <option value="America/Los_Angeles">Pacific Time</option>
                    <option value="Europe/London">London</option>
                    <option value="Europe/Paris">Paris</option>
                    <option value="Europe/Oslo">Oslo</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="distance_unit">Distance Unit</label>
                  <select id="distance_unit" v-model="editForm.distance_unit">
                    <option value="yards">Yards</option>
                    <option value="meters">Meters</option>
                  </select>
                </div>
              </div>

              <div class="form-actions">
                <button type="submit" class="btn-primary" :disabled="updating">
                  {{ updating ? 'Updating...' : 'Update Profile' }}
                </button>
              </div>
            </form>
          </div>
        </transition>
      </div>

      <!-- Handicap Management Section -->
      <div class="profile-section">
        <div class="section-header" @click="toggleSection('handicap')">
          <h2 class="section-title">Handicap Management</h2>
          <svg 
            width="20" 
            height="20" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            :class="{ rotated: expandedSections.handicap }"
            class="section-arrow"
          >
            <polyline points="6,9 12,15 18,9"></polyline>
          </svg>
        </div>
        
        <transition name="slide" mode="out-in">
          <div v-if="expandedSections.handicap" class="section-content">
            <UserHandicapManagement />
          </div>
        </transition>
      </div>

      <!-- Account Settings Section -->
      <div class="profile-section">
        <div class="section-header" @click="toggleSection('settings')">
          <h2 class="section-title">Account Settings</h2>
          <svg 
            width="20" 
            height="20" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            stroke-width="2" 
            :class="{ rotated: expandedSections.settings }"
            class="section-arrow"
          >
            <polyline points="6,9 12,15 18,9"></polyline>
          </svg>
        </div>
        
        <transition name="slide" mode="out-in">
          <div v-if="expandedSections.settings" class="section-content">
            <div class="settings-content">
              <div class="setting-item">
                <h3>Change Password</h3>
                <p>Update your account password for security</p>
                <button class="btn-secondary">Change Password</button>
              </div>
              
              <div class="setting-item danger-zone">
                <h3>Danger Zone</h3>
                <p>Permanently delete your account and all associated data</p>
                <button class="btn-danger">Delete Account</button>
              </div>
            </div>
          </div>
        </transition>
      </div>

      <!-- Toast Notification -->
      <div v-if="showToast" :class="['toast', toastType]">
        {{ toastMessage }}
      </div>
    </div>
  </AppLayout>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'
import AppLayout from '@/components/AppLayout.vue'
import UserHandicapManagement from '@/components/UserHandicapManagement.vue'

export default {
  name: 'Profile',
  components: {
    AppLayout,
    UserHandicapManagement
  },
  setup() {
    const authStore = useAuthStore()
    
    // Toast notification state
    const showToast = ref(false)
    const toastMessage = ref('')
    const toastType = ref('success') // 'success' or 'error'
    
    // Expanded sections state
    const expandedSections = ref({
      personal: false,
      handicap: false,
      settings: false
    })
    
    // Use computed properties to work directly with store data
    const profileForm = computed({
      get: () => ({
        first_name: authStore.currentUser?.first_name || '',
        last_name: authStore.currentUser?.last_name || '',
        email: authStore.currentUser?.email || '',
        sex: authStore.currentUser?.sex || 'M',
        country: authStore.currentUser?.country || '',
        city: authStore.currentUser?.city || '',
        address: authStore.currentUser?.address || '',
        postal_code: authStore.currentUser?.postal_code || '',
        timezone: authStore.currentUser?.timezone || 'UTC',
        distance_unit: authStore.currentUser?.distance_unit || 'yards'
      }),
      set: (value) => {
        // We'll handle updates through the updateProfile method
        console.log('Profile form updated:', value)
      }
    })
    
    // Local reactive form for editing
    const editForm = ref({
      first_name: '',
      last_name: '',
      sex: 'M',
      country: '',
      city: '',
      address: '',
      postal_code: '',
      timezone: 'UTC',
      distance_unit: 'yards'
    })
    
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
    
    const showToastNotification = (message, type = 'success') => {
      toastMessage.value = message
      toastType.value = type
      showToast.value = true
      
      // Auto hide after 3 seconds
      setTimeout(() => {
        showToast.value = false
      }, 3000)
    }
    
    const toggleSection = (section) => {
      expandedSections.value[section] = !expandedSections.value[section]
      
      // Load current data into edit form when opening personal section
      if (section === 'personal' && expandedSections.value[section]) {
        loadEditForm()
      }
    }
    
    const loadEditForm = () => {
      const user = authStore.currentUser
      if (user) {
        editForm.value = {
          first_name: user.first_name || '',
          last_name: user.last_name || '',
          sex: user.sex || 'M',
          country: user.country || '',
          city: user.city || '',
          address: user.address || '',
          postal_code: user.postal_code || '',
          timezone: user.timezone || 'UTC',
          distance_unit: user.distance_unit || 'yards'
        }
      }
    }
    
    const updateProfile = async () => {
      try {
        const result = await authStore.updateProfile(editForm.value)
        if (result.success) {
          showToastNotification('Profile updated successfully!', 'success')
        } else {
          showToastNotification(result.error || 'Profile update failed', 'error')
        }
      } catch (error) {
        showToastNotification('An unexpected error occurred', 'error')
        console.error('Error updating profile:', error)
      }
    }
    
    return {
      authStore,
      profileForm,
      editForm,
      expandedSections,
      fullName,
      userInitials,
      showToast,
      toastMessage,
      toastType,
      toggleSection,
      updateProfile,
      updating: computed(() => authStore.loading)
    }
  }
}
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--theme-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.5rem;
}

.profile-info {
  flex: 1;
}

.profile-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.profile-email {
  color: #64748b;
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.email-note {
  color: var(--theme-text-muted);
  font-size: 0.8rem;
  margin-bottom: 0.5rem;
  display: block;
}

.profile-status {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  background: #fef2f2;
  color: #dc2626;
}

.profile-status.active {
  background: #dcfce7;
  color: #166534;
}

.profile-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  margin-bottom: 1.5rem;
  overflow: hidden;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  cursor: pointer;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
  transition: background 0.2s ease;
}

.section-header:hover {
  background: #f1f5f9;
}

.section-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.section-arrow {
  color: #64748b;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.section-arrow.rotated {
  transform: rotate(180deg);
}

.section-content {
  padding: 2rem;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideDown 0.4s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
    max-height: 0;
  }
  to {
    opacity: 1;
    transform: translateY(0);
    max-height: 1000px;
  }
}

.section-content[style*="display: none"] {
  animation: slideUp 0.4s ease-in;
  max-height: 0;
  padding: 0 2rem;
}

@keyframes slideUp {
  from {
    opacity: 1;
    transform: translateY(0);
    max-height: 1000px;
  }
  to {
    opacity: 0;
    transform: translateY(-20px);
    max-height: 0;
  }
}

.profile-form {
  width: 100%;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--theme-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-primary {
  background: var(--theme-primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: var(--theme-primary-dark);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.settings-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.setting-item.danger-zone {
  background: #fef2f2;
  border-color: #fecaca;
}

.setting-item h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.setting-item p {
  color: #64748b;
  margin: 0;
  font-size: 0.9rem;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
  padding: 0.5rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-danger {
  background: #dc2626;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease;
}

.btn-danger:hover {
  background: #b91c1c;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
    padding: 1.5rem;
  }
  
  .profile-avatar {
    width: 60px;
    height: 60px;
    font-size: 1.2rem;
  }
  
  .profile-name {
    font-size: 1.5rem;
  }
  
  .section-header {
    padding: 1rem 1.5rem;
  }
  
  .section-content {
    padding: 1.5rem;
  }
  
  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .setting-item {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
    text-align: center;
  }
}

@media (max-width: 480px) {
  .profile-container {
    padding: 0.5rem;
  }
  
  .profile-header {
    padding: 1rem;
  }
  
  .section-header {
    padding: 1rem;
  }
  
  .section-content {
    padding: 1rem;
  }
}

/* Vue transitions */
.slide-enter-active {
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  overflow: hidden;
}

.slide-leave-active {
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  overflow: hidden;
}

.slide-enter-from {
  opacity: 0;
  transform: translateY(-40px);
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}

.slide-enter-to {
  opacity: 1;
  transform: translateY(0);
  max-height: 2000px;
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.slide-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 2000px;
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.slide-leave-to {
  opacity: 0;
  transform: translateY(-30px);
  max-height: 0;
  padding-top: 0;
  padding-bottom: 0;
}

/* Toast Notification */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  animation: slideInRight 0.3s ease-out;
  max-width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.toast.success {
  background: var(--theme-success);
}

.toast.error {
  background: var(--theme-error);
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}
</style> 