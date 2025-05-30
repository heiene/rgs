<template>
  <div class="user-management">
    <!-- Header with Search and Actions -->
    <div class="management-header">
      <h2>👥 User Management</h2>
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
        <div class="filter-actions">
          <select v-model="statusFilter" @change="loadUsers" class="status-filter">
            <option value="">All Users</option>
            <option value="true">Active Users</option>
            <option value="false">Inactive Users</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading users...</p>
    </div>

    <!-- Users Table -->
    <div v-else-if="users.length > 0" class="users-table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>User</th>
            <th>Email</th>
            <th>Status</th>
            <th>Admin</th>
            <th>Handicap</th>
            <th>Last Login</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" :class="{ inactive: !user.is_active }">
            <td class="user-info">
              <div class="user-avatar">
                {{ user.first_name?.[0] }}{{ user.last_name?.[0] }}
              </div>
              <div class="user-details">
                <div class="user-name">{{ user.full_name }}</div>
                <div class="user-meta">ID: {{ user.id }}</div>
              </div>
            </td>
            <td class="user-email">{{ user.email }}</td>
            <td>
              <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                {{ user.is_active ? '✅ Active' : '❌ Inactive' }}
              </span>
            </td>
            <td>
              <span :class="['admin-badge', user.is_admin ? 'admin' : 'user']">
                {{ user.is_admin ? '👑 Admin' : '👤 User' }}
              </span>
            </td>
            <td class="handicap-cell">
              <span v-if="user.current_handicap !== null" class="handicap-value">
                {{ user.current_handicap }}
              </span>
              <span v-else class="no-handicap">-</span>
            </td>
            <td class="last-login">
              <span v-if="user.last_login">
                {{ formatDate(user.last_login) }}
              </span>
              <span v-else class="never-logged-in">Never</span>
            </td>
            <td class="actions-cell">
              <div class="user-actions">
                <!-- Toggle Active Status -->
                <button 
                  v-if="user.is_active"
                  @click="deactivateUser(user)"
                  class="action-btn deactivate"
                  title="Deactivate User"
                >
                  🚫
                </button>
                <button 
                  v-else
                  @click="activateUser(user)"
                  class="action-btn activate"
                  title="Activate User"
                >
                  ✅
                </button>

                <!-- Toggle Admin Status -->
                <button 
                  @click="toggleAdmin(user)"
                  :disabled="user.id === currentUserId"
                  class="action-btn admin-toggle"
                  :title="user.is_admin ? 'Remove Admin' : 'Make Admin'"
                >
                  {{ user.is_admin ? '👤' : '👑' }}
                </button>

                <!-- Delete User -->
                <button 
                  @click="confirmDeleteUser(user)"
                  :disabled="user.id === currentUserId"
                  class="action-btn delete"
                  title="Delete User"
                >
                  🗑️
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">👥</div>
      <h3>No users found</h3>
      <p>{{ searchTerm ? 'Try adjusting your search criteria' : 'No users match the current filters' }}</p>
    </div>

    <!-- Pagination -->
    <div v-if="meta.pages > 1" class="pagination">
      <button 
        @click="goToPage(meta.page - 1)"
        :disabled="!meta.has_prev"
        class="pagination-btn"
      >
        ← Previous
      </button>
      
      <span class="pagination-info">
        Page {{ meta.page }} of {{ meta.pages }} ({{ meta.total }} users)
      </span>
      
      <button 
        @click="goToPage(meta.page + 1)"
        :disabled="!meta.has_next"
        class="pagination-btn"
      >
        Next →
      </button>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDelete">
      <div class="modal" @click.stop>
        <h3>⚠️ Confirm Delete</h3>
        <p>Are you sure you want to delete <strong>{{ userToDelete?.full_name }}</strong>?</p>
        <p class="warning-text">This action cannot be undone and will remove all user data including rounds and scores.</p>
        <div class="modal-actions">
          <button @click="cancelDelete" class="btn-secondary">Cancel</button>
          <button @click="deleteUser" class="btn-danger">Delete User</button>
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
  name: 'UserManagement',
  setup() {
    const authStore = useAuthStore()
    const users = ref([])
    const loading = ref(false)
    const searchTerm = ref('')
    const statusFilter = ref('')
    const currentPage = ref(1)
    const showDeleteConfirm = ref(false)
    const userToDelete = ref(null)
    
    const meta = reactive({
      total: 0,
      page: 1,
      per_page: 20,
      pages: 1,
      has_prev: false,
      has_next: false
    })

    const currentUserId = computed(() => authStore.user?.id)

    let searchTimeout = null

    const debounceSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        currentPage.value = 1
        loadUsers()
      }, 300)
    }

    const loadUsers = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          per_page: 20
        }
        
        if (searchTerm.value.trim()) {
          params.search = searchTerm.value.trim()
        }
        
        if (statusFilter.value !== '') {
          params.is_active = statusFilter.value
        }

        const response = await axios.get(`${API_BASE_URL}/users/`, {
          params,
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          users.value = response.data.data.users
          Object.assign(meta, response.data.data.meta)
        }
      } catch (error) {
        console.error('Failed to load users:', error)
        // Handle error state
      } finally {
        loading.value = false
      }
    }

    const goToPage = (page) => {
      currentPage.value = page
      loadUsers()
    }

    const activateUser = async (user) => {
      try {
        const response = await axios.post(`${API_BASE_URL}/users/${user.id}/activate`, {}, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          user.is_active = true
        }
      } catch (error) {
        console.error('Failed to activate user:', error)
      }
    }

    const deactivateUser = async (user) => {
      try {
        const response = await axios.post(`${API_BASE_URL}/users/${user.id}/deactivate`, {}, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          user.is_active = false
        }
      } catch (error) {
        console.error('Failed to deactivate user:', error)
      }
    }

    const toggleAdmin = async (user) => {
      if (user.id === currentUserId.value) return

      try {
        const response = await axios.post(`${API_BASE_URL}/users/${user.id}/toggle-admin`, {}, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          user.is_admin = response.data.data.is_admin
        }
      } catch (error) {
        console.error('Failed to toggle admin status:', error)
      }
    }

    const confirmDeleteUser = (user) => {
      if (user.id === currentUserId.value) return
      userToDelete.value = user
      showDeleteConfirm.value = true
    }

    const cancelDelete = () => {
      showDeleteConfirm.value = false
      userToDelete.value = null
    }

    const deleteUser = async () => {
      if (!userToDelete.value) return

      try {
        const response = await axios.delete(`${API_BASE_URL}/users/${userToDelete.value.id}`, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          users.value = users.value.filter(u => u.id !== userToDelete.value.id)
        }
      } catch (error) {
        console.error('Failed to delete user:', error)
      } finally {
        cancelDelete()
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    onMounted(() => {
      loadUsers()
    })

    return {
      users,
      loading,
      searchTerm,
      statusFilter,
      meta,
      currentUserId,
      showDeleteConfirm,
      userToDelete,
      debounceSearch,
      loadUsers,
      goToPage,
      activateUser,
      deactivateUser,
      toggleAdmin,
      confirmDeleteUser,
      cancelDelete,
      deleteUser,
      formatDate
    }
  }
}
</script>

<style scoped>
.user-management {
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

.search-input, .status-filter {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.search-input:focus, .status-filter:focus {
  outline: none;
  border-color: #2563eb;
}

.search-input {
  min-width: 250px;
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

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.users-table-container {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
}

.users-table th {
  background: #f8fafc;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #1e293b;
  border-bottom: 2px solid #e2e8f0;
}

.users-table td {
  padding: 1rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.users-table tr.inactive {
  opacity: 0.6;
  background: #f8fafc;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  text-transform: uppercase;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
}

.user-meta {
  font-size: 0.875rem;
  color: #64748b;
}

.user-email {
  color: #374151;
  font-family: monospace;
}

.status-badge, .admin-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.active {
  background: #dcfce7;
  color: #166534;
}

.status-badge.inactive {
  background: #fee2e2;
  color: #991b1b;
}

.admin-badge.admin {
  background: #fef3c7;
  color: #92400e;
}

.admin-badge.user {
  background: #e0e7ff;
  color: #3730a3;
}

.handicap-value {
  font-weight: 600;
  color: #059669;
}

.no-handicap {
  color: #9ca3af;
}

.never-logged-in {
  color: #9ca3af;
  font-style: italic;
}

.user-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-1px);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.activate {
  background: #dcfce7;
  color: #166534;
}

.action-btn.deactivate {
  background: #fee2e2;
  color: #991b1b;
}

.action-btn.admin-toggle {
  background: #fef3c7;
  color: #92400e;
}

.action-btn.delete {
  background: #fecaca;
  color: #dc2626;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
}

.pagination-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e2e8f0;
  background: white;
  color: #374151;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  color: #64748b;
  font-weight: 500;
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
  max-width: 400px;
  width: 90%;
}

.modal h3 {
  margin: 0 0 1rem 0;
  color: #dc2626;
}

.warning-text {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-secondary, .btn-danger {
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

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-danger:hover {
  background: #b91c1c;
}

@media (max-width: 768px) {
  .user-management {
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
  
  .users-table {
    font-size: 0.875rem;
  }
  
  .users-table th, .users-table td {
    padding: 0.75rem 0.5rem;
  }
  
  .user-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 0.875rem;
  }
}
</style> 