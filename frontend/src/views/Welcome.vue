<template>
  <div class="welcome-container">
    <div class="welcome-header">
      <div class="logo-section">
        <h1 class="logo">RGS</h1>
        <p class="tagline">Round Golf System</p>
      </div>
    </div>
    
    <div class="auth-section">
      <div class="auth-card">
        <div class="auth-tabs">
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'login' }"
            @click="activeTab = 'login'"
          >
            Sign In
          </button>
          <button 
            class="tab-button" 
            :class="{ active: activeTab === 'register' }"
            @click="activeTab = 'register'"
          >
            Create Account
          </button>
        </div>
        
        <!-- Login Form -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
          <h2 class="form-title">Welcome Back</h2>
          <p class="form-subtitle">Sign in to your account</p>
          
          <div class="form-group">
            <label for="login-email">Email Address</label>
            <input 
              id="login-email"
              v-model="loginForm.email" 
              type="email" 
              required 
              class="form-input"
              placeholder="Enter your email"
            />
          </div>
          
          <div class="form-group">
            <label for="login-password">Password</label>
            <input 
              id="login-password"
              v-model="loginForm.password" 
              type="password" 
              required 
              class="form-input"
              placeholder="Enter your password"
            />
          </div>
          
          <div class="form-actions">
            <button 
              type="button" 
              @click="showForgotPassword = true"
              class="link-button"
            >
              Forgot Password?
            </button>
          </div>
          
          <button 
            type="submit" 
            :disabled="authStore.loading"
            class="submit-button"
          >
            <span v-if="authStore.loading">Signing In...</span>
            <span v-else>Sign In</span>
          </button>
        </form>
        
        <!-- Register Form -->
        <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="auth-form">
          <h2 class="form-title">Create Account</h2>
          <p class="form-subtitle">Join the Round Golf System</p>
          
          <div class="form-row">
            <div class="form-group">
              <label for="register-first-name">First Name</label>
              <input 
                id="register-first-name"
                v-model="registerForm.first_name" 
                type="text" 
                required 
                class="form-input"
                placeholder="First name"
              />
            </div>
            <div class="form-group">
              <label for="register-last-name">Last Name</label>
              <input 
                id="register-last-name"
                v-model="registerForm.last_name" 
                type="text" 
                required 
                class="form-input"
                placeholder="Last name"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="register-email">Email Address</label>
            <input 
              id="register-email"
              v-model="registerForm.email" 
              type="email" 
              required 
              class="form-input"
              placeholder="Enter your email"
            />
          </div>
          
          <div class="form-group">
            <label for="register-password">Password</label>
            <input 
              id="register-password"
              v-model="registerForm.password" 
              type="password" 
              required 
              class="form-input"
              placeholder="Create a password"
            />
          </div>
          
          <div class="form-group">
            <label for="register-confirm-password">Confirm Password</label>
            <input 
              id="register-confirm-password"
              v-model="registerForm.confirmPassword" 
              type="password" 
              required 
              class="form-input"
              placeholder="Confirm your password"
            />
          </div>
          
          <button 
            type="submit" 
            :disabled="authStore.loading || !passwordsMatch"
            class="submit-button"
          >
            <span v-if="authStore.loading">Creating Account...</span>
            <span v-else>Create Account</span>
          </button>
        </form>
        
        <!-- Error Display -->
        <div v-if="authStore.error" class="error-message">
          {{ authStore.error }}
        </div>
      </div>
    </div>
    
    <!-- Forgot Password Modal -->
    <div v-if="showForgotPassword" class="modal-overlay" @click="showForgotPassword = false">
      <div class="modal-content" @click.stop>
        <h3>Reset Password</h3>
        <p>Enter your email address and we'll send you a link to reset your password.</p>
        
        <form @submit.prevent="handleForgotPassword">
          <div class="form-group">
            <label for="reset-email">Email Address</label>
            <input 
              id="reset-email"
              v-model="resetEmail" 
              type="email" 
              required 
              class="form-input"
              placeholder="Enter your email"
            />
          </div>
          
          <div class="modal-actions">
            <button type="button" @click="showForgotPassword = false" class="cancel-button">
              Cancel
            </button>
            <button type="submit" :disabled="authStore.loading" class="submit-button">
              Send Reset Link
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

export default {
  name: 'Welcome',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const activeTab = ref('login')
    const showForgotPassword = ref(false)
    const resetEmail = ref('')
    
    const loginForm = ref({
      email: '',
      password: ''
    })
    
    const registerForm = ref({
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    
    const passwordsMatch = computed(() => {
      return registerForm.value.password === registerForm.value.confirmPassword
    })
    
    const handleLogin = async () => {
      const result = await authStore.login(loginForm.value.email, loginForm.value.password)
      if (result.success) {
        router.push('/dashboard')
      }
    }
    
    const handleRegister = async () => {
      if (!passwordsMatch.value) {
        authStore.error = 'Passwords do not match'
        return
      }
      
      const userData = {
        first_name: registerForm.value.first_name,
        last_name: registerForm.value.last_name,
        email: registerForm.value.email,
        password: registerForm.value.password
      }
      
      const result = await authStore.register(userData)
      if (result.success) {
        router.push('/dashboard')
      }
    }
    
    const handleForgotPassword = async () => {
      const result = await authStore.requestPasswordReset(resetEmail.value)
      if (result.success) {
        showForgotPassword.value = false
        resetEmail.value = ''
        alert('Password reset email sent! Check your inbox.')
      }
    }
    
    return {
      activeTab,
      showForgotPassword,
      resetEmail,
      loginForm,
      registerForm,
      passwordsMatch,
      authStore,
      handleLogin,
      handleRegister,
      handleForgotPassword
    }
  }
}
</script>

<style scoped>
.welcome-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem 1rem;
}

.welcome-header {
  text-align: center;
  margin-bottom: 3rem;
}

.logo-section {
  color: #2c3e50;
}

.logo {
  font-size: 4rem;
  font-weight: 800;
  margin: 0;
  letter-spacing: -2px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.tagline {
  font-size: 1.2rem;
  color: #64748b;
  margin: 0.5rem 0 0 0;
  font-weight: 500;
}

.auth-section {
  width: 100%;
  max-width: 400px;
}

.auth-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.auth-tabs {
  display: flex;
  background: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.tab-button {
  flex: 1;
  padding: 1rem;
  border: none;
  background: transparent;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-button.active {
  color: #667eea;
  background: white;
  border-bottom: 2px solid #667eea;
}

.tab-button:hover:not(.active) {
  color: #475569;
  background: #f1f5f9;
}

.auth-form {
  padding: 2rem;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  text-align: center;
}

.form-subtitle {
  color: #64748b;
  text-align: center;
  margin: 0 0 2rem 0;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  flex: 1;
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-actions {
  text-align: right;
  margin-bottom: 1.5rem;
}

.link-button {
  background: none;
  border: none;
  color: #667eea;
  cursor: pointer;
  font-size: 0.9rem;
  text-decoration: underline;
}

.link-button:hover {
  color: #5a67d8;
}

.submit-button {
  width: 100%;
  padding: 0.875rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.submit-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  background: #fee2e2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 0.9rem;
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

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}

.modal-content h3 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
}

.modal-content p {
  color: #64748b;
  margin: 0 0 1.5rem 0;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-button {
  flex: 1;
  padding: 0.75rem;
  background: #f8fafc;
  color: #64748b;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}

.cancel-button:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}
</style> 