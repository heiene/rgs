import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token'),
    loading: false,
    error: null
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
          
          // Set default axios header for future requests
          axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
          
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
        delete axios.defaults.headers.common['Authorization']
      }
    },
    
    async getCurrentUser() {
      if (!this.token) return
      
      try {
        const response = await axios.get(`${API_BASE_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${this.token}` }
        })
        
        this.user = response.data.user
        this.isAuthenticated = true
      } catch (error) {
        console.warn('Failed to get current user:', error)
        this.logout()
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
    
    initializeAuth() {
      if (this.token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        this.getCurrentUser()
      }
    }
  }
}) 