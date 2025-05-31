import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null,
    refreshInterval: null
  }),
  
  getters: {
    isLoggedIn: (state) => state.isAuthenticated && state.user !== null,
    currentUser: (state) => state.user,
    authToken: (state) => state.token
  },
  
  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/login`, {
          email,
          password
        })
        
        if (response.data.access_token) {
          this.token = response.data.access_token
          this.user = response.data.user
          this.isAuthenticated = true
          
          localStorage.setItem('token', this.token)
          localStorage.setItem('user', JSON.stringify(this.user))
          
          // Set default axios header for future requests
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
          
          // Start auto-refresh of user data
          this.startUserDataRefresh()
          
          return { success: true }
        } else {
          throw new Error('No access token received')
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Login failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
    
    async register(userData) {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/register`, userData)
        
        if (response.data.access_token) {
          this.token = response.data.access_token
          this.user = response.data.user
          this.isAuthenticated = true
          
          localStorage.setItem('token', this.token)
          localStorage.setItem('user', JSON.stringify(this.user))
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
          
          return { success: true }
        } else {
          throw new Error('Registration failed')
        }
      } catch (error) {
        this.error = error.response?.data?.message || 'Registration failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
    
    async logout() {
      // Stop auto-refresh
      this.stopUserDataRefresh()
      
      try {
        if (this.token) {
          await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
            headers: { Authorization: `Bearer ${this.token}` }
          })
        }
      } catch (error) {
        console.warn('Logout request failed:', error)
      } finally {
        this.user = null
        this.token = null
        this.isAuthenticated = false
        
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
      }
    },
    
    async getCurrentUser() {
      if (!this.token) return
      
      try {
        const response = await axios.get(`${API_BASE_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        
        const data = response.data
        
        // Handle permission changes and account status
        if (data.action_required) {
          if (data.action_required === 'logout') {
            console.warn('Account deactivated, logging out...')
            await this.logout()
            return { action: 'logout', message: data.message }
          } else if (data.action_required === 'token_refresh') {
            console.warn('Permissions changed, refreshing token...')
            const refreshResult = await this.refreshToken()
            if (!refreshResult.success) {
              console.error('Token refresh failed, logging out...')
              await this.logout()
              return { action: 'logout', message: 'Session expired due to permission changes' }
            }
            return { action: 'refresh', message: data.message }
          }
        }
        
        // Update user data if everything is fine
        this.user = data.user
        this.isAuthenticated = true
        localStorage.setItem('user', JSON.stringify(this.user))
        
        return { action: 'none' }
        
      } catch (error) {
        console.warn('Failed to get current user:', error)
        if (error.response?.status === 403) {
          // Account deactivated or permissions revoked
          await this.logout()
          return { action: 'logout', message: 'Your access has been revoked' }
        }
        // For other errors, just logout to be safe
        await this.logout()
        return { action: 'logout', message: 'Authentication error' }
      }
    },
    
    async updateProfile(profileData) {
      this.loading = true
      this.error = null
      
      console.log('🔄 Starting profile update...')
      console.log('Current token:', this.token)
      console.log('Axios default auth header:', axios.defaults.headers.common['Authorization'])
      
      try {
        // Filter out email and other fields that can't be updated via this endpoint
        const updateData = {
          first_name: profileData.first_name?.trim(),
          last_name: profileData.last_name?.trim(),
          sex: profileData.sex,
          country: profileData.country?.trim() || null,
          city: profileData.city?.trim() || null,
          address: profileData.address?.trim() || null,
          postal_code: profileData.postal_code?.trim() || null,
          timezone: profileData.timezone,
          distance_unit: profileData.distance_unit
        }

        // Validate required fields
        if (!updateData.first_name || updateData.first_name.length === 0) {
          this.error = 'First name is required'
          return { success: false, error: this.error }
        }
        
        if (!updateData.last_name || updateData.last_name.length === 0) {
          this.error = 'Last name is required'
          return { success: false, error: this.error }
        }

        // Validate distance_unit
        if (!['meters', 'yards'].includes(updateData.distance_unit)) {
          updateData.distance_unit = 'yards' // default fallback
        }

        // Remove null values to avoid sending them
        Object.keys(updateData).forEach(key => {
          if (updateData[key] === null || updateData[key] === '') {
            delete updateData[key]
          }
        })

        console.log('Sending profile update data:', updateData)

        const response = await axios.put(`${API_BASE_URL}/users/profile`, updateData, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        
        if (response.data.success) {
          this.user = { ...this.user, ...response.data.data }
          localStorage.setItem('user', JSON.stringify(this.user))
          return { success: true }
        }
      } catch (error) {
        console.error('Profile update error:', error)
        console.error('Error response:', error.response?.data)
        
        // Log validation details more clearly
        if (error.response?.data?.details) {
          console.error('Validation details:', JSON.stringify(error.response.data.details, null, 2))
        }
        
        let errorMessage = 'Profile update failed'
        if (error.response?.data?.details) {
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
        
        this.error = errorMessage
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
    
    async requestPasswordReset(email) {
      this.loading = true
      this.error = null
      
      try {
        await axios.post(`${API_BASE_URL}/auth/request-password-reset`, { email })
        return { success: true, message: 'Password reset email sent' }
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to send reset email'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },
    
    isTokenExpired() {
      if (!this.token) return true
      
      try {
        const payload = JSON.parse(atob(this.token.split('.')[1]))
        const currentTime = Date.now() / 1000
        console.log('🕒 Token expires at:', new Date(payload.exp * 1000))
        console.log('🕒 Current time:', new Date(currentTime * 1000))
        console.log('🕒 Token expired?', payload.exp < currentTime)
        return payload.exp < currentTime
      } catch (error) {
        console.error('Error parsing token:', error)
        return true
      }
    },
    
    initializeAuth() {
      console.log('🔐 Initializing auth...')
      console.log('Token in state:', this.token)
      console.log('Token in localStorage:', localStorage.getItem('token'))
      console.log('User in state:', this.user)
      console.log('User in localStorage:', localStorage.getItem('user'))
      
      if (this.token) {
        if (this.isTokenExpired()) {
          console.log('⏰ Token is expired, logging out...')
          this.logout()
          return
        }
        
        console.log('✅ Setting axios default header with token')
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        // Only fetch user data if we don't have it in localStorage
        if (!this.user) {
          console.log('👤 Fetching current user data...')
          this.getCurrentUser()
        }
      } else {
        console.log('❌ No token found, user needs to login')
      }
    },

    async refreshToken() {
      if (!this.token) return { success: false }
      
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {}, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        
        if (response.data.access_token) {
          this.token = response.data.access_token
          localStorage.setItem('token', this.token)
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
          
          // Refresh user data after token refresh
          await this.getCurrentUser()
          return { success: true }
        }
        
        return { success: false }
      } catch (error) {
        console.error('Token refresh failed:', error)
        return { success: false }
      }
    },

    // Auto-refresh user data every 30 seconds when app is active
    startUserDataRefresh() {
      if (this.refreshInterval) return // Already started
      
      this.refreshInterval = setInterval(async () => {
        if (this.isAuthenticated && this.token) {
          const result = await this.getCurrentUser()
          
          // Handle permission changes
          if (result.action === 'logout') {
            // User will be logged out automatically
            this.stopUserDataRefresh()
          } else if (result.action === 'refresh') {
            // Show notification about permission changes
            console.info('Your permissions have been updated')
          }
        }
      }, 30000) // 30 seconds
    },

    stopUserDataRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
    }
  }
}) 