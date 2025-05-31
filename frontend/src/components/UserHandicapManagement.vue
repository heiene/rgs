<template>
  <div class="user-handicap-management">
    <!-- Header -->
    <div class="header">
      <h2>⛳ My Handicap</h2>
      <div class="current-handicap-display">
        <span v-if="currentHandicap" class="handicap-value">{{ currentHandicap.handicap_value }}</span>
        <span v-else class="no-handicap">Not Set</span>
      </div>
    </div>

    <!-- Current Handicap Card -->
    <div class="current-handicap-card">
      <div class="card-header">
        <h3>Current Handicap</h3>
        <div class="actions">
          <button 
            @click="showHandicapModal = true" 
            class="btn-primary"
          >
            {{ currentHandicap ? 'Update Handicap' : 'Set Initial Handicap' }}
          </button>
        </div>
      </div>

      <div v-if="currentHandicap" class="handicap-details">
        <div class="detail-item">
          <label>Handicap Value:</label>
          <span class="value">{{ currentHandicap.handicap_value }}</span>
        </div>
        <div class="detail-item">
          <label>Valid Since:</label>
          <span class="value">{{ formatDate(currentHandicap.start_date) }}</span>
        </div>
        <div class="detail-item">
          <label>Days Active:</label>
          <span class="value">{{ currentHandicap.days_active }} days</span>
        </div>
        <div v-if="currentHandicap.reason" class="detail-item">
          <label>Reason:</label>
          <span class="value">{{ currentHandicap.reason }}</span>
        </div>
      </div>

      <div v-else class="no-handicap-state">
        <div class="no-handicap-icon">⛳</div>
        <h4>No Handicap Set</h4>
        <p>Set your initial handicap to start tracking your golf progress.</p>
      </div>
    </div>

    <!-- Handicap History -->
    <div class="handicap-history">
      <div class="history-header" @click="toggleHistoryExpanded">
        <h3>📊 Handicap History</h3>
        <div class="header-actions">
          <button @click.stop="loadHandicapHistory" class="refresh-btn" title="Refresh">
            🔄
          </button>
          <span class="expand-icon" :class="{ expanded: isHistoryExpanded }">▼</span>
        </div>
      </div>

      <div class="history-content" :class="{ expanded: isHistoryExpanded }">
        <div class="history-content-inner">
          <div v-if="loadingHistory" class="loading-state">
            <div class="spinner"></div>
            <p>Loading history...</p>
          </div>

          <div v-else-if="handicapHistory.length > 0" class="history-list">
            <div 
              v-for="handicap in handicapHistory" 
              :key="handicap.id"
              :class="['history-item', { current: handicap.is_current }]"
            >
              <div class="handicap-value">{{ handicap.handicap_value }}</div>
              <div class="handicap-period">
                <div class="period-dates">
                  {{ formatDate(handicap.start_date) }}
                  <span v-if="handicap.end_date"> - {{ formatDate(handicap.end_date) }}</span>
                  <span v-else class="current-indicator"> - Current</span>
                </div>
                <div class="period-duration">{{ handicap.days_active }} days</div>
              </div>
              <div class="handicap-reason">
                {{ handicap.reason || 'No reason provided' }}
              </div>
            </div>
          </div>

          <div v-else class="empty-history">
            <div class="empty-icon">📈</div>
            <h4>No History Available</h4>
            <p>Your handicap history will appear here as you update your handicap.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Set/Update Handicap Modal -->
    <div v-if="showHandicapModal" class="modal-overlay" @click="closeHandicapModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>⛳ Set/Update Handicap</h3>
          <button class="modal-close" @click="closeHandicapModal">&times;</button>
        </div>
        <p class="modal-description">
          Enter your current handicap index. This will be used as your starting point for tracking improvements.
        </p>
        
        <form @submit.prevent="setHandicap" class="handicap-form">
          <div class="form-group">
            <label>Handicap Value:</label>
            <input 
              v-model.number="handicapForm.handicap_value" 
              type="number" 
              step="0.1" 
              min="-5" 
              max="54" 
              required 
              class="form-input"
              placeholder="e.g., 15.4"
            >
            <small class="form-help">Enter a value between -5 and 54</small>
          </div>

          <div class="form-group">
            <label>Effective Date:</label>
            <input 
              v-model="handicapForm.start_date" 
              type="date" 
              required 
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label>Reason for Change (Optional):</label>
            <textarea 
              v-model="handicapForm.reason" 
              placeholder="e.g., Recent tournament results, improved short game (leave blank for default)"
              class="form-input"
              rows="3"
            ></textarea>
            <small class="form-help">If left blank, will default to 'Handicap updated by [Your Name]'</small>
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeHandicapModal" class="btn-secondary">Cancel</button>
            <button type="submit" :disabled="settingHandicap" class="btn-primary">
              {{ settingHandicap ? 'Setting...' : 'Set/Update Handicap' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../store/auth'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export default {
  name: 'UserHandicapManagement',
  setup() {
    const authStore = useAuthStore()
    const currentHandicap = ref(null)
    const handicapHistory = ref([])
    const loadingHistory = ref(false)
    const showHandicapModal = ref(false)
    const settingHandicap = ref(false)
    const isHistoryExpanded = ref(false)

    const handicapForm = reactive({
      handicap_value: '',
      start_date: new Date().toISOString().split('T')[0],
      reason: ''
    })

    const loadCurrentHandicap = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/handicaps/my-handicaps/current`, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          currentHandicap.value = response.data.data
        }
      } catch (error) {
        if (error.response?.status !== 404) {
          console.error('Failed to load current handicap:', error)
        }
      }
    }

    const loadHandicapHistory = async () => {
      loadingHistory.value = true
      try {
        const response = await axios.get(`${API_BASE_URL}/handicaps/my-handicaps`, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          handicapHistory.value = response.data.data
        }
      } catch (error) {
        console.error('Failed to load handicap history:', error)
      } finally {
        loadingHistory.value = false
      }
    }

    const setHandicap = async () => {
      settingHandicap.value = true
      try {
        const payload = {
          user_id: parseInt(authStore.currentUser?.id),
          handicap_value: parseFloat(handicapForm.handicap_value),
          start_date: handicapForm.start_date,
          reason: handicapForm.reason,
          created_by_id: parseInt(authStore.currentUser?.id)
        }

        console.log('Sending handicap payload:', payload)

        const response = await axios.post(`${API_BASE_URL}/handicaps/my-handicaps`, payload, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          currentHandicap.value = response.data.data
          closeHandicapModal()
          loadHandicapHistory()
        }
      } catch (error) {
        console.error('Failed to set handicap:', error)
        console.error('Error response:', error.response?.data)
        
        let errorMessage = 'Failed to set handicap'
        if (error.response?.data?.details) {
          // Handle validation errors
          const details = error.response.data.details
          const fieldErrors = Object.entries(details).map(([field, errors]) => 
            `${field}: ${Array.isArray(errors) ? errors.join(', ') : errors}`
          ).join('; ')
          errorMessage = `Validation errors: ${fieldErrors}`
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        }
        
        alert(errorMessage) // Temporary - you could add a proper notification system
      } finally {
        settingHandicap.value = false
      }
    }

    const closeHandicapModal = () => {
      showHandicapModal.value = false
      handicapForm.handicap_value = ''
      handicapForm.start_date = new Date().toISOString().split('T')[0]
      handicapForm.reason = ''
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }

    const toggleHistoryExpanded = () => {
      isHistoryExpanded.value = !isHistoryExpanded.value
    }

    onMounted(() => {
      loadCurrentHandicap()
      loadHandicapHistory()
    })

    return {
      currentHandicap,
      handicapHistory,
      loadingHistory,
      showHandicapModal,
      settingHandicap,
      handicapForm,
      loadHandicapHistory,
      setHandicap,
      closeHandicapModal,
      formatDate,
      isHistoryExpanded,
      toggleHistoryExpanded
    }
  }
}
</script>

<style scoped>
.user-handicap-management {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.current-handicap-display {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--theme-primary) 0%, var(--theme-primary-dark) 100%);
  color: white;
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
}

.current-handicap-display .handicap-value {
  font-size: 2.5rem;
  font-weight: 800;
}

.current-handicap-display .no-handicap {
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  opacity: 0.8;
}

.current-handicap-card {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f1f5f9;
  background: #f8fafc;
}

.card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1e293b;
}

.handicap-details {
  padding: 2rem;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-item .value {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
}

.no-handicap-state {
  padding: 3rem 2rem;
  text-align: center;
}

.no-handicap-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-handicap-state h4 {
  margin: 0 0 0.5rem 0;
  color: #64748b;
}

.no-handicap-state p {
  margin: 0;
  color: #9ca3af;
}

.handicap-history {
  background: white;
  border-radius: 16px;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #f1f5f9;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.2s ease;
}

.history-header:hover {
  background: #f1f5f9;
}

.history-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1e293b;
  user-select: none;
}

.refresh-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.refresh-btn:hover {
  background: #e2e8f0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.expand-icon {
  transition: transform 0.2s ease;
  user-select: none;
  color: #64748b;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.history-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
  background: white;
}

.history-content.expanded {
  max-height: 1000px;
}

.history-content-inner {
  padding: 1.5rem 2rem;
}

.loading-state {
  text-align: center;
  padding: 3rem 2rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid var(--theme-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-item {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1.5rem;
  align-items: center;
  padding: 1.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.history-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.history-item.current {
  background: #eff6ff;
  border-color: var(--theme-primary);
}

.history-item .handicap-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--theme-primary);
  min-width: 80px;
}

.handicap-period {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.period-dates {
  font-weight: 500;
  color: #374151;
}

.current-indicator {
  color: var(--theme-primary);
  font-weight: 600;
}

.period-duration {
  font-size: 0.875rem;
  color: #64748b;
}

.handicap-reason {
  font-size: 0.875rem;
  color: #64748b;
  text-align: right;
  max-width: 200px;
}

.empty-history {
  padding: 3rem 2rem;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-history h4 {
  margin: 0 0 0.5rem 0;
  color: #64748b;
}

.empty-history p {
  margin: 0;
  color: #9ca3af;
}

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--theme-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--theme-primary-dark);
  transform: translateY(-1px);
}

.btn-secondary {
  background: #f1f5f9;
  color: #374151;
  border: 2px solid #e2e8f0;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 0;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close:hover {
  background: #e2e8f0;
  color: #374151;
}

.modal-description {
  margin: 0 0 2rem 0;
  color: #64748b;
  line-height: 1.6;
  padding: 0 2rem;
}

.handicap-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 0 2rem 2rem;
  overflow-y: auto;
  flex: 1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--theme-primary);
}

.form-help {
  font-size: 0.875rem;
  color: #64748b;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 768px) {
  .user-handicap-management {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    text-align: center;
  }
  
  .current-handicap-display {
    min-width: 100px;
    height: 100px;
  }
  
  .current-handicap-display .handicap-value {
    font-size: 2rem;
  }
  
  .card-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .handicap-details {
    grid-template-columns: 1fr;
    padding: 1.5rem;
  }
  
  .history-item {
    grid-template-columns: 1fr;
    gap: 1rem;
    text-align: center;
  }
  
  .handicap-reason {
    text-align: center;
    max-width: none;
  }
}
</style>