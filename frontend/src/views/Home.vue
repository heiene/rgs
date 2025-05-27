<template>
  <div class="home">
    <h1>Welcome to RGS</h1>
    <p>Vue 3 + Flask Backend Application</p>
    
    <div class="api-test">
      <h2>API Connection Test</h2>
      <button @click="testHealthEndpoint">Test Health Endpoint</button>
      <button @click="testApiEndpoint">Test API Endpoint</button>
      
      <div v-if="healthStatus" class="status">
        <h3>Health Status:</h3>
        <pre>{{ healthStatus }}</pre>
      </div>
      
      <div v-if="apiResponse" class="status">
        <h3>API Response:</h3>
        <pre>{{ apiResponse }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'

export default {
  name: 'Home',
  setup() {
    const healthStatus = ref(null)
    const apiResponse = ref(null)
    
    const testHealthEndpoint = async () => {
      try {
        const response = await axios.get('/health')
        healthStatus.value = response.data
      } catch (error) {
        healthStatus.value = { error: error.message }
      }
    }
    
    const testApiEndpoint = async () => {
      try {
        const response = await axios.get('/api/v1/users')
        apiResponse.value = response.data
      } catch (error) {
        apiResponse.value = { error: error.message }
      }
    }
    
    return {
      healthStatus,
      apiResponse,
      testHealthEndpoint,
      testApiEndpoint
    }
  }
}
</script>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.api-test {
  margin-top: 40px;
  text-align: left;
}

button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #369870;
}

.status {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

pre {
  text-align: left;
  white-space: pre-wrap;
}
</style> 