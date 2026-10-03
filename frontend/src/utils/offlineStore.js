import seedData from './seedData.json'

const STORAGE_KEYS = {
  PRODUCTS: 'offline_products',
  CATEGORIES: 'offline_categories',
  CUSTOMERS: 'offline_customers',
  TRANSACTIONS: 'offline_transactions',
  INITIALIZED: 'offline_initialized_v1',
}

export function initOfflineStore() {
  if (typeof localStorage === 'undefined') return
  const isInit = localStorage.getItem(STORAGE_KEYS.INITIALIZED)
  if (!isInit) {
    localStorage.setItem(STORAGE_KEYS.CATEGORIES, JSON.stringify(seedData.categories || []))
    localStorage.setItem(STORAGE_KEYS.PRODUCTS, JSON.stringify(seedData.products || []))
    localStorage.setItem(STORAGE_KEYS.CUSTOMERS, JSON.stringify(seedData.customers || []))
    localStorage.setItem(STORAGE_KEYS.TRANSACTIONS, JSON.stringify(seedData.transactions || []))
    localStorage.setItem(STORAGE_KEYS.INITIALIZED, 'true')
  }
}

export function getOfflineCategories() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.CATEGORIES) || '[]')
}

export function getOfflineProducts() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.PRODUCTS) || '[]')
}

export function getOfflineCustomers() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.CUSTOMERS) || '[]')
}

export function getOfflineTransactions() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.TRANSACTIONS) || '[]')
}

export function saveOfflineTransaction(payload) {
  initOfflineStore()
  const transactions = getOfflineTransactions()
  const products = getOfflineProducts()
  const customers = getOfflineCustomers()

  const newId = transactions.length > 0 ? Math.max(...transactions.map((t) => t.id || 0)) + 1 : 1001
  const nowStr = new Date().toISOString()

  let custName = 'Walk-in Customer'
  if (payload.customer) {
    const cust = customers.find((c) => c.id === payload.customer)
    if (cust) {
      custName = cust.name
      if (payload.transaction_type === 'CREDIT') {
        const debt = parseFloat(payload.total_amount) - parseFloat(payload.amount_paid || 0)
        cust.total_utang = (parseFloat(cust.total_utang || 0) + debt).toFixed(2)
      } else if (payload.transaction_type === 'DEBT_PAYMENT') {
        cust.total_utang = Math.max(0, parseFloat(cust.total_utang || 0) - parseFloat(payload.amount_paid || 0)).toFixed(2)
      }
      localStorage.setItem(STORAGE_KEYS.CUSTOMERS, JSON.stringify(customers))
    }
  }

  // Deduct stock for physical items
  ;(payload.items || []).forEach((item) => {
    const prod = products.find((p) => p.id === item.product)
    if (prod && !prod.is_service) {
      const qty = parseFloat(item.quantity) || 1
      if (item.unit_type === 'SACK') {
        prod.stock_sacks = Math.max(0, (parseFloat(prod.stock_sacks) || 0) - qty).toFixed(2)
      } else {
        prod.stock_kilos = Math.max(0, (parseFloat(prod.stock_kilos) || 0) - qty).toFixed(2)
      }
    }
  })
  localStorage.setItem(STORAGE_KEYS.PRODUCTS, JSON.stringify(products))

  const newTx = {
    id: newId,
    transaction_type: payload.transaction_type,
    reference_number: payload.reference_number || '',
    customer: payload.customer,
    customer_name: custName,
    total_amount: parseFloat(payload.total_amount).toFixed(2),
    amount_paid: parseFloat(payload.amount_paid).toFixed(2),
    change_given: parseFloat(payload.change_given || 0).toFixed(2),
    created_at: nowStr,
    items: (payload.items || []).map((i, idx) => {
      const prod = products.find((p) => p.id === i.product)
      return {
        id: idx + 1,
        product: i.product,
        product_name: prod ? prod.name : 'Item',
        unit_type: i.unit_type,
        quantity: i.quantity,
        unit_price: i.unit_price,
        subtotal: i.subtotal,
        notes: i.notes || '',
      }
    }),
  }

  transactions.unshift(newTx)
  localStorage.setItem(STORAGE_KEYS.TRANSACTIONS, JSON.stringify(transactions))
  return newTx
}

export function deleteOfflineTransaction(txId) {
  initOfflineStore()
  const transactions = getOfflineTransactions()
  const products = getOfflineProducts()
  const customers = getOfflineCustomers()

  const targetIdx = transactions.findIndex((t) => t.id === parseInt(txId, 10))
  if (targetIdx === -1) return false

  const tx = transactions[targetIdx]

  // Reverse debt if credit
  if (tx.customer) {
    const cust = customers.find((c) => c.id === tx.customer)
    if (cust && tx.transaction_type === 'CREDIT') {
      const debt = parseFloat(tx.total_amount) - parseFloat(tx.amount_paid || 0)
      cust.total_utang = Math.max(0, parseFloat(cust.total_utang || 0) - debt).toFixed(2)
      localStorage.setItem(STORAGE_KEYS.CUSTOMERS, JSON.stringify(customers))
    }
  }

  // Restore inventory
  ;(tx.items || []).forEach((item) => {
    const prod = products.find((p) => p.id === item.product)
    if (prod && !prod.is_service) {
      const qty = parseFloat(item.quantity) || 1
      if (item.unit_type === 'SACK') {
        prod.stock_sacks = ((parseFloat(prod.stock_sacks) || 0) + qty).toFixed(2)
      } else {
        prod.stock_kilos = ((parseFloat(prod.stock_kilos) || 0) + qty).toFixed(2)
      }
    }
  })
  localStorage.setItem(STORAGE_KEYS.PRODUCTS, JSON.stringify(products))

  transactions.splice(targetIdx, 1)
  localStorage.setItem(STORAGE_KEYS.TRANSACTIONS, JSON.stringify(transactions))
  return true
}

export function getOfflineDailySummary() {
  initOfflineStore()
  const transactions = getOfflineTransactions()
  const todayStr = new Date().toISOString().slice(0, 10)

  const todayTxs = transactions.filter((t) => (t.created_at || '').startsWith(todayStr))
  let totalCash = 0
  let totalGcash = 0
  let totalCredit = 0
  let totalDebtCollected = 0

  todayTxs.forEach((t) => {
    const amt = parseFloat(t.total_amount) || 0
    if (t.transaction_type === 'CASH') totalCash += amt
    else if (t.transaction_type === 'GCASH') totalGcash += amt
    else if (t.transaction_type === 'CREDIT') totalCredit += amt
    else if (t.transaction_type === 'DEBT_PAYMENT') totalDebtCollected += amt
  })

  return {
    today_date: todayStr,
    total_sales_revenue: totalCash + totalGcash + totalCredit,
    total_cash_revenue: totalCash,
    total_shift_sales: totalCash + totalDebtCollected,
    total_gcash_revenue: totalGcash,
    total_credit_issued: totalCredit,
    total_debt_collected: totalDebtCollected,
    transaction_count: todayTxs.length,
    recent_transactions: todayTxs.slice(0, 20),
  }
}
