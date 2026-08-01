<template>
  <q-page class="q-pa-lg">
    <!-- Header -->
    <div class="row items-center q-mb-lg">
      <q-btn flat round dense icon="arrow_back" size="lg" color="green-10" class="q-mr-md" @click="$router.push('/')">
        <q-tooltip>Back to Dashboard</q-tooltip>
      </q-btn>
      <q-icon name="shopping_cart" size="lg" color="green-10" class="q-mr-sm" />
      <h1 class="text-h4 text-weight-bold text-green-10 q-my-none">Pay (Checkout Register)</h1>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- 1. LEFT COLUMN: PRODUCT SEARCH & CATALOG -->
      <div class="col-12 col-md-7 col-lg-8">
        <q-card flat bordered class="bg-white shadow-1 fit-height">
          <q-card-section class="q-pb-none">
            <div class="text-h6 text-weight-bold text-indigo-10 q-mb-md">Product Catalog</div>
            <div class="row q-col-gutter-sm q-mb-md">
              <!-- Search Bar -->
              <div class="col-12 col-sm-8">
                <q-input
                  v-model="searchQuery"
                  placeholder="Search products by name..."
                  outlined
                  dense
                  clearable
                >
                  <template v-slot:prepend>
                    <q-icon name="search" />
                  </template>
                </q-input>
              </div>
              <!-- Category Filter -->
              <div class="col-12 col-sm-4">
                <q-select
                  v-model="selectedCategory"
                  :options="categoryOptions"
                  label="Category"
                  outlined
                  dense
                  emit-value
                  map-options
                />
              </div>
            </div>
          </q-card-section>

          <q-separator />

          <!-- Products Grid -->
          <q-card-section class="q-pa-md scroll-container">
            <div v-if="filteredProducts.length === 0" class="text-center text-grey-6 q-py-xl">
              <q-icon name="inventory_2" size="xl" class="q-mb-sm" />
              <div>No products found matching the criteria.</div>
            </div>
            
            <div class="row q-col-gutter-md">
              <div
                v-for="product in filteredProducts"
                :key="product.id"
                class="col-12 col-sm-6 col-md-6 col-lg-4"
              >
                <q-card flat bordered class="product-item-card hover-grow q-pa-sm">
                  <q-card-section class="q-pa-sm">
                    <div class="text-subtitle1 text-weight-bold text-indigo-10 ellipsis">{{ product.name }}</div>
                    <q-badge color="indigo-1" text-color="indigo-10" class="q-mb-xs">{{ product.category_name }}</q-badge>
                    
                    <div class="row justify-between text-caption q-mt-sm">
                      <div>Sack Stock: 
                        <span :class="parseFloat(product.stock_sacks) < product.low_stock_threshold ? 'text-red text-weight-bold' : 'text-grey-9'">
                          {{ parseFloat(product.stock_sacks) }}
                        </span>
                      </div>
                      <div>Kilo Stock: 
                        <span :class="parseFloat(product.stock_kilos) < product.low_stock_threshold ? 'text-red text-weight-bold' : 'text-grey-9'">
                          {{ parseFloat(product.stock_kilos) }}
                        </span>
                      </div>
                    </div>

                    <div class="q-mt-sm text-subtitle2">
                      <div v-if="product.price_per_sack">Sack: <span class="text-weight-bold text-green-10">₱{{ product.price_per_sack }}</span></div>
                      <div v-if="product.price_per_kilo">Kilo: <span class="text-weight-bold text-green-10">₱{{ product.price_per_kilo }}</span></div>
                    </div>
                  </q-card-section>

                  <q-separator />

                  <q-card-actions align="right" class="q-pa-xs">
                    <q-btn
                      v-if="product.price_per_kilo"
                      flat
                      color="primary"
                      label="+ Kilo"
                      icon="add_circle"
                      size="sm"
                      @click="addToCart(product, 'KILO')"
                    />
                    <q-btn
                      v-if="product.price_per_sack"
                      flat
                      color="secondary"
                      label="+ Sack"
                      icon="add_box"
                      size="sm"
                      @click="addToCart(product, 'SACK')"
                    />
                  </q-card-actions>
                </q-card>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- 2. RIGHT COLUMN: CART & BILLING -->
      <div class="col-12 col-md-5 col-lg-4">
        <q-card flat bordered class="bg-white shadow-1 flex-column fit-height">
          <q-card-section class="q-py-md row items-center justify-between">
            <div class="text-h6 text-weight-bold text-indigo-10">Cart Items</div>
            <q-btn flat dense color="negative" icon="delete_sweep" label="Clear" size="sm" @click="clearCart" :disable="cart.length === 0" />
          </q-card-section>

          <q-separator />

          <!-- Cart Items List -->
          <q-card-section class="q-pa-none flex-grow scroll-container" style="max-height: 250px;">
            <div v-if="cart.length === 0" class="text-center text-grey-6 q-py-xl">
              <q-icon name="shopping_cart" size="xl" class="q-mb-sm" />
              <div>Your cart is empty.</div>
            </div>

            <q-list separator v-else>
              <q-item v-for="(item, index) in cart" :key="index" class="q-py-sm">
                <q-item-section>
                  <q-item-section class="text-subtitle2 text-weight-bold">{{ item.product.name }}</q-item-section>
                  <q-item-label caption class="row items-center q-mt-xs">
                    <q-badge :color="item.unitType === 'SACK' ? 'secondary' : 'primary'" class="q-mr-xs text-weight-bold">
                      {{ item.unitType }}
                    </q-badge>
                    ₱{{ item.price.toFixed(2) }} / {{ item.unitType === 'SACK' ? 'sack' : 'kg' }}
                  </q-item-label>
                </q-item-section>

                <q-item-section side style="width: 140px;">
                  <div class="row no-wrap items-center justify-end">
                    <!-- Quantity Input -->
                    <q-input
                      v-model.number="item.quantity"
                      type="number"
                      step="0.1"
                      outlined
                      dense
                      class="quantity-input q-mr-sm"
                      @update:model-value="validateQuantity(item)"
                    />
                    <!-- Remove Button -->
                    <q-btn flat round color="negative" icon="remove_circle_outline" size="sm" @click="removeFromCart(index)" />
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>

          <q-separator />

          <!-- Checkout Configuration -->
          <q-card-section class="q-pa-md bg-grey-1">
            <!-- Totals -->
            <div class="row justify-between items-center q-mb-md">
              <div class="text-subtitle1 text-weight-bold text-grey-8">Grand Total:</div>
              <div class="text-h4 text-weight-bold text-green-10">₱{{ grandTotal.toFixed(2) }}</div>
            </div>

            <!-- Payment Type -->
            <div class="q-mb-md">
              <div class="text-subtitle2 text-weight-bold text-grey-8 q-mb-xs">Payment Method:</div>
              <q-btn-toggle
                v-model="paymentMethod"
                toggle-color="primary"
                flat
                bordered
                spread
                :options="[
                  { label: '💵 CASH', value: 'CASH' },
                  { label: '📋 CREDIT (Utang)', value: 'CREDIT' }
                ]"
              />
            </div>

            <!-- Conditional Inputs -->
            <!-- A. CASH TRANSACTION DETAILS -->
            <div v-if="paymentMethod === 'CASH'" class="row q-col-gutter-sm q-mb-md">
              <div class="col-12">
                <q-input
                  v-model.number="cashTendered"
                  type="number"
                  label="Cash Tendered"
                  outlined
                  dense
                  prefix="₱"
                />
              </div>
              <div class="col-12 row justify-between items-center q-mt-sm" v-if="cashTendered >= grandTotal">
                <div class="text-subtitle2 text-grey-8">Change:</div>
                <div class="text-h6 text-weight-bold text-indigo-10">₱{{ (cashTendered - grandTotal).toFixed(2) }}</div>
              </div>
            </div>

            <!-- B. CREDIT TRANSACTION DETAILS -->
            <div v-else class="q-mb-md">
              <div class="row items-center justify-between q-mb-xs">
                <div class="text-subtitle2 text-weight-bold text-grey-8">Customer Account:</div>
                <q-btn flat color="primary" icon="person_add" label="New Customer" size="xs" @click="openNewCustomerDialog" />
              </div>
              <q-select
                v-model="selectedCustomer"
                :options="customerOptions"
                outlined
                dense
                label="Select Customer"
                option-label="name"
                option-value="id"
              />
              <!-- Optional Downpayment -->
              <q-input
                v-model.number="amountPaid"
                type="number"
                label="Downpayment (Optional)"
                outlined
                dense
                prefix="₱"
                class="q-mt-sm"
              />
              <div class="row justify-between items-center q-mt-sm" v-if="selectedCustomer">
                <div class="text-subtitle2 text-grey-8">Balance to Log:</div>
                <div class="text-h6 text-weight-bold text-orange-10">₱{{ (grandTotal - (amountPaid || 0)).toFixed(2) }}</div>
              </div>
            </div>

            <!-- Checkout Submit Button -->
            <q-btn
              color="green-10"
              class="full-width text-weight-bold q-py-sm"
              size="lg"
              label="Complete Transaction"
              icon="check_circle"
              :disable="!canCheckout"
              @click="submitTransaction"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- New Customer Dialog -->
    <q-dialog v-model="customerDialog.open">
      <q-card style="width: 400px; max-width: 90vw;">
        <q-card-section class="bg-indigo-10 text-white q-py-md">
          <div class="text-h6 text-weight-bold">Add New Customer</div>
        </q-card-section>

        <q-card-section class="q-py-md row q-col-gutter-sm">
          <div class="col-12">
            <q-input v-model="customerDialog.name" label="Customer Name" outlined dense />
          </div>
          <div class="col-12">
            <q-input v-model="customerDialog.contact" label="Contact Number" outlined dense />
          </div>
          <div class="col-12">
            <q-input v-model="customerDialog.notes" label="Notes" outlined dense type="textarea" rows="3" />
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn label="Save Customer" color="primary" @click="saveNewCustomer" :disable="!customerDialog.name" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()

// State lists
const products = ref([])
const customers = ref([])
const categories = ref([])

// Filtering state
const searchQuery = ref('')
const selectedCategory = ref(null)

// Cart & Checkout state
const cart = ref([])
const paymentMethod = ref('CASH')
const cashTendered = ref(null)
const selectedCustomer = ref(null)
const amountPaid = ref(null)

// Dialog state
const customerDialog = ref({
  open: false,
  name: '',
  contact: '',
  notes: ''
})

// Options mappings
const categoryOptions = computed(() => {
  const list = categories.value.map(cat => ({ label: cat.name, value: cat.id }))
  return [{ label: 'All Categories', value: null }, ...list]
})

const customerOptions = computed(() => {
  return customers.value
})

// Filtered products list
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === null || product.category === selectedCategory.value
    return matchesSearch && matchesCategory && product.is_active
  })
})

// Cart calculations
const grandTotal = computed(() => {
  return cart.value.reduce((sum, item) => sum + (item.quantity * item.price), 0)
})

const canCheckout = computed(() => {
  if (cart.value.length === 0) return false
  if (paymentMethod.value === 'CASH') {
    return cashTendered.value >= grandTotal.value
  } else {
    // CREDIT
    return selectedCustomer.value !== null
  }
})

// API Calls
async function fetchData() {
  try {
    const prodRes = await api.get('products/')
    products.value = prodRes.data

    const custRes = await api.get('customers/')
    customers.value = custRes.data

    const catRes = await api.get('categories/')
    categories.value = catRes.data
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to sync database data.',
      icon: 'report_problem'
    })
  }
}

// Add Item
function addToCart(product, unitType) {
  const price = unitType === 'SACK' ? parseFloat(product.price_per_sack) : parseFloat(product.price_per_kilo)
  
  // Check if item already exists in cart with same unit type
  const existingIndex = cart.value.findIndex(item => item.product.id === product.id && item.unitType === unitType)
  
  if (existingIndex > -1) {
    cart.value[existingIndex].quantity += 1
  } else {
    cart.value.push({
      product,
      unitType,
      quantity: 1,
      price
    })
  }

  $q.notify({
    color: 'indigo-10',
    message: `${product.name} (${unitType}) added.`,
    icon: 'shopping_basket',
    timeout: 1000
  })
}

function removeFromCart(index) {
  cart.value.splice(index, 1)
}

function clearCart() {
  cart.value = []
  cashTendered.value = null
  selectedCustomer.value = null
  amountPaid.value = null
}

function validateQuantity(item) {
  if (item.quantity <= 0 || isNaN(item.quantity)) {
    item.quantity = 1
  }
}

// Dialog management
function openNewCustomerDialog() {
  customerDialog.value.name = ''
  customerDialog.value.contact = ''
  customerDialog.value.notes = ''
  customerDialog.value.open = true
}

async function saveNewCustomer() {
  try {
    const res = await api.post('customers/', {
      name: customerDialog.value.name,
      contact_number: customerDialog.value.contact,
      notes: customerDialog.value.notes
    })
    customers.value.push(res.data)
    selectedCustomer.value = res.data // Set as active
    customerDialog.value.open = false
    $q.notify({
      color: 'positive',
      message: `Customer ${res.data.name} added!`,
      icon: 'person'
    })
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to create new customer.',
      icon: 'error'
    })
  }
}

// Submit Transaction
async function submitTransaction() {
  try {
    const payload = {
      transaction_type: paymentMethod.value,
      customer: paymentMethod.value === 'CREDIT' ? selectedCustomer.value.id : null,
      total_amount: grandTotal.value,
      amount_paid: paymentMethod.value === 'CASH' ? grandTotal.value : (amountPaid.value || 0.00),
      change_given: paymentMethod.value === 'CASH' ? (cashTendered.value - grandTotal.value) : 0.00,
      items: cart.value.map(item => ({
        product: item.product.id,
        unit_type: item.unitType,
        quantity: item.quantity,
        unit_price: item.price,
        subtotal: item.quantity * item.price
      }))
    }

    await api.post('transactions/', payload)
    
    $q.notify({
      color: 'positive',
      message: 'Transaction completed successfully!',
      icon: 'check_circle'
    })

    clearCart()
    fetchData() // Refresh stock levels
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to complete transaction. Check stock limits.',
      icon: 'error'
    })
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
h1 {
  font-size: 2rem;
  line-height: 2.5rem;
}
.fit-height {
  height: 100%;
}
.scroll-container {
  overflow-y: auto;
  max-height: 60vh;
}
.product-item-card {
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.hover-grow:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.quantity-input {
  width: 70px;
}
.bg-indigo-10 {
  background-color: #1a237e !important;
}
.bg-indigo-1 {
  background-color: #e8eaf6 !important;
}
.bg-green-1 {
  background-color: #e8f5e9 !important;
}
.bg-orange-1 {
  background-color: #fff3e0 !important;
}
.rounded-borders {
  border-radius: 6px;
}
</style>
