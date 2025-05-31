import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// Import global theme styles
import './assets/theme.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app') 