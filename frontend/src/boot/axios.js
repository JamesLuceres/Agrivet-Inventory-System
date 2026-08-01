import { boot } from 'quasar/wrappers'
import axios from 'axios'

// We configure a default api instance pointing to the local Django server.
const api = axios.create({ baseURL: 'http://127.0.0.1:8000/api/' })

export default boot(({ app }) => {
  // For use inside Vue files (Options API) through this.$axios and this.$api
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { axios, api }
