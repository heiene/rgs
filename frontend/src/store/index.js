import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    message: 'Hello from Pinia Store!',
    counter: 0
  }),
  
  getters: {
    doubleCount: (state) => state.counter * 2
  },
  
  actions: {
    increment() {
      this.counter++
    },
    
    setMessage(newMessage) {
      this.message = newMessage
    }
  }
}) 