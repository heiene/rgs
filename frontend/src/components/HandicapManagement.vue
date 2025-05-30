<template>
  <div class="handicap-management">
    <!-- Header -->
    <div class="management-header">
      <h2>⛳ Handicap Management</h2>
      <div class="header-actions">
        <div class="search-box">
          <input 
            v-model="searchTerm" 
            type="text" 
            placeholder="Search users..."
            @input="debounceSearch"
            class="search-input"
          >
        </div>
        <button @click="showAddHandicapModal = true" class="add-handicap-btn">
          + Add Handicap
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading users...</p>
    </div>

    <!-- Users List -->
    <div v-else-if="users.length > 0" class="users-list">
      <div v-for="user in users" :key="user.id" class="user-card">
        <div class="user-header">
          <div class="user-info">
            <div class="user-avatar">
              {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
            </div>
            <div class="user-details">
              <h3>{{ user.full_name }}</h3>
              <p class="user-email">{{ user.email }}</p>
            </div>
          </div>
          <div class="current-handicap">
            <label>Current Handicap:</label>
            <span v-if="user.current_handicap !== null" class="handicap-value">
              {{ user.current_handicap }}
            </span>
            <span v-else class="no-handicap">No handicap set</span>
          </div>
          <div class="user-actions">
            <button 
              @click="viewHandicapHistory(user)" 
              class="action-btn view"
              title="View Handicap History"
            >
              📊
            </button>
            <button 
              @click="addHandicapForUser(user)" 
              class="action-btn add"
              title="Add New Handicap"
            >
              ➕
            </button>
          </div>
        </div>

        <!-- Handicap History (Expanded) -->
        <div v-if="expandedUser === user.id" class="handicap-history">
          <div class="history-header">
            <h4>Handicap History</h4>
            <button @click="expandedUser = null" class="close-btn">✕</button>
          </div>
          
          <div v-if="userHandicaps[user.id]" class="handicap-list">
            <div 
              v-for="handicap in userHandicaps[user.id]" 
              :key="handicap.id"
              :class="['handicap-item', { current: handicap.is_current }]"
            >
              <div class="handicap-value">{{ handicap.handicap_value }}</div>
              <div class="handicap-dates">
                <div class="start-date">From: {{ formatDate(handicap.start_date) }}</div>
                <div v-if="handicap.end_date" class="end-date">
                  To: {{ formatDate(handicap.end_date) }}
                </div>
                <div v-else class="current-badge">Current</div>
              </div>
              <div class="handicap-reason">
                {{ handicap.reason || 'No reason provided' }}
              </div>
              <div class="handicap-actions">
                <button 
                  @click="editHandicap(handicap)" 
                  class="edit-btn"
                  title="Edit Handicap"
                >
                  ✏️
                </button>
                <button 
                  @click="confirmDeleteHandicap(handicap)"
                  :disabled="userHandicaps[user.id].length <= 1"
                  class="delete-btn"
                  title="Delete Handicap"
                >
                  🗑️
                </button>
              </div>
            </div>
          </div>

          <div v-else class="loading-handicaps">
            <div class="small-spinner"></div>
            <span>Loading handicaps...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">⛳</div>
      <h3>No users found</h3>
      <p>{{ searchTerm ? 'Try adjusting your search criteria' : 'No users match the current filters' }}</p>
    </div>

    <!-- Add/Edit Handicap Modal -->
    <div v-if="showHandicapModal" class="modal-overlay" @click="closeHandicapModal">
      <div class="modal" @click.stop>
        <h3>{{ editingHandicap ? '✏️ Edit Handicap' : '➕ Add Handicap' }}</h3>
        
        <form @submit.prevent="saveHandicap" class="handicap-form">
          <!-- User Selection (only for new handicaps) -->
          <div v-if="!editingHandicap" class="form-group">
            <label>User:</label>
            <select v-model="handicapForm.selectedUserId" required class="form-input">
              <option value="">Select a user...</option>
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.full_name }} ({{ user.email }})
              </option>
            </select>
          </div>

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
            >
          </div>

          <div class="form-group">
            <label>Start Date:</label>
            <input 
              v-model="handicapForm.start_date" 
              type="date" 
              required 
              class="form-input"
            >
          </div>

          <div class="form-group">
            <label>Reason:</label>
            <textarea 
              v-model="handicapForm.reason" 
              placeholder="Reason for handicap change..."
              class="form-input"
              rows="3"
            ></textarea>
          </div>

          <div class="modal-actions">
            <button type="button" @click="closeHandicapModal" class="btn-secondary">Cancel</button>
            <button type="submit" :disabled="savingHandicap" class="btn-primary">
              {{ savingHandicap ? 'Saving...' : 'Save Handicap' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDeleteHandicap">
      <div class="modal" @click.stop>
        <h3>⚠️ Confirm Delete</h3>
        <p>Are you sure you want to delete this handicap entry?</p>
        <p class="warning-text">This action cannot be undone.</p>
        <div class="modal-actions">
          <button @click="cancelDeleteHandicap" class="btn-secondary">Cancel</button>
          <button @click="deleteHandicap" class="btn-danger">Delete Handicap</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useAuthStore } from '../store/auth'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export default {
  name: 'HandicapManagement',
  setup() {
    const authStore = useAuthStore()
    const users = ref([])
    const userHandicaps = reactive({})
    const loading = ref(false)
    const searchTerm = ref('')
    const expandedUser = ref(null)
    const showHandicapModal = ref(false)
    const showAddHandicapModal = ref(false)
    const editingHandicap = ref(null)
    const savingHandicap = ref(false)
    const showDeleteConfirm = ref(false)
    const handicapToDelete = ref(null)

    const handicapForm = reactive({
      selectedUserId: '',
      handicap_value: '',
      start_date: new Date().toISOString().split('T')[0],
      reason: ''
    })

    let searchTimeout = null

    const debounceSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        loadUsers()
      }, 300)
    }

    const loadUsers = async () => {
      loading.value = true
      try {
        const params = {
          per_page: 100 // Load more users for handicap management
        }
        
        if (searchTerm.value.trim()) {
          params.search = searchTerm.value.trim()
        }

        const response = await axios.get(`${API_BASE_URL}/users/`, {
          params,
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          users.value = response.data.data.users
        }
      } catch (error) {
        console.error('Failed to load users:', error)
      } finally {
        loading.value = false
      }
    }

    const viewHandicapHistory = async (user) => {
      if (expandedUser.value === user.id) {
        expandedUser.value = null
        return
      }

      expandedUser.value = user.id

      if (!userHandicaps[user.id]) {
        try {
          const response = await axios.get(`${API_BASE_URL}/handicaps/admin/users/${user.id}/handicaps`, {
            headers: { Authorization: `Bearer ${authStore.token}` }
          })

          if (response.data.success) {
            userHandicaps[user.id] = response.data.data
          }
        } catch (error) {
          console.error('Failed to load handicap history:', error)
        }
      }
    }

    const addHandicapForUser = (user) => {
      handicapForm.selectedUserId = user.id
      showHandicapModal.value = true
    }

    const editHandicap = (handicap) => {
      editingHandicap.value = handicap
      handicapForm.handicap_value = handicap.handicap_value
      handicapForm.start_date = handicap.start_date
      handicapForm.reason = handicap.reason || ''
      showHandicapModal.value = true
    }

    const closeHandicapModal = () => {
      showHandicapModal.value = false
      showAddHandicapModal.value = false
      editingHandicap.value = null
      resetHandicapForm()
    }

    const resetHandicapForm = () => {
      handicapForm.selectedUserId = ''
      handicapForm.handicap_value = ''
      handicapForm.start_date = new Date().toISOString().split('T')[0]
      handicapForm.reason = ''
    }

    const saveHandicap = async () => {
      savingHandicap.value = true
      try {
        if (editingHandicap.value) {
          // Update existing handicap
          const response = await axios.put(`${API_BASE_URL}/handicaps/admin/handicaps/${editingHandicap.value.id}`, {
            handicap_value: handicapForm.handicap_value,
            reason: handicapForm.reason
          }, {
            headers: { Authorization: `Bearer ${authStore.token}` }
          })

          if (response.data.success) {
            // Update local data
            const userId = editingHandicap.value.user_id
            const handicapIndex = userHandicaps[userId].findIndex(h => h.id === editingHandicap.value.id)
            if (handicapIndex !== -1) {
              userHandicaps[userId][handicapIndex] = response.data.data
            }
          }
        } else {
          // Create new handicap
          const response = await axios.post(`${API_BASE_URL}/handicaps/admin/users/${handicapForm.selectedUserId}/handicaps`, {
            handicap_value: handicapForm.handicap_value,
            start_date: handicapForm.start_date,
            reason: handicapForm.reason
          }, {
            headers: { Authorization: `Bearer ${authStore.token}` }
          })

          if (response.data.success) {
            // Refresh user data and handicap history
            await loadUsers()
            if (userHandicaps[handicapForm.selectedUserId]) {
              delete userHandicaps[handicapForm.selectedUserId]
            }
          }
        }

        closeHandicapModal()
      } catch (error) {
        console.error('Failed to save handicap:', error)
      } finally {
        savingHandicap.value = false
      }
    }

    const confirmDeleteHandicap = (handicap) => {
      handicapToDelete.value = handicap
      showDeleteConfirm.value = true
    }

    const cancelDeleteHandicap = () => {
      showDeleteConfirm.value = false
      handicapToDelete.value = null
    }

    const deleteHandicap = async () => {
      if (!handicapToDelete.value) return

      try {
        const response = await axios.delete(`${API_BASE_URL}/handicaps/admin/handicaps/${handicapToDelete.value.id}`, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          // Remove from local data
          const userId = handicapToDelete.value.user_id
          userHandicaps[userId] = userHandicaps[userId].filter(h => h.id !== handicapToDelete.value.id)
        }
      } catch (error) {
        console.error('Failed to delete handicap:', error)
      } finally {
        cancelDeleteHandicap()
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      users,
      userHandicaps,
      loading,
      searchTerm,
      expandedUser,
      showHandicapModal,
      showAddHandicapModal,
      editingHandicap,
      savingHandicap,
      showDeleteConfirm,
      handicapToDelete,
      handicapForm,
      debounceSearch,
      loadUsers,
      viewHandicapHistory,
      addHandicapForUser,
      editHandicap,
      closeHandicapModal,
      saveHandicap,
      confirmDeleteHandicap,
      cancelDeleteHandicap,
      deleteHandicap,
      formatDate
    }
  }
}
</script>

<style scoped>
.handicap-management {
  padding: 2rem;
}

.management-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.management-header h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-input {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  min-width: 250px;
  transition: border-color 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2563eb;
}

.add-handicap-btn {
  padding: 0.75rem 1.5rem;
  background: #059669;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.add-handicap-btn:hover {
  background: #047857;
  transform: translateY(-1px);
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.small-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #e2e8f0;
  border-top: 2px solid #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.users-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  overflow: hidden;
  transition: box-shadow 0.2s ease;
}

.user-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.user-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
  min-width: 200px;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  text-transform: uppercase;
}

.user-details h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #1e293b;
}

.user-email {
  margin: 0.25rem 0 0 0;
  color: #64748b;
  font-size: 0.875rem;
}

.current-handicap {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-width: 120px;
}

.current-handicap label {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 0.25rem;
}

.handicap-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #059669;
}

.no-handicap {
  font-size: 1rem;
  color: #9ca3af;
  font-style: italic;
}

.user-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s ease;
}

.action-btn.view {
  background: #e0e7ff;
  color: #3730a3;
}

.action-btn.add {
  background: #dcfce7;
  color: #166534;
}

.action-btn:hover {
  transform: translateY(-1px);
}

.handicap-history {
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  padding: 1.5rem;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.history-header h4 {
  margin: 0;
  color: #1e293b;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: background 0.2s ease;
}

.close-btn:hover {
  background: #e2e8f0;
}

.handicap-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.handicap-item {
  display: grid;
  grid-template-columns: auto 1fr auto auto;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.handicap-item.current {
  border-color: #059669;
  background: #f0fdf4;
}

.handicap-item .handicap-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #059669;
  min-width: 60px;
}

.handicap-dates {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.start-date, .end-date {
  font-size: 0.875rem;
  color: #64748b;
}

.current-badge {
  background: #059669;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  text-align: center;
}

.handicap-reason {
  color: #374151;
  font-size: 0.875rem;
  max-width: 200px;
}

.handicap-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.edit-btn {
  background: #fef3c7;
  color: #92400e;
}

.delete-btn {
  background: #fecaca;
  color: #dc2626;
}

.delete-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-handicaps {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #64748b;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
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
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h3 {
  margin: 0 0 1.5rem 0;
  color: #1e293b;
}

.handicap-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  border-color: #2563eb;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-secondary, .btn-primary, .btn-danger {
  flex: 1;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary {
  background: #f1f5f9;
  color: #374151;
}

.btn-primary {
  background: #2563eb;
  color: white;
}

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-primary:hover {
  background: #1d4ed8;
}

.btn-danger:hover {
  background: #b91c1c;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.warning-text {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .handicap-management {
    padding: 1rem;
  }
  
  .management-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .header-actions {
    flex-direction: column;
  }
  
  .search-input {
    min-width: auto;
  }
  
  .user-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .handicap-item {
    grid-template-columns: 1fr;
    gap: 0.5rem;
    text-align: center;
  }
  
  .handicap-actions {
    justify-content: center;
  }
}
</style> 