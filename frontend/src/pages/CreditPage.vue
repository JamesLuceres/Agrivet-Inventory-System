<template>
  <q-page class="q-pa-lg">
    <!-- Header -->
    <div class="row items-center q-mb-lg">
      <q-btn flat round dense icon="arrow_back" size="lg" color="orange-10" class="q-mr-md" @click="$router.push('/')">
        <q-tooltip>Back to Dashboard</q-tooltip>
      </q-btn>
      <q-icon name="payment" size="lg" color="orange-10" class="q-mr-sm" />
      <h1 class="text-h4 text-weight-bold text-orange-10 q-my-none">Credit Tracker (Utang Log)</h1>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- 1. LEFT COLUMN: CUSTOMERS LIST -->
      <div class="col-12 col-md-6 col-lg-5">
        <q-card flat bordered class="bg-white shadow-1 fit-height">
          <q-card-section class="q-pb-none">
            <div class="text-h6 text-weight-bold text-indigo-10 q-mb-md">Customer Ledgers</div>
            <!-- Search bar -->
            <q-input
              v-model="searchQuery"
              placeholder="Search customers by name..."
              outlined
              dense
              clearable
              class="q-mb-md"
            >
              <template v-slot:prepend>
                <q-icon name="search" />
              </template>
            </q-input>
          </q-card-section>

          <q-separator />

          <!-- Customer Cards List -->
          <q-card-section class="q-pa-none scroll-container" style="max-height: 60vh;">
            <div v-if="filteredCustomers.length === 0" class="text-center text-grey-6 q-py-xl">
              <q-icon name="people" size="xl" class="q-mb-sm" />
              <div>No customers matching criteria.</div>
            </div>

            <q-list separator v-else>
              <q-item
                v-for="customer in filteredCustomers"
                :key="customer.id"
                clickable
                v-ripple
                :active="selectedCustomer?.id === customer.id"
                active-class="bg-orange-1 text-orange-10"
                @click="selectCustomer(customer)"
                class="q-py-md"
              >
                <q-item-section avatar>
                  <q-avatar color="orange-2" text-color="orange-10" icon="person" />
                </q-item-section>

                <q-item-section>
                  <q-item-label class="text-subtitle1 text-weight-bold">{{ customer.name }}</q-item-label>
                  <q-item-label caption class="text-grey-7" v-if="customer.contact_number">
                    📞 {{ customer.contact_number }}
                  </q-item-label>
                  <q-item-label caption class="ellipsis text-grey-6" v-if="customer.notes">
                    Note: {{ customer.notes }}
                  </q-item-label>
                </q-item-section>

                <q-item-section side class="text-right">
                  <q-item-label class="text-subtitle1 text-weight-bold text-red-10">
                    ₱{{ parseFloat(customer.total_utang).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                  </q-item-label>
                  <div class="row q-gutter-xs q-mt-xs justify-end">
                    <q-btn
                      color="positive"
                      size="sm"
                      label="Bayad"
                      icon="payments"
                      @click.stop="openPaymentDialog(customer)"
                      :disable="parseFloat(customer.total_utang) <= 0"
                    />
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>
        </q-card>
      </div>

      <!-- 2. RIGHT COLUMN: CREDIT TRANSACTION HISTORY -->
      <div class="col-12 col-md-6 col-lg-7">
        <q-card flat bordered class="bg-white shadow-1 fit-height">
          <q-card-section class="q-py-md">
            <div class="text-h6 text-weight-bold text-indigo-10">
              {{ selectedCustomer ? `${selectedCustomer.name}'s Account History` : 'Select a customer to view ledger history' }}
            </div>
          </q-card-section>

          <q-separator />

          <q-card-section class="q-pa-md" v-if="!selectedCustomer">
            <div class="text-center text-grey-6 q-py-xl">
              <q-icon name="history" size="xl" class="q-mb-sm" />
              <div>Click on a customer ledger in the list to view their invoices and transaction histories.</div>
            </div>
          </q-card-section>

          <!-- History Table -->
          <q-card-section class="q-pa-none" v-else>
            <q-table
              :rows="customerTransactions"
              :columns="columns"
              row-key="id"
              flat
              no-data-label="No transactions recorded for this customer."
              :rows-per-page-options="[5, 10, 20]"
            >
              <!-- Time Column -->
              <template v-slot:body-cell-created_at="props">
                <q-td :props="props">
                  {{ formatDate(props.value) }}
                </q-td>
              </template>

              <!-- Total Amount Column -->
              <template v-slot:body-cell-total_amount="props">
                <q-td :props="props" class="text-weight-bold">
                  ₱{{ parseFloat(props.value).toFixed(2) }}
                </q-td>
              </template>

              <!-- Amount Paid Column -->
              <template v-slot:body-cell-amount_paid="props">
                <q-td :props="props" class="text-green-10">
                  ₱{{ parseFloat(props.value).toFixed(2) }}
                </q-td>
              </template>

              <!-- Unpaid Balance Column -->
              <template v-slot:body-cell-unpaid_balance="props">
                <q-td :props="props" class="text-red-10 text-weight-bold">
                  ₱{{ (parseFloat(props.row.total_amount) - parseFloat(props.row.amount_paid)).toFixed(2) }}
                </q-td>
              </template>
            </q-table>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Record Payment Dialog -->
    <q-dialog v-model="paymentDialog.open">
      <q-card style="width: 400px; max-width: 90vw;">
        <q-card-section class="bg-indigo-10 text-white q-py-md">
          <div class="text-h6 text-weight-bold">Record Payment (Bayad)</div>
          <div class="text-subtitle2">{{ paymentDialog.customerName }}</div>
        </q-card-section>

        <q-card-section class="q-py-md">
          <!-- Outstanding -->
          <div class="row justify-between items-center q-mb-md bg-grey-2 q-pa-md rounded-borders">
            <div class="text-subtitle1 text-grey-8">Outstanding Debt:</div>
            <div class="text-h6 text-weight-bold text-red-10">
              ₱{{ parseFloat(paymentDialog.maxAmount).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
            </div>
          </div>

          <!-- Input Payment -->
          <q-input
            v-model.number="paymentAmount"
            type="number"
            step="0.01"
            label="Payment Amount (₱)"
            outlined
            dense
            prefix="₱"
            class="q-mb-sm"
            :rules="[
              val => !!val || 'Amount is required',
              val => val > 0 || 'Amount must be greater than 0',
              val => val <= paymentDialog.maxAmount || 'Amount cannot exceed outstanding balance'
            ]"
          />
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            label="Post Payment"
            color="positive"
            @click="submitPayment"
            :disable="paymentAmount <= 0 || paymentAmount > paymentDialog.maxAmount"
          />
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
const customers = ref([])
const transactions = ref([])
const selectedCustomer = ref(null)

// Filtering & Payment Inputs
const searchQuery = ref('')
const paymentAmount = ref(null)

// Payment modal state
const paymentDialog = ref({
  open: false,
  customerId: null,
  customerName: '',
  maxAmount: 0.0
})

// Filtered Customer list
const filteredCustomers = computed(() => {
  return customers.value.filter(customer => {
    return customer.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  })
})

// Transactions for selected customer
const customerTransactions = computed(() => {
  if (!selectedCustomer.value) return []
  return transactions.value.filter(tx => tx.customer === selectedCustomer.value.id)
})

const columns = [
  { name: 'id', label: 'Receipt ID', field: 'id', align: 'left', sortable: true },
  { name: 'created_at', label: 'Date/Time', field: 'created_at', align: 'left', sortable: true },
  { name: 'total_amount', label: 'Total Invoiced', field: 'total_amount', align: 'right', sortable: true },
  { name: 'amount_paid', label: 'Paid Down', field: 'amount_paid', align: 'right', sortable: true },
  { name: 'unpaid_balance', label: 'Unpaid Balance', field: 'id', align: 'right', sortable: true }
]

// API Requests
async function fetchData() {
  try {
    const custRes = await api.get('customers/')
    customers.value = custRes.data

    const txRes = await api.get('transactions/')
    transactions.value = txRes.data

    // Keep selected customer synchronized if it is open
    if (selectedCustomer.value) {
      const match = customers.value.find(c => c.id === selectedCustomer.value.id)
      if (match) {
        selectedCustomer.value = match
      }
    }
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to synchronize credit database.',
      icon: 'error'
    })
  }
}

// Select Customer helper
function selectCustomer(customer) {
  selectedCustomer.value = customer
}

// Open Payment Dialog helper
function openPaymentDialog(customer) {
  paymentDialog.value.customerId = customer.id
  paymentDialog.value.customerName = customer.name
  paymentDialog.value.maxAmount = parseFloat(customer.total_utang)
  paymentAmount.value = parseFloat(customer.total_utang) // Autofill with max outstanding
  paymentDialog.value.open = true
}

// Post payment adjustment
async function submitPayment() {
  try {
    const currentUtang = paymentDialog.value.maxAmount
    const reduction = parseFloat(paymentAmount.value)
    const newUtang = currentUtang - reduction

    // PATCH update to customer total_utang
    await api.patch(`customers/${paymentDialog.value.customerId}/`, {
      total_utang: newUtang.toFixed(2)
    })

    // Also register this cash receipt by posting a dummy Transaction representing the debt payment
    // E.g., CASH payment of amount 'reduction' associated with customer
    await api.post('transactions/', {
      transaction_type: 'CASH',
      customer: paymentDialog.value.customerId,
      total_amount: reduction.toFixed(2),
      amount_paid: reduction.toFixed(2),
      change_given: '0.00',
      items: [] // No items, represents a payment ledger record
    })

    $q.notify({
      color: 'positive',
      message: `Payment of ₱${reduction.toFixed(2)} recorded for ${paymentDialog.value.customerName}!`,
      icon: 'payments'
    })

    paymentDialog.value.open = false
    paymentAmount.value = null
    fetchData() // Refresh ledgers
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to record payment transaction.',
      icon: 'error'
    })
  }
}

// Format Date string
function formatDate(dateTimeStr) {
  if (!dateTimeStr) return ''
  const date = new Date(dateTimeStr)
  return date.toLocaleString([], { month: 'short', day: '2-digit', hour: '2-digit', minute: '2-digit' })
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
}
.bg-orange-1 {
  background-color: #fff3e0 !important;
}
.bg-indigo-10 {
  background-color: #1a237e !important;
}
.bg-grey-2 {
  background-color: #f5f5f5 !important;
}
.rounded-borders {
  border-radius: 6px;
}
</style>
