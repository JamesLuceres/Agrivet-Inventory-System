import { boot } from 'quasar/wrappers'
import axios from 'axios'
import {
  getOfflineCategories,
  saveOfflineCategory,
  getOfflineProducts,
  saveOfflineProduct,
  deleteOfflineProduct,
  getOfflineCustomers,
  saveOfflineCustomer,
  patchOfflineCustomer,
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
  timeout: 4000,
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
      const parseBody = () => {
        if (!error.config.data) return {}
        return typeof error.config.data === 'string'
          ? JSON.parse(error.config.data)
          : error.config.data
      }

      // CATEGORIES
      if (url.includes('categories/')) {
        if (method === 'post') {
          const created = saveOfflineCategory(parseBody())
          return { data: created, status: 201, statusText: 'Created (Offline Mode)' }
        }
        return { data: getOfflineCategories(), status: 200, statusText: 'OK (Offline Mode)' }
      }

      // PRODUCTS LOW STOCK
      if (url.includes('products/low-stock/')) {
        const prods = getOfflineProducts().filter((p) => {
          const bulk =
            parseFloat(p.stock_sacks || 0) +
            parseFloat(p.stock_kilos || 0) / (parseFloat(p.units_per_bulk) || 50)
          return bulk < (p.low_stock_threshold || 5)
        })
        return { data: prods, status: 200, statusText: 'OK (Offline Mode)' }
      }

      // PRODUCTS CRUD
      if (url.includes('products/')) {
        if (method === 'post') {
          const created = saveOfflineProduct(parseBody())
          return { data: created, status: 201, statusText: 'Created (Offline Mode)' }
        }
        if (method === 'put' || method === 'patch') {
          const match = url.match(/products\/(\d+)\//)
          const prodId = match ? match[1] : null
          const updated = saveOfflineProduct(parseBody(), prodId)
          return { data: updated, status: 200, statusText: 'OK (Offline Mode)' }
        }
        if (method === 'delete') {
          const match = url.match(/products\/(\d+)\//)
          if (match) {
            deleteOfflineProduct(match[1])
            return { data: { success: true }, status: 204, statusText: 'No Content (Offline Mode)' }
          }
        }
        return { data: getOfflineProducts(), status: 200, statusText: 'OK (Offline Mode)' }
      }

      // CUSTOMERS CRUD
      if (url.includes('customers/')) {
        if (method === 'post') {
          const created = saveOfflineCustomer(parseBody())
          return { data: created, status: 201, statusText: 'Created (Offline Mode)' }
        }
        if (method === 'patch' || method === 'put') {
          const match = url.match(/customers\/(\d+)\//)
          const custId = match ? match[1] : null
          const updated = patchOfflineCustomer(custId, parseBody())
          return { data: updated, status: 200, statusText: 'OK (Offline Mode)' }
        }
        return { data: getOfflineCustomers(), status: 200, statusText: 'OK (Offline Mode)' }
      }

      // DAILY SUMMARY
      if (url.includes('transactions/daily-summary/')) {
        return { data: getOfflineDailySummary(), status: 200, statusText: 'OK (Offline Mode)' }
      }

      // TRANSACTIONS CRUD
      if (url.includes('transactions/')) {
        if (method === 'post') {
          const created = saveOfflineTransaction(parseBody())
          return { data: created, status: 201, statusText: 'Created (Offline Mode)' }
        }
        if (method === 'delete') {
          const match = url.match(/transactions\/(\d+)\//)
          if (match) {
            deleteOfflineTransaction(match[1])
            return { data: { success: true }, status: 204, statusText: 'No Content (Offline Mode)' }
          }
        }
        return { data: getOfflineTransactions(), status: 200, statusText: 'OK (Offline Mode)' }
      }

      // BACKUP EXPORT & RESTORE
      if (url.includes('backup/export/')) {
        return {
          data: {
            app: 'Nichole Agrivet POS & Inventory (Standalone Tablet)',
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
      if (url.includes('backup/restore/') && method === 'post') {
        const payload = parseBody()
        if (payload.categories) {
          localStorage.setItem('offline_categories', JSON.stringify(payload.categories))
        }
        if (payload.products) {
          localStorage.setItem('offline_products', JSON.stringify(payload.products))
        }
        if (payload.customers) {
          localStorage.setItem('offline_customers', JSON.stringify(payload.customers))
        }
        if (payload.transactions) {
          localStorage.setItem('offline_transactions', JSON.stringify(payload.transactions))
        }
        return { data: { success: true, message: 'Database restored successfully!' }, status: 200 }
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
