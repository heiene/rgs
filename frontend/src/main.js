import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './store/auth'

// Import global theme styles
import './assets/theme.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize auth store and start auto-refresh if user is logged in
const authStore = useAuthStore()
if (authStore.isAuthenticated) {
  authStore.startUserDataRefresh()
}

app.mount('#app') 