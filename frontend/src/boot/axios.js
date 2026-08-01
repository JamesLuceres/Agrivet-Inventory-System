import { boot } from 'quasar/wrappers'
import axios from 'axios'

// We configure a default api instance pointing to environment variable or local Django server.
const apiBaseURL = (import.meta.env && import.meta.env.VITE_API_URL) || 'http://127.0.0.1:8000/api/'
const api = axios.create({ baseURL: apiBaseURL })

export default boot(({ app }) => {
  // For use inside Vue files (Options API) through this.$axios and this.$api
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { axios, api }
