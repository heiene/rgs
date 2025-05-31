<template>
  <AppLayout>
    <div class="admin-user-management">
      <!-- Header -->
      <div class="page-header">
        <div class="header-content">
          <h1 class="page-title">👥 User Management</h1>
          <p class="page-subtitle">Manage user accounts, permissions, and handicap history</p>
        </div>
        <div class="header-actions">
          <button @click="refreshUsers" class="btn-secondary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23,4 23,10 17,10"></polyline>
              <polyline points="1,20 1,14 7,14"></polyline>
              <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
            </svg>
            Refresh
          </button>
        </div>
      </div>

      <!-- Search and Filters -->
      <div class="filters-section">
        <div class="search-box">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"></circle>
            <path d="M21 21l-4.35-4.35"></path>
          </svg>
          <input 
            v-model="searchTerm" 
            type="text" 
            placeholder="Search users by name or email (case-insensitive)..."
            @input="debounceSearch"
            class="search-input"
          >
        </div>
        <div class="filter-controls">
          <select v-model="statusFilter" @change="loadUsers" class="filter-select">
            <option value="">All Status</option>
            <option value="true">Active Users</option>
            <option value="false">Inactive Users</option>
          </select>
          <select v-model="adminFilter" @change="loadUsers" class="filter-select">
            <option value="">All Roles</option>
            <option value="true">Admins Only</option>
            <option value="false">Regular Users</option>
          </select>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading users...</p>
      </div>

      <!-- Users Table -->
      <div v-else-if="users.length > 0" class="users-section">
        <div class="table-container">
          <table class="users-table">
            <thead>
              <tr>
                <th>User</th>
                <th>Email</th>
                <th>Status</th>
                <th>Role</th>
                <th>Handicap</th>
                <th>Club</th>
                <th>Last Login</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" :class="{ inactive: !user.is_active }">
                <td>
                  <div class="user-info">
                    <div class="user-avatar">
                      {{ getUserInitials(user) }}
                    </div>
                    <div class="user-details">
                      <div class="user-name">{{ user.full_name || `${user.first_name} ${user.last_name}` }}</div>
                      <div class="user-id">ID: {{ user.id }}</div>
                    </div>
                  </div>
                </td>
                <td class="user-email">{{ user.email }}</td>
                <td>
                  <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                    {{ user.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <span :class="['role-badge', user.is_admin ? 'admin' : 'user']">
                    {{ user.is_admin ? 'Admin' : 'User' }}
                  </span>
                </td>
                <td>
                  <span v-if="user.current_handicap !== null" class="handicap-value">
                    {{ user.current_handicap }}
                  </span>
                  <span v-else class="no-handicap">No HCP</span>
                </td>
                <td class="club-cell">
                  <span v-if="user.home_club_id" class="club-name">
                    Club {{ user.home_club_id }}
                  </span>
                  <span v-else class="no-club">No Club</span>
                </td>
                <td>
                  <span v-if="user.last_login" class="last-login">
                    {{ formatDate(user.last_login) }}
                  </span>
                  <span v-else class="never-logged">Never</span>
                </td>
                <td>
                  <div class="user-actions">
                    <div class="action-item">
                      <button 
                        @click="viewUserHandicaps(user)"
                        @mouseenter="showTooltip(`handicaps-${user.id}`)"
                        @mouseleave="hideTooltip"
                        @touchstart="toggleTooltip(`handicaps-${user.id}`)"
                        class="action-btn view-handicaps"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
                        </svg>
                      </button>
                      <div v-if="activeTooltip === `handicaps-${user.id}`" class="tooltip">
                        View Handicap History
                      </div>
                    </div>
                    
                    <div class="action-item">
                      <button 
                        @click="editUser(user)"
                        @mouseenter="showTooltip(`edit-${user.id}`)"
                        @mouseleave="hideTooltip"
                        @touchstart="toggleTooltip(`edit-${user.id}`)"
                        class="action-btn edit"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                      </button>
                      <div v-if="activeTooltip === `edit-${user.id}`" class="tooltip">
                        Edit User Details
                      </div>
                    </div>

                    <div class="action-item">
                      <button 
                        v-if="user.is_active"
                        @click="toggleUserStatus(user, false)"
                        @mouseenter="showTooltip(`deactivate-${user.id}`)"
                        @mouseleave="hideTooltip"
                        @touchstart="toggleTooltip(`deactivate-${user.id}`)"
                        class="action-btn deactivate"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="10"></circle>
                          <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>
                        </svg>
                      </button>
                      <button 
                        v-else
                        @click="toggleUserStatus(user, true)"
                        @mouseenter="showTooltip(`activate-${user.id}`)"
                        @mouseleave="hideTooltip"
                        @touchstart="toggleTooltip(`activate-${user.id}`)"
                        class="action-btn activate"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                          <polyline points="22,4 12,14.01 9,11.01"></polyline>
                        </svg>
                      </button>
                      <div v-if="activeTooltip === `deactivate-${user.id}`" class="tooltip">
                        Deactivate User Account
                      </div>
                      <div v-if="activeTooltip === `activate-${user.id}`" class="tooltip">
                        Activate User Account
                      </div>
                    </div>

                    <div class="action-item">
                      <button 
                        @click="toggleAdminStatus(user)"
                        @mouseenter="showTooltip(`admin-${user.id}`)"
                        @mouseleave="hideTooltip"
                        @touchstart="toggleTooltip(`admin-${user.id}`)"
                        :disabled="user.id === currentUserId"
                        class="action-btn admin-toggle"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <circle cx="12" cy="12" r="3"></circle>
                          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
                        </svg>
                      </button>
                      <div v-if="activeTooltip === `admin-${user.id}`" class="tooltip">
                        {{ user.id === currentUserId ? 'Cannot modify own admin status' : (user.is_admin ? 'Remove Admin Privileges' : 'Grant Admin Privileges') }}
                      </div>
                    </div>

                    <div class="action-item">
                      <button 
                        @click="confirmDeleteUser(user)"
                        @mouseenter="showTooltip(`delete-${user.id}`)"
                        @mouseleave="hideTooltip"
                        @touchstart="toggleTooltip(`delete-${user.id}`)"
                        :disabled="user.id === currentUserId"
                        class="action-btn delete"
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <polyline points="3,6 5,6 21,6"></polyline>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                      </button>
                      <div v-if="activeTooltip === `delete-${user.id}`" class="tooltip">
                        {{ user.id === currentUserId ? 'Cannot delete own account' : 'Delete User Account' }}
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
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
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </div>
        <h3>No users found</h3>
        <p>{{ searchTerm ? 'Try adjusting your search criteria' : 'No users match the current filters' }}</p>
      </div>

      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteConfirm" class="modal-overlay" @click="cancelDelete">
        <div class="modal" @click.stop>
          <div class="modal-header">
            <h3>⚠️ Confirm User Deletion</h3>
          </div>
          <div class="modal-content">
            <p>Are you sure you want to delete <strong>{{ userToDelete?.full_name || `${userToDelete?.first_name} ${userToDelete?.last_name}` }}</strong>?</p>
            <div class="warning-box">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              <div>
                <strong>This action cannot be undone!</strong>
                <p>All user data including rounds, scores, and handicap history will be permanently deleted.</p>
              </div>
            </div>
          </div>
          <div class="modal-actions">
            <button @click="cancelDelete" class="btn-secondary">Cancel</button>
            <button @click="deleteUser" class="btn-danger">Delete User</button>
          </div>
        </div>
      </div>

      <!-- Edit User Modal -->
      <div v-if="showEditModal" class="modal-overlay" @click="cancelEdit">
        <div class="modal edit-modal" @click.stop>
          <div class="modal-header">
            <h3>✏️ Edit User</h3>
            <button @click="cancelEdit" class="close-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-content">
            <form @submit.prevent="updateUser" class="edit-form">
              <div class="form-row">
                <div class="form-group">
                  <label>First Name</label>
                  <input v-model="editForm.first_name" type="text" required>
                </div>
                <div class="form-group">
                  <label>Last Name</label>
                  <input v-model="editForm.last_name" type="text" required>
                </div>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="editForm.email" type="email" required>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Gender</label>
                  <select v-model="editForm.sex">
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Distance Unit</label>
                  <select v-model="editForm.distance_unit">
                    <option value="meters">Meters</option>
                    <option value="yards">Yards</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>Country</label>
                <input v-model="editForm.country" type="text">
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>City</label>
                  <input v-model="editForm.city" type="text">
                </div>
                <div class="form-group">
                  <label>Postal Code</label>
                  <input v-model="editForm.postal_code" type="text">
                </div>
              </div>
              <div class="form-group">
                <label>Address</label>
                <input v-model="editForm.address" type="text">
              </div>
            </form>
          </div>
          <div class="modal-actions">
            <button @click="cancelEdit" class="btn-secondary">Cancel</button>
            <button @click="updateUser" class="btn-primary" :disabled="updatingUser">
              {{ updatingUser ? 'Updating...' : 'Update User' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Handicap History Modal -->
      <div v-if="showHandicapModal" class="modal-overlay" @click="closeHandicapModal">
        <div class="modal handicap-modal" @click.stop>
          <div class="modal-header">
            <h3>🏌️ Handicap Management - {{ selectedUser?.full_name || `${selectedUser?.first_name} ${selectedUser?.last_name}` }}</h3>
            <button @click="closeHandicapModal" class="close-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-content">
            <!-- Add New Handicap Button -->
            <div class="handicap-actions">
              <button @click="showAddHandicapForm" class="btn-primary add-handicap-btn">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                Add New Handicap
              </button>
            </div>

            <!-- Add/Edit Handicap Form -->
            <div v-if="showHandicapForm" class="handicap-form">
              <h4>{{ editingHandicap ? 'Edit Handicap' : 'Add New Handicap' }}</h4>
              <form @submit.prevent="saveHandicap" class="handicap-form-fields">
                <div class="form-row">
                  <div class="form-group">
                    <label>Handicap Value</label>
                    <input 
                      v-model="handicapForm.handicap_value" 
                      type="number" 
                      step="0.1" 
                      min="0" 
                      max="54" 
                      required
                      placeholder="e.g. 18.5"
                    >
                  </div>
                  <div class="form-group">
                    <label>Start Date</label>
                    <input 
                      v-model="handicapForm.start_date" 
                      type="date" 
                      required
                    >
                  </div>
                </div>
                <div class="form-group">
                  <label>Reason (Optional)</label>
                  <input 
                    v-model="handicapForm.reason" 
                    type="text" 
                    placeholder="Reason for handicap change..."
                  >
                </div>
                <div class="form-actions">
                  <button type="button" @click="cancelHandicapForm" class="btn-secondary">Cancel</button>
                  <button type="submit" :disabled="savingHandicap" class="btn-primary">
                    {{ savingHandicap ? 'Saving...' : (editingHandicap ? 'Update' : 'Add') }}
                  </button>
                </div>
              </form>
            </div>

            <!-- Handicap History -->
            <div v-if="loadingHandicaps" class="loading-state">
              <div class="spinner"></div>
              <p>Loading handicap history...</p>
            </div>
            <div v-else-if="handicapHistory.length > 0" class="handicap-list">
              <h4>Handicap History</h4>
              <div v-for="handicap in handicapHistory" :key="handicap.id" class="handicap-item">
                <div class="handicap-value">{{ handicap.handicap_value }}</div>
                <div class="handicap-details">
                  <div class="handicap-period">
                    {{ formatDate(handicap.start_date) }}
                    <span v-if="handicap.end_date"> - {{ formatDate(handicap.end_date) }}</span>
                    <span v-else class="current"> (Current)</span>
                  </div>
                  <div class="handicap-reason">{{ handicap.reason || 'No reason provided' }}</div>
                </div>
                <div class="handicap-item-actions">
                  <button @click="editHandicap(handicap)" class="action-btn edit" title="Edit Handicap">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <div v-else class="empty-handicaps">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M22 12h-4l-3 9L9 3l-3 9H2"></path>
              </svg>
              <p>No handicap history found for this user.</p>
              <button @click="showAddHandicapForm" class="btn-primary">Add First Handicap</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import AppLayout from '@/components/AppLayout.vue'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export default {
  name: 'AdminUserManagement',
  components: {
    AppLayout
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    // State
    const users = ref([])
    const loading = ref(false)
    const searchTerm = ref('')
    const statusFilter = ref('')
    const adminFilter = ref('')
    const currentPage = ref(1)
    
    // Modals
    const showDeleteConfirm = ref(false)
    const showEditModal = ref(false)
    const showHandicapModal = ref(false)
    const userToDelete = ref(null)
    const selectedUser = ref(null)
    const updatingUser = ref(false)
    
    // Tooltip state
    const activeTooltip = ref(null)
    const tooltipTimeout = ref(null)
    
    // Handicap management
    const handicapHistory = ref([])
    const loadingHandicaps = ref(false)
    const showHandicapForm = ref(false)
    const editingHandicap = ref(null)
    const savingHandicap = ref(false)
    
    // Handicap form
    const handicapForm = reactive({
      handicap_value: '',
      start_date: new Date().toISOString().split('T')[0],
      reason: ''
    })
    
    // Edit form
    const editForm = reactive({
      id: null,
      first_name: '',
      last_name: '',
      email: '',
      sex: 'M',
      distance_unit: 'yards',
      country: '',
      city: '',
      postal_code: '',
      address: ''
    })
    
    // Pagination metadata
    const meta = reactive({
      total: 0,
      page: 1,
      per_page: 20,
      pages: 1,
      has_prev: false,
      has_next: false
    })

    const currentUserId = computed(() => authStore.currentUser?.id)

    // Check admin access
    onMounted(() => {
      if (!authStore.currentUser?.is_admin) {
        router.push('/dashboard')
        return
      }
      loadUsers()
      
      // Add global click handler to hide tooltips on mobile
      document.addEventListener('click', (event) => {
        // Check if click is outside any action button
        if (!event.target.closest('.action-item')) {
          activeTooltip.value = null
        }
      })
    })

    // Search debouncing
    let searchTimeout = null
    const debounceSearch = () => {
      clearTimeout(searchTimeout)
      searchTimeout = setTimeout(() => {
        currentPage.value = 1
        loadUsers()
      }, 300)
    }

    // User management functions
    const loadUsers = async () => {
      loading.value = true
      try {
        const params = {
          page: currentPage.value,
          per_page: 20
        }
        
        if (searchTerm.value.trim()) {
          // Make search case-insensitive by converting to lowercase
          params.search = searchTerm.value.trim().toLowerCase()
        }
        
        if (statusFilter.value !== '') {
          params.is_active = statusFilter.value
        }

        if (adminFilter.value !== '') {
          params.is_admin = adminFilter.value
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

    const refreshUsers = () => {
      searchTerm.value = ''
      statusFilter.value = ''
      adminFilter.value = ''
      currentPage.value = 1
      loadUsers()
    }

    const goToPage = (page) => {
      currentPage.value = page
      loadUsers()
    }

    const getUserInitials = (user) => {
      const first = user.first_name?.[0] || ''
      const last = user.last_name?.[0] || ''
      return `${first}${last}`.toUpperCase()
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

    // User status management
    const toggleUserStatus = async (user, activate) => {
      try {
        const endpoint = activate ? 'activate' : 'deactivate'
        const response = await axios.post(`${API_BASE_URL}/users/${user.id}/${endpoint}`, {}, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          user.is_active = activate
        }
      } catch (error) {
        console.error(`Failed to ${activate ? 'activate' : 'deactivate'} user:`, error)
      }
    }

    const toggleAdminStatus = async (user) => {
      if (user.id === currentUserId.value) return

      try {
        const response = await axios.post(`${API_BASE_URL}/users/${user.id}/toggle-admin`, {}, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          user.is_admin = response.data.data.is_admin
          
          // Show notification if admin permissions were changed
          if (response.data.action_required === 'token_refresh') {
            const userName = user.full_name || `${user.first_name} ${user.last_name}`
            const action = user.is_admin ? 'granted' : 'revoked'
            alert(`Admin privileges ${action} for ${userName}. They will need to refresh their session to see changes.`)
          }
        }
      } catch (error) {
        console.error('Failed to toggle admin status:', error)
      }
    }

    // User deletion
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
          meta.total--
        }
      } catch (error) {
        console.error('Failed to delete user:', error)
      } finally {
        cancelDelete()
      }
    }

    // User editing
    const editUser = (user) => {
      Object.assign(editForm, {
        id: user.id,
        first_name: user.first_name,
        last_name: user.last_name,
        email: user.email,
        sex: user.sex || 'M',
        distance_unit: user.distance_unit || 'yards',
        country: user.country || '',
        city: user.city || '',
        postal_code: user.postal_code || '',
        address: user.address || ''
      })
      showEditModal.value = true
    }

    const cancelEdit = () => {
      showEditModal.value = false
      Object.keys(editForm).forEach(key => {
        if (key !== 'sex' && key !== 'distance_unit') {
          editForm[key] = ''
        }
      })
    }

    const updateUser = async () => {
      if (!editForm.id) return

      updatingUser.value = true
      try {
        const updateData = { ...editForm }
        delete updateData.id

        const response = await axios.put(`${API_BASE_URL}/users/${editForm.id}`, updateData, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          // Update user in the list
          const userIndex = users.value.findIndex(u => u.id === editForm.id)
          if (userIndex !== -1) {
            Object.assign(users.value[userIndex], response.data.data)
          }
          cancelEdit()
        }
      } catch (error) {
        console.error('Failed to update user:', error)
      } finally {
        updatingUser.value = false
      }
    }

    // Handicap management
    const viewUserHandicaps = async (user) => {
      selectedUser.value = user
      showHandicapModal.value = true
      loadingHandicaps.value = true
      
      try {
        const response = await axios.get(`${API_BASE_URL}/handicaps/user/${user.id}`, {
          headers: { Authorization: `Bearer ${authStore.token}` }
        })

        if (response.data.success) {
          handicapHistory.value = response.data.data
        }
      } catch (error) {
        console.error('Failed to load handicap history:', error)
        handicapHistory.value = []
      } finally {
        loadingHandicaps.value = false
      }
    }

    const closeHandicapModal = () => {
      showHandicapModal.value = false
      selectedUser.value = null
      handicapHistory.value = []
      showHandicapForm.value = false
      editingHandicap.value = null
      resetHandicapForm()
    }

    // Handicap form management
    const showAddHandicapForm = () => {
      editingHandicap.value = null
      resetHandicapForm()
      showHandicapForm.value = true
    }

    const editHandicap = (handicap) => {
      editingHandicap.value = handicap
      handicapForm.handicap_value = handicap.handicap_value
      handicapForm.start_date = handicap.start_date
      handicapForm.reason = handicap.reason || ''
      showHandicapForm.value = true
    }

    const cancelHandicapForm = () => {
      showHandicapForm.value = false
      editingHandicap.value = null
      resetHandicapForm()
    }

    const resetHandicapForm = () => {
      handicapForm.handicap_value = ''
      handicapForm.start_date = new Date().toISOString().split('T')[0]
      handicapForm.reason = ''
    }

    const saveHandicap = async () => {
      if (!selectedUser.value) return

      savingHandicap.value = true
      try {
        if (editingHandicap.value) {
          // Update existing handicap
          const response = await axios.put(`${API_BASE_URL}/handicaps/admin/handicaps/${editingHandicap.value.id}`, {
            handicap_value: parseFloat(handicapForm.handicap_value),
            reason: handicapForm.reason
          }, {
            headers: { Authorization: `Bearer ${authStore.token}` }
          })

          if (response.data.success) {
            // Update local data
            const handicapIndex = handicapHistory.value.findIndex(h => h.id === editingHandicap.value.id)
            if (handicapIndex !== -1) {
              handicapHistory.value[handicapIndex] = response.data.data
            }
          }
        } else {
          // Create new handicap
          const response = await axios.post(`${API_BASE_URL}/handicaps/admin/users/${selectedUser.value.id}/handicaps`, {
            handicap_value: parseFloat(handicapForm.handicap_value),
            start_date: handicapForm.start_date,
            reason: handicapForm.reason
          }, {
            headers: { Authorization: `Bearer ${authStore.token}` }
          })

          if (response.data.success) {
            // Reload handicap history
            await viewUserHandicaps(selectedUser.value)
            // Update user in main list
            const userIndex = users.value.findIndex(u => u.id === selectedUser.value.id)
            if (userIndex !== -1) {
              users.value[userIndex].current_handicap = response.data.data.handicap_value
            }
          }
        }

        cancelHandicapForm()
      } catch (error) {
        console.error('Failed to save handicap:', error)
        
        // Provide more specific error feedback
        let errorMessage = 'Failed to save handicap. Please try again.'
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
        
        alert(errorMessage)
      } finally {
        savingHandicap.value = false
      }
    }

    // Tooltip methods
    const showTooltip = (tooltipId) => {
      // Clear any existing timeout
      if (tooltipTimeout.value) {
        clearTimeout(tooltipTimeout.value)
      }
      activeTooltip.value = tooltipId
    }

    const hideTooltip = () => {
      // Add slight delay for better UX
      tooltipTimeout.value = setTimeout(() => {
        activeTooltip.value = null
      }, 150)
    }

    const toggleTooltip = (tooltipId) => {
      // For mobile - toggle tooltip on tap
      if (activeTooltip.value === tooltipId) {
        activeTooltip.value = null
      } else {
        activeTooltip.value = tooltipId
      }
    }

    return {
      // State
      users,
      loading,
      searchTerm,
      statusFilter,
      adminFilter,
      meta,
      currentUserId,
      
      // Modals
      showDeleteConfirm,
      showEditModal,
      showHandicapModal,
      userToDelete,
      selectedUser,
      updatingUser,
      editForm,
      
      // Tooltip
      activeTooltip,
      
      // Handicap
      handicapHistory,
      loadingHandicaps,
      showHandicapForm,
      editingHandicap,
      savingHandicap,
      handicapForm,
      
      // Methods
      loadUsers,
      refreshUsers,
      debounceSearch,
      goToPage,
      getUserInitials,
      formatDate,
      toggleUserStatus,
      toggleAdminStatus,
      confirmDeleteUser,
      cancelDelete,
      deleteUser,
      editUser,
      cancelEdit,
      updateUser,
      viewUserHandicaps,
      closeHandicapModal,
      showTooltip,
      hideTooltip,
      toggleTooltip,
      showAddHandicapForm,
      editHandicap,
      cancelHandicapForm,
      resetHandicapForm,
      saveHandicap
    }
  }
}
</script>

<style scoped>
.admin-user-management {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.header-content h1.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--theme-text-primary);
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  color: var(--theme-text-secondary);
  margin: 0;
  font-size: 1rem;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.btn-secondary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: var(--theme-bg-card-alt);
  border: 1px solid var(--theme-border);
  border-radius: 6px;
  color: var(--theme-text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.btn-secondary:hover {
  background: var(--theme-nav-hover);
  border-color: var(--theme-primary);
}

/* Filters */
.filters-section {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  align-items: center;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 300px;
}

.search-box svg {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--theme-text-muted);
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  border: 2px solid var(--theme-border);
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
  background: var(--theme-bg-card);
}

.search-input:focus {
  outline: none;
  border-color: var(--theme-primary);
}

.filter-controls {
  display: flex;
  gap: 1rem;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid var(--theme-border);
  border-radius: 8px;
  background: var(--theme-bg-card);
  color: var(--theme-text-primary);
  cursor: pointer;
  transition: border-color 0.2s ease;
  min-width: 140px;
}

.filter-select:focus {
  outline: none;
  border-color: var(--theme-primary);
}

/* Loading */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: var(--theme-text-secondary);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--theme-border);
  border-top: 4px solid var(--theme-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Users Table */
.users-section {
  background: var(--theme-bg-card);
  border-radius: 12px;
  box-shadow: var(--theme-shadow);
  border: 1px solid var(--theme-border);
  overflow: hidden;
}

.table-container {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th {
  background: var(--theme-bg-card-alt);
  padding: 1rem 1.5rem;
  text-align: left;
  font-weight: 600;
  color: var(--theme-text-primary);
  border-bottom: 2px solid var(--theme-border);
  white-space: nowrap;
}

.users-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--theme-border-light);
  vertical-align: middle;
}

.users-table tr.inactive {
  opacity: 0.6;
  background: var(--theme-bg-card-alt);
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
  background: var(--theme-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.user-details {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: var(--theme-text-primary);
  margin-bottom: 0.25rem;
}

.user-id {
  font-size: 0.8rem;
  color: var(--theme-text-muted);
}

.user-email {
  color: var(--theme-text-secondary);
  font-family: monospace;
  font-size: 0.9rem;
}

/* Badges */
.status-badge, .role-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
}

.status-badge.active {
  background: var(--theme-success-light);
  color: var(--theme-success);
}

.status-badge.inactive {
  background: var(--theme-error-light);
  color: var(--theme-error);
}

.role-badge.admin {
  background: var(--theme-warning-light);
  color: var(--theme-warning);
}

.role-badge.user {
  background: var(--theme-bg-card-alt);
  color: var(--theme-text-secondary);
}

/* Table data */
.handicap-value {
  font-weight: 600;
  color: var(--theme-success);
}

.no-handicap, .no-club, .never-logged {
  color: var(--theme-text-muted);
  font-style: italic;
  font-size: 0.9rem;
}

.club-name, .last-login {
  color: var(--theme-text-secondary);
  font-size: 0.9rem;
}

/* Actions */
.user-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-item {
  position: relative;
  display: inline-block;
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
  transition: all 0.2s ease;
  color: white;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--theme-shadow);
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.view-handicaps {
  background: var(--theme-primary);
}

.action-btn.edit {
  background: var(--theme-warning);
}

.action-btn.activate {
  background: var(--theme-success);
}

.action-btn.deactivate {
  background: var(--theme-error);
}

.action-btn.admin-toggle {
  background: var(--theme-warning);
}

.action-btn.delete {
  background: var(--theme-error);
}

/* Tooltips */
.tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: var(--theme-text-primary);
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  white-space: nowrap;
  z-index: 1000;
  margin-bottom: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  opacity: 0;
  animation: tooltipFadeIn 0.2s ease forwards;
}

.tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: var(--theme-text-primary);
}

@keyframes tooltipFadeIn {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: var(--theme-bg-card-alt);
  border-top: 1px solid var(--theme-border);
}

.pagination-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid var(--theme-border);
  background: var(--theme-bg-card);
  color: var(--theme-text-secondary);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.pagination-btn:hover:not(:disabled) {
  background: var(--theme-nav-hover);
  border-color: var(--theme-primary);
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  color: var(--theme-text-secondary);
  font-weight: 500;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--theme-bg-card);
  border-radius: 12px;
  border: 1px solid var(--theme-border);
}

.empty-icon {
  color: var(--theme-text-muted);
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: var(--theme-text-secondary);
  margin: 0 0 0.5rem 0;
}

.empty-state p {
  color: var(--theme-text-muted);
  margin: 0;
}

/* Modals */
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
  padding: 1rem;
}

.modal {
  background: var(--theme-bg-card);
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal.edit-modal {
  max-width: 600px;
}

.modal.handicap-modal {
  max-width: 700px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--theme-border);
  background: var(--theme-bg-card-alt);
}

.modal-header h3 {
  margin: 0;
  color: var(--theme-text-primary);
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 4px;
  color: var(--theme-text-muted);
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--theme-nav-hover);
  color: var(--theme-text-secondary);
}

.modal-content {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  padding: 1.5rem 2rem;
  border-top: 1px solid var(--theme-border);
  background: var(--theme-bg-card-alt);
}

.btn-primary {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background: var(--theme-primary);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary:hover:not(:disabled) {
  background: var(--theme-primary-dark);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-danger {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background: var(--theme-error);
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-danger:hover {
  background: #dc2626;
}

/* Warning Box */
.warning-box {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  background: var(--theme-error-light);
  border: 1px solid #fecaca;
  border-radius: 8px;
  margin-top: 1rem;
}

.warning-box svg {
  color: var(--theme-error);
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.warning-box strong {
  color: var(--theme-error);
}

.warning-box p {
  margin: 0.5rem 0 0 0;
  color: var(--theme-text-secondary);
  font-size: 0.9rem;
}

/* Edit Form */
.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: var(--theme-text-secondary);
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 2px solid var(--theme-border);
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
  background: var(--theme-bg-card);
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--theme-primary);
}

/* Handicap History */
.handicap-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.handicap-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--theme-bg-card-alt);
  border: 1px solid var(--theme-border);
  border-radius: 8px;
}

.handicap-item .handicap-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--theme-primary);
  min-width: 60px;
  text-align: center;
}

.handicap-details {
  flex: 1;
}

.handicap-period {
  font-weight: 500;
  color: var(--theme-text-primary);
  margin-bottom: 0.25rem;
}

.handicap-period .current {
  color: var(--theme-success);
  font-weight: 600;
}

.handicap-reason {
  font-size: 0.9rem;
  color: var(--theme-text-secondary);
}

.empty-handicaps {
  text-align: center;
  padding: 3rem 2rem;
  color: var(--theme-text-muted);
}

.empty-handicaps svg {
  margin-bottom: 1rem;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
  .admin-user-management {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .filters-section {
    flex-direction: column;
    gap: 1rem;
  }
  
  .search-box {
    min-width: unset;
  }
  
  .filter-controls {
    flex-direction: column;
  }
  
  .table-container {
    font-size: 0.9rem;
  }
  
  .users-table th,
  .users-table td {
    padding: 0.75rem 1rem;
  }
  
  .user-actions {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .action-item {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .action-btn {
    width: 32px;
    height: 32px;
  }
  
  .pagination {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .modal {
    margin: 1rem;
    max-width: unset;
  }
  
  .modal-header,
  .modal-content,
  .modal-actions {
    padding: 1rem;
  }
  
  /* Mobile tooltip adjustments */
  .tooltip {
    position: fixed;
    bottom: auto;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    margin-bottom: 0;
    max-width: 200px;
    text-align: center;
    white-space: normal;
    z-index: 1100;
  }
  
  .tooltip::after {
    display: none;
  }
}

@media (max-width: 480px) {
  .admin-user-management {
    padding: 0.5rem;
  }
  
  .users-table th,
  .users-table td {
    padding: 0.5rem;
    font-size: 0.8rem;
  }
  
  .user-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 0.5rem;
  }
  
  .user-avatar {
    width: 32px;
    height: 32px;
    font-size: 0.8rem;
  }
}

/* Handicap Form Styles */
.handicap-actions {
  margin-bottom: 1.5rem;
  text-align: center;
}

.add-handicap-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 500;
}

.handicap-form {
  background: var(--theme-bg-card-alt);
  border: 1px solid var(--theme-border);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.handicap-form h4 {
  margin: 0 0 1rem 0;
  color: var(--theme-text-primary);
  font-weight: 600;
}

.handicap-form-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.handicap-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: var(--theme-bg-card-alt);
  border: 1px solid var(--theme-border);
  border-radius: 8px;
}

.handicap-item .handicap-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--theme-primary);
  min-width: 60px;
  text-align: center;
}

.handicap-details {
  flex: 1;
}

.handicap-period {
  font-weight: 500;
  color: var(--theme-text-primary);
  margin-bottom: 0.25rem;
}

.handicap-period .current {
  color: var(--theme-success);
  font-weight: 600;
}

.handicap-reason {
  font-size: 0.9rem;
  color: var(--theme-text-secondary);
}

.handicap-item-actions {
  display: flex;
  gap: 0.5rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--theme-border);
}
</style> 