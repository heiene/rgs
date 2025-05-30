<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    
    onMounted(() => {
      // Initialize authentication on app start
      authStore.initializeAuth()
    })
    
    return {}
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #f8fafc;
  color: #1e293b;
  line-height: 1.6;
  /* Mobile optimization */
  -webkit-text-size-adjust: 100%;
  -ms-text-size-adjust: 100%;
  touch-action: manipulation;
}

#app {
  min-height: 100vh;
  /* Prevent horizontal scroll on mobile */
  overflow-x: hidden;
}

/* Global button styles */
button {
  font-family: inherit;
  /* Make buttons more touch-friendly */
  min-height: 44px;
  min-width: 44px;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}

/* Global input styles */
input, textarea, select {
  font-family: inherit;
  /* Prevent zoom on iOS when font-size < 16px */
  font-size: 16px;
  touch-action: manipulation;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}

/* Utility classes for consistent spacing and styling */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.text-right {
  text-align: right;
}

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

/* Light theme color variables - clean and minimal */
:root {
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --color-secondary: #64748b;
  --color-accent: #3b82f6;
  
  --color-gray-50: #f8fafc;
  --color-gray-100: #f1f5f9;
  --color-gray-200: #e2e8f0;
  --color-gray-300: #cbd5e1;
  --color-gray-400: #94a3b8;
  --color-gray-500: #64748b;
  --color-gray-600: #475569;
  --color-gray-700: #334155;
  --color-gray-800: #1e293b;
  --color-gray-900: #0f172a;
  
  --color-success: #059669;
  --color-warning: #d97706;
  --color-error: #dc2626;
  --color-info: #0284c7;
  
  --border-radius-sm: 4px;
  --border-radius: 8px;
  --border-radius-lg: 12px;
  --border-radius-xl: 16px;
  
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.08);
  --shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.1);
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  /* Ensure content doesn't get too close to screen edges */
  .container {
    padding: 0 1rem;
  }
  
  /* More generous spacing on mobile */
  .mb-1 { margin-bottom: 0.75rem; }
  .mb-2 { margin-bottom: 1.25rem; }
  .mb-3 { margin-bottom: 1.75rem; }
  .mb-4 { margin-bottom: 2.25rem; }
  
  .mt-1 { margin-top: 0.75rem; }
  .mt-2 { margin-top: 1.25rem; }
  .mt-3 { margin-top: 1.75rem; }
  .mt-4 { margin-top: 2.25rem; }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.5rem;
  }
  
  /* Larger touch targets for small screens */
  button {
    min-height: 48px;
    min-width: 48px;
  }
}
</style> 