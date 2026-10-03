import { boot } from 'quasar/wrappers'
import axios from 'axios'
import {
  getOfflineCategories,
  getOfflineProducts,
  getOfflineCustomers,
  getOfflineTransactions,
  saveOfflineTransaction,
  deleteOfflineTransaction,
  getOfflineDailySummary,
  initOfflineStore,
} from 'src/utils/offlineStore'

// Initialize offline storage on app startup
initOfflineStore()

// We configure a default api instance pointing to environment variable, localStorage, dynamic network host, or local Django server.
const getApiBaseURL = () => {
  if (import.meta.env && import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  const savedUrl = typeof localStorage !== 'undefined' ? localStorage.getItem('apiBaseURL') : null
  if (savedUrl) return savedUrl

  if (
    typeof window !== 'undefined' &&
    window.location.hostname &&
    window.location.hostname !== 'localhost' &&
    window.location.hostname !== '127.0.0.1'
  ) {
    return `http://${window.location.hostname}:8000/api/`
  }
  return 'http://127.0.0.1:8000/api/'
}

const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 5000,
})

// Seamless offline fallback interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const isOffline =
      !error.response ||
      error.code === 'ERR_NETWORK' ||
      error.code === 'ECONNABORTED' ||
      error.message?.includes('Network Error') ||
      error.message?.includes('timeout')

    if (isOffline && error.config) {
      const url = error.config.url || ''
      const method = (error.config.method || 'get').toLowerCase()

      if (url.includes('categories/')) {
        return { data: getOfflineCategories(), status: 200, statusText: 'OK (Offline Cache)' }
      }
      if (url.includes('products/low-stock/')) {
        const prods = getOfflineProducts().filter((p) => {
          const bulk =
            parseFloat(p.stock_sacks || 0) +
            parseFloat(p.stock_kilos || 0) / (parseFloat(p.units_per_bulk) || 50)
          return bulk < (p.low_stock_threshold || 5)
        })
        return { data: prods, status: 200, statusText: 'OK (Offline Cache)' }
      }
      if (url.includes('products/')) {
        return { data: getOfflineProducts(), status: 200, statusText: 'OK (Offline Cache)' }
      }
      if (url.includes('customers/')) {
        return { data: getOfflineCustomers(), status: 200, statusText: 'OK (Offline Cache)' }
      }
      if (url.includes('transactions/daily-summary/')) {
        return { data: getOfflineDailySummary(), status: 200, statusText: 'OK (Offline Cache)' }
      }
      if (url.includes('transactions/') && method === 'post') {
        const payload =
          typeof error.config.data === 'string' ? JSON.parse(error.config.data) : error.config.data
        const created = saveOfflineTransaction(payload)
        return { data: created, status: 201, statusText: 'Created (Offline Cache)' }
      }
      if (url.includes('transactions/') && method === 'delete') {
        const match = url.match(/transactions\/(\d+)\//)
        if (match) {
          deleteOfflineTransaction(match[1])
          return { data: { success: true }, status: 204, statusText: 'No Content (Offline Cache)' }
        }
      }
      if (url.includes('transactions/')) {
        return { data: getOfflineTransactions(), status: 200, statusText: 'OK (Offline Cache)' }
      }
      if (url.includes('backup/export/')) {
        return {
          data: {
            app: 'Nichole Agrivet POS & Inventory (Offline)',
            version: '1.0',
            exported_at: new Date().toISOString(),
            categories: getOfflineCategories(),
            products: getOfflineProducts(),
            customers: getOfflineCustomers(),
            transactions: getOfflineTransactions(),
          },
          status: 200,
        }
      }
    }
    return Promise.reject(error)
  },
)

export default boot(({ app }) => {
  // For use inside Vue files (Options API) through this.$axios and this.$api
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { axios, api }
