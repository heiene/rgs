<template>
  <div class="login">
    <h1>Login</h1>
    <p>Authentication interface - to be implemented</p>
    
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input 
          type="text" 
          id="username" 
          v-model="username" 
          required 
        />
      </div>
      
      <div class="form-group">
        <label for="password">Password:</label>
        <input 
          type="password" 
          id="password" 
          v-model="password" 
          required 
        />
      </div>
      
      <button type="submit">Login</button>
    </form>
    
    <div v-if="message" class="message">
      {{ message }}
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'Login',
  setup() {
    const username = ref('')
    const password = ref('')
    const message = ref('')
    
    const handleLogin = async () => {
      try {
        const response = await axios.post('/api/v1/auth/login', {
          username: username.value,
          password: password.value
        })
        message.value = `Login response: ${JSON.stringify(response.data)}`
      } catch (error) {
        message.value = `Login error: ${error.message}`
      }
    }
    
    return {
      username,
      password,
      message,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.login-form {
  text-align: left;
  margin-top: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #369870;
}

.message {
  margin-top: 20px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 4px;
  word-wrap: break-word;
}
</style> 