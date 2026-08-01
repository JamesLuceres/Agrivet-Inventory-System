<template>
  <q-page class="q-pa-lg">
    <!-- Header -->
    <div class="row items-center q-mb-lg justify-between">
      <div class="row items-center">
        <q-btn flat round dense icon="arrow_back" size="lg" color="indigo-10" class="q-mr-md" @click="$router.push('/')">
          <q-tooltip>Back to Dashboard</q-tooltip>
        </q-btn>
        <q-icon name="bar_chart" size="lg" color="indigo-10" class="q-mr-sm" />
        <h1 class="text-h4 text-weight-bold text-indigo-10 q-my-none">Sales Tracker</h1>
      </div>
      <div>
        <q-btn flat color="indigo-10" icon="refresh" label="Refresh Data" @click="refreshData" />
      </div>
    </div>

    <!-- Tabs Header -->
    <q-tabs
      v-model="tab"
      class="text-indigo-10 bg-white shadow-1 rounded-borders q-mb-lg"
      active-color="primary"
      indicator-color="primary"
      align="justify"
      bordered
    >
      <q-tab name="daily" icon="today" label="Daily Sales Report" />
      <q-tab name="monthly" icon="calendar_month" label="Monthly Sales Report" />
    </q-tabs>

    <!-- Tab Panels -->
    <q-tab-panels v-model="tab" animated class="bg-transparent">
      <!-- 1. DAILY SALES PANEL -->
      <q-tab-panel name="daily" class="q-pa-none">
        <!-- Daily Metrics Grid -->
        <div class="row q-col-gutter-md q-mb-lg">
          <!-- Total Cash Sales -->
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-white q-pa-md shadow-1">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-grey-7 text-subtitle2 text-uppercase text-weight-bold">Total Cash Sales</div>
                  <div class="text-h4 text-weight-bold text-green-10 q-mt-xs">
                    ₱{{ totalCashSales.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                  </div>
                </div>
                <q-icon name="payments" size="md" color="positive" class="bg-green-1 q-pa-md rounded-borders" />
              </div>
            </q-card>
          </div>

          <!-- Total Credit (Utang) -->
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-white q-pa-md shadow-1">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-grey-7 text-subtitle2 text-uppercase text-weight-bold">Total Credit Issued</div>
                  <div class="text-h4 text-weight-bold text-orange-10 q-mt-xs">
                    ₱{{ totalCreditGiven.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                  </div>
                </div>
                <q-icon name="assignment_late" size="md" color="warning" class="bg-orange-1 q-pa-md rounded-borders" />
              </div>
            </q-card>
          </div>

          <!-- Cash on Hand -->
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-white q-pa-md shadow-1">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-grey-7 text-subtitle2 text-uppercase text-weight-bold">Cash on Hand</div>
                  <div class="text-h4 text-weight-bold text-indigo-10 q-mt-xs">
                    ₱{{ cashOnHand.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                  </div>
                </div>
                <q-icon name="account_balance_wallet" size="md" color="primary" class="bg-indigo-1 q-pa-md rounded-borders" />
              </div>
            </q-card>
          </div>

          <!-- Total Transactions -->
          <div class="col-12 col-sm-6 col-md-3">
            <q-card flat bordered class="bg-white q-pa-md shadow-1">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-grey-7 text-subtitle2 text-uppercase text-weight-bold">Total Transactions</div>
                  <div class="text-h4 text-weight-bold text-purple-10 q-mt-xs">
                    {{ todayTransactions.length }}
                  </div>
                </div>
                <q-icon name="receipt_long" size="md" color="purple" class="bg-purple-1 q-pa-md rounded-borders" />
              </div>
            </q-card>
          </div>
        </div>

        <!-- Today's Transactions Table -->
        <q-card flat bordered class="bg-white shadow-1">
          <q-card-section class="q-py-md">
            <div class="text-h6 text-weight-bold text-indigo-10">Today's Transactions</div>
          </q-card-section>
          
          <q-separator />

          <q-table
            :rows="todayTransactions"
            :columns="dailyColumns"
            row-key="id"
            flat
            no-data-label="No transactions recorded today."
            :rows-per-page-options="[10, 20, 50]"
          >
            <!-- Type Column -->
            <template v-slot:body-cell-transaction_type="props">
              <q-td :props="props">
                <q-badge :color="props.value === 'CASH' ? 'positive' : 'warning'" text-color="white" class="text-weight-bold">
                  {{ props.value }}
                </q-badge>
              </q-td>
            </template>

            <!-- Customer Column -->
            <template v-slot:body-cell-customer_name="props">
              <q-td :props="props">
                {{ props.value || 'Walk-in Guest' }}
              </q-td>
            </template>

            <!-- Created At (Time) Column -->
            <template v-slot:body-cell-created_at="props">
              <q-td :props="props">
                {{ formatTime(props.value) }}
              </q-td>
            </template>

            <!-- Total Amount Column -->
            <template v-slot:body-cell-total_amount="props">
              <q-td :props="props">
                ₱{{ parseFloat(props.value).toFixed(2) }}
              </q-td>
            </template>

            <!-- Amount Paid Column -->
            <template v-slot:body-cell-amount_paid="props">
              <q-td :props="props">
                ₱{{ parseFloat(props.value).toFixed(2) }}
              </q-td>
            </template>

            <!-- Action Column -->
            <template v-slot:body-cell-actions="props">
              <q-td :props="props" align="center">
                <q-btn
                  flat
                  round
                  dense
                  color="primary"
                  icon="visibility"
                  @click="viewTransactionDetails(props.row)"
                >
                  <q-tooltip>View Items</q-tooltip>
                </q-btn>
              </q-td>
            </template>
          </q-table>
        </q-card>
      </q-tab-panel>

      <!-- 2. MONTHLY SALES PANEL -->
      <q-tab-panel name="monthly" class="q-pa-none">
        <!-- Selection Filters Card -->
        <q-card flat bordered class="bg-white q-pa-md q-mb-lg shadow-1">
          <div class="row q-col-gutter-md items-center">
            <div class="col-12 col-sm-4 text-h6 text-weight-bold text-indigo-10">
              Select Month & Year
            </div>
            <!-- Month Dropdown -->
            <div class="col-6 col-sm-4">
              <q-select
                v-model="selectedMonth"
                :options="monthOptions"
                label="Month"
                outlined
                emit-value
                map-options
                dense
                @update:model-value="fetchMonthlySummary"
              />
            </div>
            <!-- Year Dropdown -->
            <div class="col-6 col-sm-4">
              <q-select
                v-model="selectedYear"
                :options="yearOptions"
                label="Year"
                outlined
                dense
                @update:model-value="fetchMonthlySummary"
              />
            </div>
          </div>
        </q-card>

        <!-- Monthly Metrics Grid -->
        <div class="row q-col-gutter-md q-mb-lg">
          <!-- Total Monthly Revenue -->
          <div class="col-12 col-md-4">
            <q-card flat bordered class="bg-white q-pa-md shadow-1">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-grey-7 text-subtitle2 text-uppercase text-weight-bold">Total Monthly Revenue</div>
                  <div class="text-h4 text-weight-bold text-indigo-10 q-mt-xs">
                    ₱{{ monthlySummary.total_revenue.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                  </div>
                </div>
                <q-icon name="trending_up" size="md" color="primary" class="bg-indigo-1 q-pa-md rounded-borders" />
              </div>
            </q-card>
          </div>

          <!-- Total Monthly Credit Issued -->
          <div class="col-12 col-md-4">
            <q-card flat bordered class="bg-white q-pa-md shadow-1">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-grey-7 text-subtitle2 text-uppercase text-weight-bold">Monthly Credit Issued</div>
                  <div class="text-h4 text-weight-bold text-orange-10 q-mt-xs">
                    ₱{{ monthlySummary.total_credit_issued.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
                  </div>
                </div>
                <q-icon name="credit_card" size="md" color="warning" class="bg-orange-1 q-pa-md rounded-borders" />
              </div>
            </q-card>
          </div>

          <!-- Monthly Transaction Count -->
          <div class="col-12 col-md-4">
            <q-card flat bordered class="bg-white q-pa-md shadow-1">
              <div class="row items-center justify-between">
                <div>
                  <div class="text-grey-7 text-subtitle2 text-uppercase text-weight-bold">Transaction Count</div>
                  <div class="text-h4 text-weight-bold text-purple-10 q-mt-xs">
                    {{ monthlySummary.transaction_count }}
                  </div>
                </div>
                <q-icon name="bar_chart" size="md" color="purple" class="bg-purple-1 q-pa-md rounded-borders" />
              </div>
            </q-card>
          </div>
        </div>

        <!-- Daily Breakdown Table -->
        <q-card flat bordered class="bg-white shadow-1">
          <q-card-section class="q-py-md">
            <div class="text-h6 text-weight-bold text-indigo-10">Daily Breakdown for {{ getMonthName(selectedMonth) }} {{ selectedYear }}</div>
          </q-card-section>
          
          <q-separator />

          <q-table
            :rows="monthlySummary.daily_breakdown"
            :columns="monthlyColumns"
            row-key="date"
            flat
            no-data-label="No data available for this month."
            :rows-per-page-options="[15, 31]"
          >
            <!-- Date Column -->
            <template v-slot:body-cell-date="props">
              <q-td :props="props" class="text-weight-medium">
                {{ formatDateString(props.value) }}
              </q-td>
            </template>

            <!-- Cash Revenue Column -->
            <template v-slot:body-cell-cash_revenue="props">
              <q-td :props="props">
                ₱{{ props.value.toFixed(2) }}
              </q-td>
            </template>

            <!-- Credit Issued Column -->
            <template v-slot:body-cell-credit_given="props">
              <q-td :props="props">
                ₱{{ props.value.toFixed(2) }}
              </q-td>
            </template>

            <!-- Daily Total Column -->
            <template v-slot:body-cell-daily_total="props">
              <q-td :props="props" class="text-weight-bold text-indigo-10">
                ₱{{ (props.row.cash_revenue + props.row.credit_given).toFixed(2) }}
              </q-td>
            </template>
          </q-table>
        </q-card>
      </q-tab-panel>
    </q-tab-panels>

    <!-- Detailed Transaction Dialog -->
    <q-dialog v-model="detailsDialog.open">
      <q-card style="width: 500px; max-width: 90vw;">
        <q-card-section class="bg-indigo-10 text-white q-py-md">
          <div class="text-h6 text-weight-bold">Receipt details #{{ detailsDialog.tx.id }}</div>
          <div class="text-subtitle2">{{ formatTime(detailsDialog.tx.created_at) }} • {{ detailsDialog.tx.transaction_type }}</div>
        </q-card-section>

        <q-card-section class="q-py-md">
          <!-- Summary Details -->
          <div class="row q-col-gutter-xs q-mb-md">
            <div class="col-6 text-grey-7">Customer:</div>
            <div class="col-6 text-weight-bold text-right">{{ detailsDialog.tx.customer_name || 'Walk-in Guest' }}</div>

            <div class="col-6 text-grey-7">Payment Type:</div>
            <div class="col-6 text-weight-bold text-right text-uppercase">{{ detailsDialog.tx.transaction_type }}</div>
          </div>

          <q-separator class="q-my-sm" />

          <!-- Items Table -->
          <div class="text-weight-bold text-indigo-10 q-mb-sm">Items Purchased</div>
          <q-list bordered separator class="rounded-borders">
            <q-item v-for="item in detailsDialog.tx.items" :key="item.id" class="q-py-sm">
              <q-item-section>
                <q-item-label class="text-weight-bold">{{ item.product_name }}</q-item-label>
                <q-item-label caption>{{ item.quantity }} {{ item.unit_type }}(s) @ ₱{{ parseFloat(item.unit_price).toFixed(2) }}</q-item-label>
              </q-item-section>
              <q-item-section side class="text-weight-bold text-dark">
                ₱{{ parseFloat(item.subtotal).toFixed(2) }}
              </q-item-section>
            </q-item>
          </q-list>

          <q-separator class="q-my-md" />

          <!-- Financial Breakdown -->
          <div class="row q-col-gutter-xs text-subtitle1">
            <div class="col-6 text-grey-8">Total Amount:</div>
            <div class="col-6 text-weight-bold text-right">₱{{ parseFloat(detailsDialog.tx.total_amount).toFixed(2) }}</div>

            <div class="col-6 text-grey-8">Amount Tendered:</div>
            <div class="col-6 text-weight-bold text-right text-green-10">₱{{ parseFloat(detailsDialog.tx.amount_paid).toFixed(2) }}</div>

            <div class="col-6 text-grey-8">{{ detailsDialog.tx.transaction_type === 'CASH' ? 'Change Given:' : 'Remaining Balance:' }}</div>
            <div class="col-6 text-weight-bold text-right" :class="detailsDialog.tx.transaction_type === 'CASH' ? 'text-indigo-10' : 'text-orange-10'">
              ₱{{ detailsDialog.tx.transaction_type === 'CASH' ? parseFloat(detailsDialog.tx.change_given).toFixed(2) : (parseFloat(detailsDialog.tx.total_amount) - parseFloat(detailsDialog.tx.amount_paid)).toFixed(2) }}
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Close" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from 'boot/axios'

const tab = ref('daily')

// State variables
const allTransactions = ref([])
const totalCashSales = ref(0.0)
const totalCreditGiven = ref(0.0)
const cashOnHand = ref(0.0)

// Filters for monthly view
const selectedYear = ref(new Date().getFullYear())
const selectedMonth = ref(new Date().getMonth() + 1) // 1-indexed

const monthlySummary = ref({
  total_revenue: 0.0,
  total_credit_issued: 0.0,
  transaction_count: 0,
  daily_breakdown: []
})

// Detailed Transaction Modal state
const detailsDialog = ref({
  open: false,
  tx: {}
})

// Dropdown options
const yearOptions = ref([2024, 2025, 2026, 2027])
const monthOptions = ref([
  { label: 'January', value: 1 },
  { label: 'February', value: 2 },
  { label: 'March', value: 3 },
  { label: 'April', value: 4 },
  { label: 'May', value: 5 },
  { label: 'June', value: 6 },
  { label: 'July', value: 7 },
  { label: 'August', value: 8 },
  { label: 'September', value: 9 },
  { label: 'October', value: 10 },
  { label: 'November', value: 11 },
  { label: 'December', value: 12 }
])

// Columns definitions
const dailyColumns = [
  { name: 'id', label: 'Receipt ID', field: 'id', align: 'left', sortable: true },
  { name: 'created_at', label: 'Time', field: 'created_at', align: 'left', sortable: true },
  { name: 'transaction_type', label: 'Type', field: 'transaction_type', align: 'center', sortable: true },
  { name: 'customer_name', label: 'Customer', field: 'customer_name', align: 'left', sortable: true },
  { name: 'total_amount', label: 'Total Cost', field: 'total_amount', align: 'right', sortable: true },
  { name: 'amount_paid', label: 'Amount Paid', field: 'amount_paid', align: 'right', sortable: true },
  { name: 'actions', label: 'Actions', field: 'id', align: 'center' }
]

const monthlyColumns = [
  { name: 'date', label: 'Date', field: 'date', align: 'left', sortable: true },
  { name: 'cash_revenue', label: 'Cash Sales', field: 'cash_revenue', align: 'right', sortable: true },
  { name: 'credit_given', label: 'Credit Given', field: 'credit_given', align: 'right', sortable: true },
  { name: 'daily_total', label: 'Daily Total', field: 'cash_revenue', align: 'right', sortable: true },
  { name: 'sales_count', label: 'Sales Count', field: 'sales_count', align: 'center', sortable: true }
]

// Computed: filter transactions that occurred today (client timezone match)
const todayTransactions = computed(() => {
  const todayStr = new Date().toLocaleDateString('en-CA') // Format YYYY-MM-DD
  return allTransactions.value.filter(tx => {
    // tx.created_at format: YYYY-MM-DDTHH:mm:ss.sssZ
    return tx.created_at.startsWith(todayStr)
  })
})

// Fetch daily metrics and transactions
async function fetchDailyData() {
  try {
    // 1. Fetch raw transaction log list to display individual rows
    const txRes = await api.get('transactions/')
    allTransactions.value = txRes.data

    // 2. Fetch daily aggregates
    const dailyRes = await api.get('transactions/daily-summary/')
    totalCashSales.value = dailyRes.data.total_cash_revenue
    totalCreditGiven.value = dailyRes.data.total_credit_given

    // 3. Compute Cash on Hand (Sum of paid amounts for today's transactions)
    cashOnHand.value = todayTransactions.value.reduce((sum, tx) => sum + parseFloat(tx.amount_paid || 0), 0)
  } catch (error) {
    console.error('Failed to fetch daily sales data:', error)
  }
}

// Fetch monthly summaries
async function fetchMonthlySummary() {
  try {
    const res = await api.get(`transactions/monthly-summary/`, {
      params: {
        year: selectedYear.value,
        month: selectedMonth.value
      }
    })
    monthlySummary.value = res.data
  } catch (error) {
    console.error('Failed to fetch monthly summary data:', error)
  }
}

// Dialog helper
function viewTransactionDetails(tx) {
  detailsDialog.value.tx = tx
  detailsDialog.value.open = true
}

function refreshData() {
  if (tab.value === 'daily') {
    fetchDailyData()
  } else {
    fetchMonthlySummary()
  }
}

// Formatting helpers
function formatTime(dateTimeStr) {
  if (!dateTimeStr) return ''
  const date = new Date(dateTimeStr)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true })
}

function formatDateString(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString([], { month: 'short', day: '2-digit', weekday: 'short' })
}

function getMonthName(monthNumber) {
  const match = monthOptions.value.find(m => m.value === monthNumber)
  return match ? match.label : ''
}

onMounted(() => {
  fetchDailyData()
  fetchMonthlySummary()
})
</script>

<style scoped>
h1 {
  font-size: 2rem;
  line-height: 2.5rem;
}
.rounded-borders {
  border-radius: 8px;
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
.bg-purple-1 {
  background-color: #f3e5f5 !important;
}
</style>
