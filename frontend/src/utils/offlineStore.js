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

// -------------------------------------------------------------
// CATEGORIES CRUD
// -------------------------------------------------------------
export function getOfflineCategories() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.CATEGORIES) || '[]')
}

export function saveOfflineCategory(payload) {
  initOfflineStore()
  const categories = getOfflineCategories()
  const name = typeof payload === 'string' ? payload.trim() : (payload.name || '').trim()
  const existing = categories.find((c) => c.name.toLowerCase() === name.toLowerCase())
  if (existing) return existing

  const newId = categories.length > 0 ? Math.max(...categories.map((c) => c.id || 0)) + 1 : 1
  const newCat = {
    id: newId,
    name: name,
    description: payload.description || null,
  }
  categories.push(newCat)
  localStorage.setItem(STORAGE_KEYS.CATEGORIES, JSON.stringify(categories))
  return newCat
}

// -------------------------------------------------------------
// PRODUCTS CRUD
// -------------------------------------------------------------
export function getOfflineProducts() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.PRODUCTS) || '[]')
}

export function saveOfflineProduct(payload, productId = null) {
  initOfflineStore()
  const products = getOfflineProducts()
  const categories = getOfflineCategories()

  const id = productId ? parseInt(productId, 10) : null
  const catObj = categories.find((c) => c.id === payload.category)
  const categoryName = catObj ? catObj.name : 'Essentials'

  const ratio = parseFloat(payload.units_per_bulk) || 50
  const sacks = parseFloat(payload.stock_sacks || 0)
  const kilos = parseFloat(payload.stock_kilos || 0)
  const totalBaseStock = payload.unit_bulk_name && ratio > 1 ? sacks * ratio + kilos : kilos

  if (id) {
    const idx = products.findIndex((p) => p.id === id)
    if (idx > -1) {
      const updated = {
        ...products[idx],
        ...payload,
        id: id,
        category_name: categoryName,
        total_base_stock: totalBaseStock,
      }
      products[idx] = updated
      localStorage.setItem(STORAGE_KEYS.PRODUCTS, JSON.stringify(products))
      return updated
    }
  }

  // Create new product
  const newId = products.length > 0 ? Math.max(...products.map((p) => p.id || 0)) + 1 : 101
  const newProd = {
    id: newId,
    name: payload.name,
    category: payload.category,
    category_name: categoryName,
    unit_bulk_name: payload.unit_bulk_name || null,
    unit_retail_name: payload.unit_retail_name || 'Piece',
    units_per_bulk: payload.units_per_bulk || 50,
    price_per_sack: payload.price_per_sack ?? null,
    price_per_kilo: payload.price_per_kilo ?? null,
    cost_per_sack: payload.cost_per_sack ?? null,
    cost_per_kilo: payload.cost_per_kilo ?? null,
    stock_sacks: (sacks || 0).toFixed(2),
    stock_kilos: (kilos || 0).toFixed(2),
    low_stock_threshold: payload.low_stock_threshold ?? 5,
    is_active: payload.is_active !== false,
    is_service: payload.is_service === true,
    total_base_stock: totalBaseStock,
  }

  products.push(newProd)
  localStorage.setItem(STORAGE_KEYS.PRODUCTS, JSON.stringify(products))
  return newProd
}

export function deleteOfflineProduct(productId) {
  initOfflineStore()
  const products = getOfflineProducts()
  const id = parseInt(productId, 10)
  const idx = products.findIndex((p) => p.id === id)
  if (idx === -1) return false

  products.splice(idx, 1)
  localStorage.setItem(STORAGE_KEYS.PRODUCTS, JSON.stringify(products))
  return true
}

// -------------------------------------------------------------
// CUSTOMERS CRUD
// -------------------------------------------------------------
export function getOfflineCustomers() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.CUSTOMERS) || '[]')
}

export function saveOfflineCustomer(payload, customerId = null) {
  initOfflineStore()
  const customers = getOfflineCustomers()
  const id = customerId ? parseInt(customerId, 10) : null

  if (id) {
    const idx = customers.findIndex((c) => c.id === id)
    if (idx > -1) {
      const updated = {
        ...customers[idx],
        name: payload.name || customers[idx].name,
        contact_number:
          payload.contact_number !== undefined
            ? payload.contact_number
            : customers[idx].contact_number,
        notes: payload.notes !== undefined ? payload.notes : customers[idx].notes,
        total_utang:
          payload.total_utang !== undefined ? payload.total_utang : customers[idx].total_utang,
      }
      customers[idx] = updated
      localStorage.setItem(STORAGE_KEYS.CUSTOMERS, JSON.stringify(customers))
      return updated
    }
  }

  const newId = customers.length > 0 ? Math.max(...customers.map((c) => c.id || 0)) + 1 : 1
  const newCust = {
    id: newId,
    name: payload.name,
    contact_number: payload.contact_number || null,
    total_utang: payload.total_utang ? parseFloat(payload.total_utang).toFixed(2) : '0.00',
    notes: payload.notes || null,
  }

  customers.push(newCust)
  localStorage.setItem(STORAGE_KEYS.CUSTOMERS, JSON.stringify(customers))
  return newCust
}

export function patchOfflineCustomer(customerId, patchData) {
  initOfflineStore()
  const customers = getOfflineCustomers()
  const id = parseInt(customerId, 10)
  const idx = customers.findIndex((c) => c.id === id)
  if (idx === -1) return null

  customers[idx] = {
    ...customers[idx],
    ...patchData,
  }
  localStorage.setItem(STORAGE_KEYS.CUSTOMERS, JSON.stringify(customers))
  return customers[idx]
}

// -------------------------------------------------------------
// TRANSACTIONS CRUD
// -------------------------------------------------------------
export function getOfflineTransactions() {
  initOfflineStore()
  return JSON.parse(localStorage.getItem(STORAGE_KEYS.TRANSACTIONS) || '[]')
}

export function saveOfflineTransaction(payload) {
  initOfflineStore()
  const transactions = getOfflineTransactions()
  const products = getOfflineProducts()
  const customers = getOfflineCustomers()

  const newId =
    transactions.length > 0 ? Math.max(...transactions.map((t) => t.id || 0)) + 1 : 1001
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
        cust.total_utang = Math.max(
          0,
          parseFloat(cust.total_utang || 0) - parseFloat(payload.amount_paid || 0),
        ).toFixed(2)
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
