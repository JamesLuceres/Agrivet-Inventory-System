<template>
  <q-page class="credit-tracker-page q-pa-lg">
    <!-- Top Action & Navigation Bar -->
    <div class="row items-center justify-between q-mb-lg q-col-gutter-y-sm">
      <div class="row items-center no-wrap">
        <q-btn
          flat
          round
          dense
          icon="arrow_back"
          size="md"
          color="slate-800"
          class="q-mr-sm back-button"
          @click="$router.push('/')"
        >
          <q-tooltip>Back to Dashboard</q-tooltip>
        </q-btn>
        <div>
          <h1 class="text-h5 text-weight-bolder text-slate-900 q-my-none tracking-tight leading-tight">
            Credit Tracker
          </h1>
          <div class="text-caption text-slate-500 font-medium">
            Customer Utang Log, Credit Balances & Collection Records
          </div>
        </div>
      </div>

      <!-- Search & New Customer Button -->
      <div class="row items-center q-gutter-sm">
        <q-input
          v-model="searchQuery"
          placeholder="Search customer ledgers by name or phone..."
          outlined
          dense
          clearable
          class="reports-search-input-long"
          style="min-width: 320px"
        >
          <template v-slot:prepend>
            <q-icon name="search" color="slate-400" size="18px" />
          </template>
        </q-input>

        <q-btn
          unelevated
          icon="person_add"
          label="Add Customer"
          class="btn-agrivet-green export-btn text-weight-bold"
          @click="openAddCustomerDialog"
        />

        <q-btn
          flat
          round
          dense
          icon="refresh"
          color="slate-600"
          class="refresh-btn"
          @click="fetchData"
        >
          <q-tooltip>Refresh Ledger Data</q-tooltip>
        </q-btn>
      </div>
    </div>

    <!-- 4 KPI Summary Metric Cards (Matching Reports Aesthetics) -->
    <div class="row q-col-gutter-md q-mb-lg items-stretch">
      <!-- Card 1: Total Outstanding Debt -->
      <div class="col-12 col-sm-6 col-lg-3 column">
        <q-card flat class="kpi-metric-card full-height bg-white">
          <div class="row items-center justify-between no-wrap">
            <div>
              <div class="text-caption text-slate-500 font-semibold text-uppercase tracking-wider">
                Total Outstanding Utang
              </div>
              <div class="kpi-metric-value text-rose-7 num-tabular q-mt-xs">
                ₱{{
                  totalOutstandingUtang.toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                }}
              </div>
              <div class="text-caption text-slate-500 q-mt-xs">Active credit receivables</div>
            </div>
            <div class="kpi-icon-squircle bg-rose-1 text-rose-7">
              <q-icon name="account_balance_wallet" size="24px" color="rose-7" />
            </div>
          </div>
        </q-card>
      </div>

      <!-- Card 2: Debtors with Balance -->
      <div class="col-12 col-sm-6 col-lg-3 column">
        <q-card flat class="kpi-metric-card full-height bg-white">
          <div class="row items-center justify-between no-wrap">
            <div>
              <div class="text-caption text-slate-500 font-semibold text-uppercase tracking-wider">
                Accounts with Balance
              </div>
              <div class="kpi-metric-value text-amber-9 num-tabular q-mt-xs">
                {{ customersWithBalanceCount }}
              </div>
              <div class="text-caption text-slate-500 q-mt-xs">Buyers owing credit</div>
            </div>
            <div class="kpi-icon-squircle bg-amber-1 text-amber-9">
              <q-icon name="people_alt" size="24px" color="amber-9" />
            </div>
          </div>
        </q-card>
      </div>

      <!-- Card 3: Total Registered Customers -->
      <div class="col-12 col-sm-6 col-lg-3 column">
        <q-card flat class="kpi-metric-card full-height bg-white">
          <div class="row items-center justify-between no-wrap">
            <div>
              <div class="text-caption text-slate-500 font-semibold text-uppercase tracking-wider">
                Registered Ledgers
              </div>
              <div class="kpi-metric-value text-slate-900 num-tabular q-mt-xs">
                {{ customers.length }}
              </div>
              <div class="text-caption text-slate-500 q-mt-xs">All buyer accounts</div>
            </div>
            <div class="kpi-icon-squircle bg-blue-1 text-blue-9">
              <q-icon name="badge" size="24px" color="blue-8" />
            </div>
          </div>
        </q-card>
      </div>

      <!-- Card 4: Total Debt Collected -->
      <div class="col-12 col-sm-6 col-lg-3 column">
        <q-card flat class="kpi-metric-card full-height bg-white">
          <div class="row items-center justify-between no-wrap">
            <div>
              <div class="text-caption text-slate-500 font-semibold text-uppercase tracking-wider">
                Total Debt Collected
              </div>
              <div class="kpi-metric-value text-emerald-9 num-tabular q-mt-xs">
                ₱{{
                  totalDebtCollected.toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                }}
              </div>
              <div class="text-caption text-slate-500 q-mt-xs">Settled collection receipts</div>
            </div>
            <div class="kpi-icon-squircle bg-emerald-1 text-emerald-9">
              <q-icon name="payments" size="24px" color="emerald-9" />
            </div>
          </div>
        </q-card>
      </div>
    </div>

    <!-- 2 Column Master-Detail Layout -->
    <div class="row q-col-gutter-lg items-start">
      <!-- 1. LEFT COLUMN: CUSTOMER LEDGERS LIST -->
      <div class="col-12 col-lg-5 column">
        <q-card flat class="data-table-card bg-white full-width">
          <!-- Card Header Banner -->
          <div
            class="q-px-md q-py-sm row items-center justify-between border-bottom-subtle bg-slate-50"
          >
            <div class="row items-center">
              <q-icon name="contacts" size="20px" color="primary" class="q-mr-sm" />
              <span class="text-subtitle2 text-weight-bold text-slate-800">Customer Ledgers</span>
              <q-badge color="emerald-1" text-color="emerald-9" class="q-ml-sm text-weight-bold">
                {{ filteredCustomers.length }} accounts
              </q-badge>
            </div>

            <!-- Quick Filter Filter Tabs -->
            <div class="row items-center q-gutter-xs">
              <q-btn
                dense
                unelevated
                size="xs"
                :color="filterMode === 'all' ? 'primary' : 'grey-3'"
                :text-color="filterMode === 'all' ? 'white' : 'grey-8'"
                label="All"
                class="q-px-sm"
                @click="filterMode = 'all'"
              />
              <q-btn
                dense
                unelevated
                size="xs"
                :color="filterMode === 'with_debt' ? 'rose-7' : 'grey-3'"
                :text-color="filterMode === 'with_debt' ? 'white' : 'grey-8'"
                label="With Utang"
                class="q-px-sm"
                @click="filterMode = 'with_debt'"
              />
              <q-btn
                dense
                unelevated
                size="xs"
                :color="filterMode === 'zero' ? 'emerald-8' : 'grey-3'"
                :text-color="filterMode === 'zero' ? 'white' : 'grey-8'"
                label="Paid / Zero"
                class="q-px-sm"
                @click="filterMode = 'zero'"
              />
            </div>
          </div>

          <!-- Customer Cards List -->
          <div class="scroll-container" style="max-height: 65vh; min-height: 380px">
            <div v-if="filteredCustomers.length === 0" class="text-center text-slate-400 q-py-xl">
              <q-icon name="people_outline" size="56px" color="slate-300" class="q-mb-sm" />
              <div class="text-body2 font-medium">No customer ledgers found matching criteria.</div>
              <div class="text-caption text-slate-400 q-mt-xs">
                Try a different search query or add a new customer.
              </div>
            </div>

            <q-list separator v-else class="customer-list">
              <q-item
                v-for="customer in filteredCustomers"
                :key="customer.id"
                clickable
                v-ripple
                :active="selectedCustomer?.id === customer.id"
                active-class="active-customer-ledger"
                @click="selectCustomer(customer)"
                class="q-py-md q-px-md customer-item-row"
              >
                <!-- Avatar -->
                <q-item-section avatar>
                  <q-avatar
                    :color="parseFloat(customer.total_utang) > 0 ? 'rose-1' : 'emerald-1'"
                    :text-color="parseFloat(customer.total_utang) > 0 ? 'rose-8' : 'emerald-8'"
                    size="42px"
                    class="text-weight-bold"
                  >
                    {{ customer.name ? customer.name.charAt(0).toUpperCase() : '?' }}
                  </q-avatar>
                </q-item-section>

                <!-- Customer Details -->
                <q-item-section>
                  <div class="row items-center no-wrap">
                    <span class="text-subtitle1 text-weight-bolder text-slate-900 ellipsis">
                      {{ customer.name }}
                    </span>
                    <q-badge
                      v-if="parseFloat(customer.total_utang) > 0"
                      color="rose-1"
                      text-color="rose-8"
                      class="q-ml-xs text-weight-bold"
                      style="font-size: 0.65rem"
                    >
                      Utang
                    </q-badge>
                    <q-badge
                      v-else
                      color="emerald-1"
                      text-color="emerald-9"
                      class="q-ml-xs text-weight-bold"
                      style="font-size: 0.65rem"
                    >
                      Clear
                    </q-badge>
                  </div>

                  <div class="row items-center text-caption text-slate-500 q-mt-xs">
                    <span v-if="customer.contact_number" class="q-mr-sm">
                      <q-icon name="call" size="13px" class="q-mr-xs text-slate-400" />
                      {{ customer.contact_number }}
                    </span>
                    <span v-if="customer.notes" class="ellipsis text-slate-400">
                      • {{ customer.notes }}
                    </span>
                  </div>
                </q-item-section>

                <!-- Balance & Action Button -->
                <q-item-section side class="text-right">
                  <div
                    class="text-subtitle1 text-weight-bolder num-tabular"
                    :class="parseFloat(customer.total_utang) > 0 ? 'text-rose-7' : 'text-slate-400'"
                  >
                    ₱{{
                      parseFloat(customer.total_utang).toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })
                    }}
                  </div>

                  <div class="row q-gutter-xs q-mt-xs justify-end items-center">
                    <q-btn
                      unelevated
                      size="sm"
                      label="Bayad"
                      icon="payments"
                      class="btn-agrivet-green text-weight-bold q-px-sm"
                      style="border-radius: 8px; font-size: 0.75rem"
                      @click.stop="openPaymentDialog(customer)"
                      :disable="parseFloat(customer.total_utang) <= 0"
                    />
                    <q-btn
                      flat
                      round
                      dense
                      icon="edit"
                      size="xs"
                      color="slate-500"
                      @click.stop="openEditCustomerDialog(customer)"
                    >
                      <q-tooltip>Edit Profile</q-tooltip>
                    </q-btn>
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </q-card>
      </div>

      <!-- 2. RIGHT COLUMN: CREDIT TRANSACTION HISTORY -->
      <div class="col-12 col-lg-7 column">
        <q-card flat class="data-table-card bg-white full-width">
          <!-- Card Header Banner -->
          <div
            class="q-px-md q-py-sm row items-center justify-between border-bottom-subtle bg-slate-50"
          >
            <div class="row items-center">
              <q-icon name="history" size="20px" color="primary" class="q-mr-sm" />
              <span class="text-subtitle2 text-weight-bold text-slate-800">
                {{
                  selectedCustomer
                    ? `${selectedCustomer.name}'s Account History`
                    : 'Customer Ledger History'
                }}
              </span>
              <q-badge
                v-if="selectedCustomer"
                color="blue-1"
                text-color="blue-9"
                class="q-ml-sm text-weight-bold"
              >
                {{ customerTransactions.length }} transactions
              </q-badge>
            </div>

            <!-- Header Quick Badge -->
            <div v-if="selectedCustomer" class="row items-center q-gutter-xs">
              <span class="text-caption text-slate-500">Balance:</span>
              <span class="text-subtitle2 text-weight-bolder text-rose-7 num-tabular">
                ₱{{
                  parseFloat(selectedCustomer.total_utang).toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                }}
              </span>
            </div>
          </div>

          <!-- Empty State when no customer selected -->
          <div v-if="!selectedCustomer" class="text-center text-slate-400 q-py-xl" style="min-height: 380px">
            <q-icon name="manage_search" size="64px" color="slate-300" class="q-mb-md" />
            <div class="text-body1 text-weight-bold text-slate-700">No Customer Selected</div>
            <div class="text-caption text-slate-400 q-mt-xs" style="max-width: 320px; margin: 0 auto">
              Select a customer from the left ledger list to inspect their recorded credit transactions, invoices, and debt payment history.
            </div>
          </div>

          <!-- Account History Content when customer selected -->
          <div v-else>
            <!-- Summary Micro-Cards Banner -->
            <div class="q-pa-md bg-slate-100 border-bottom-subtle row q-col-gutter-sm">
              <div class="col-4">
                <div class="text-caption text-slate-500 font-semibold">Total Invoiced</div>
                <div class="text-subtitle1 text-weight-bolder text-slate-800 num-tabular">
                  ₱{{ selectedCustomerTotalInvoiced.toFixed(2) }}
                </div>
              </div>
              <div class="col-4">
                <div class="text-caption text-slate-500 font-semibold">Total Paid Down</div>
                <div class="text-subtitle1 text-weight-bolder text-emerald-9 num-tabular">
                  ₱{{ selectedCustomerTotalPaid.toFixed(2) }}
                </div>
              </div>
              <div class="col-4 text-right">
                <div class="text-caption text-slate-500 font-semibold">Current Balance Due</div>
                <div class="text-subtitle1 text-weight-bolder text-rose-7 num-tabular">
                  ₱{{ parseFloat(selectedCustomer.total_utang).toFixed(2) }}
                </div>
              </div>
            </div>

            <!-- History Table -->
            <q-table
              :rows="customerTransactions"
              :columns="columns"
              row-key="id"
              flat
              separator="cell"
              class="credit-history-table"
              no-data-label="No transactions recorded for this customer yet."
              :rows-per-page-options="[10, 20, 50]"
            >
              <!-- Date Column -->
              <template v-slot:body-cell-created_at="props">
                <q-td :props="props" class="text-slate-700 font-medium">
                  {{ formatDate(props.value) }}
                </q-td>
              </template>

              <!-- Type Badge Column -->
              <template v-slot:body-cell-transaction_type="props">
                <q-td :props="props">
                  <q-badge
                    v-if="props.value === 'CREDIT'"
                    color="amber-1"
                    text-color="amber-9"
                    class="text-weight-bold"
                  >
                    <q-icon name="credit_score" size="12px" class="q-mr-xs" />
                    Credit Invoice
                  </q-badge>
                  <q-badge
                    v-else-if="props.value === 'DEBT_PAYMENT'"
                    color="emerald-1"
                    text-color="emerald-9"
                    class="text-weight-bold"
                  >
                    <q-icon name="payments" size="12px" class="q-mr-xs" />
                    Bayad
                  </q-badge>
                  <q-badge v-else color="grey-3" text-color="grey-8">
                    {{ props.value }}
                  </q-badge>
                </q-td>
              </template>

              <!-- Total Bill Column -->
              <template v-slot:body-cell-total_amount="props">
                <q-td :props="props" class="text-weight-bolder text-slate-900 num-tabular">
                  ₱{{ parseFloat(props.value).toFixed(2) }}
                </q-td>
              </template>

              <!-- Amount Paid Column -->
              <template v-slot:body-cell-amount_paid="props">
                <q-td :props="props" class="text-emerald-9 text-weight-bold num-tabular">
                  ₱{{ parseFloat(props.value).toFixed(2) }}
                </q-td>
              </template>

              <!-- Unpaid Balance Column -->
              <template v-slot:body-cell-unpaid_balance="props">
                <q-td :props="props" class="text-rose-7 text-weight-bolder num-tabular">
                  ₱{{
                    props.row.transaction_type === 'DEBT_PAYMENT'
                      ? '0.00'
                      : Math.max(
                          0,
                          parseFloat(props.row.total_amount) - parseFloat(props.row.amount_paid),
                        ).toFixed(2)
                  }}
                </q-td>
              </template>
            </q-table>
          </div>
        </q-card>
      </div>
    </div>

    <!-- Record Payment Dialog (Clean Modern Modal) -->
    <q-dialog v-model="paymentDialog.open">
      <q-card style="width: 440px; max-width: 92vw; border-radius: 16px; overflow: hidden">
        <!-- Dialog Header -->
        <q-card-section class="bg-slate-900 text-white q-py-md q-px-lg row items-center justify-between">
          <div class="row items-center">
            <div class="kpi-icon-squircle bg-emerald-9 text-white q-mr-sm" style="width: 36px; height: 36px">
              <q-icon name="payments" size="20px" />
            </div>
            <div>
              <div class="text-subtitle1 text-weight-bolder leading-tight">Record Bayad</div>
              <div class="text-caption text-slate-400">{{ paymentDialog.customerName }}</div>
            </div>
          </div>
          <q-btn flat round dense icon="close" color="white" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-lg">
          <!-- Outstanding Balance Banner -->
          <div class="outstanding-banner q-pa-md rounded-borders q-mb-md">
            <div class="text-caption text-slate-500 font-semibold text-uppercase tracking-wider">
              Total Outstanding Balance
            </div>
            <div class="text-h5 text-weight-bolder text-rose-7 num-tabular q-mt-xs">
              ₱{{
                parseFloat(paymentDialog.maxAmount).toLocaleString('en-US', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })
              }}
            </div>
          </div>

          <!-- Quick Preset Buttons -->
          <div class="text-caption text-slate-500 font-semibold q-mb-xs">Quick Amounts:</div>
          <div class="row q-gutter-xs q-mb-md">
            <q-btn
              unelevated
              size="sm"
              class="border-slate text-weight-bold"
              label="Full Balance"
              color="emerald-1"
              text-color="emerald-9"
              @click="paymentAmount = paymentDialog.maxAmount"
            />
            <q-btn
              unelevated
              size="sm"
              class="border-slate text-weight-bold"
              label="₱100"
              color="grey-2"
              text-color="grey-9"
              @click="setQuickAmount(100)"
            />
            <q-btn
              unelevated
              size="sm"
              class="border-slate text-weight-bold"
              label="₱200"
              color="grey-2"
              text-color="grey-9"
              @click="setQuickAmount(200)"
            />
            <q-btn
              unelevated
              size="sm"
              class="border-slate text-weight-bold"
              label="₱500"
              color="grey-2"
              text-color="grey-9"
              @click="setQuickAmount(500)"
            />
            <q-btn
              unelevated
              size="sm"
              class="border-slate text-weight-bold"
              label="₱1,000"
              color="grey-2"
              text-color="grey-9"
              @click="setQuickAmount(1000)"
            />
          </div>

          <!-- Input Payment Field -->
          <q-input
            v-model.number="paymentAmount"
            type="number"
            step="0.01"
            min="0.01"
            label="Payment Amount (₱)"
            outlined
            prefix="₱"
            class="text-weight-bold payment-input"
            :rules="[
              (val) => !!val || 'Amount is required',
              (val) => val > 0 || 'Amount must be greater than ₱0',
              (val) => val <= paymentDialog.maxAmount || 'Amount cannot exceed balance due',
            ]"
          />

          <!-- Calculated Remaining Balance -->
          <div
            v-if="paymentAmount && paymentAmount > 0"
            class="row justify-between items-center q-mt-xs text-caption text-slate-600 bg-slate-100 q-pa-sm rounded-borders"
          >
            <span>Remaining Balance After Payment:</span>
            <span class="text-weight-bold text-slate-900 num-tabular">
              ₱{{ Math.max(0, paymentDialog.maxAmount - paymentAmount).toFixed(2) }}
            </span>
          </div>
        </q-card-section>

        <q-separator />

        <q-card-actions align="right" class="q-px-lg q-py-md bg-slate-50">
          <q-btn flat label="Cancel" color="slate-600" class="text-weight-bold" v-close-popup />
          <q-btn
            unelevated
            label="Post Payment Receipt"
            icon="payments"
            class="btn-agrivet-green text-weight-bold export-btn"
            @click="submitPayment"
            :disable="!paymentAmount || paymentAmount <= 0 || paymentAmount > paymentDialog.maxAmount"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Add / Edit Customer Dialog -->
    <q-dialog v-model="customerDialog.open">
      <q-card style="width: 440px; max-width: 92vw; border-radius: 16px; overflow: hidden">
        <q-card-section class="bg-slate-900 text-white q-py-md q-px-lg row items-center justify-between">
          <div class="row items-center">
            <q-icon
              :name="customerDialog.editMode ? 'edit' : 'person_add'"
              size="24px"
              class="q-mr-sm text-emerald-4"
            />
            <div class="text-subtitle1 text-weight-bolder">
              {{ customerDialog.editMode ? 'Edit Customer Profile' : 'Add New Customer' }}
            </div>
          </div>
          <q-btn flat round dense icon="close" color="white" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-lg q-gutter-y-md">
          <q-input
            v-model="customerForm.name"
            label="Customer Full Name *"
            outlined
            dense
            :rules="[(val) => !!val?.trim() || 'Customer name is required']"
          />

          <q-input
            v-model="customerForm.contact_number"
            label="Contact Number (Optional)"
            outlined
            dense
            hint="e.g. 0917-123-4567"
          />

          <q-input
            v-model="customerForm.notes"
            label="Notes / Address (Optional)"
            type="textarea"
            rows="2"
            outlined
            dense
            hint="e.g. Purok 4, Mangga St."
          />
        </q-card-section>

        <q-separator />

        <q-card-actions align="right" class="q-px-lg q-py-md bg-slate-50">
          <q-btn flat label="Cancel" color="slate-600" class="text-weight-bold" v-close-popup />
          <q-btn
            unelevated
            :label="customerDialog.editMode ? 'Save Changes' : 'Create Ledger'"
            icon="check"
            class="btn-agrivet-green text-weight-bold export-btn"
            @click="saveCustomer"
            :disable="!customerForm.name?.trim()"
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
import { playChime, playWarning } from 'src/utils/audio'

const $q = useQuasar()

// State lists
const customers = ref([])
const transactions = ref([])
const selectedCustomer = ref(null)

// Filtering & Payment Inputs
const searchQuery = ref('')
const filterMode = ref('all') // 'all' | 'with_debt' | 'zero'
const paymentAmount = ref(null)

// Payment modal state
const paymentDialog = ref({
  open: false,
  customerId: null,
  customerName: '',
  maxAmount: 0.0,
})

// Customer modal state (Add/Edit)
const customerDialog = ref({
  open: false,
  editMode: false,
  customerId: null,
})

const customerForm = ref({
  name: '',
  contact_number: '',
  notes: '',
})

// KPI Metrics Computeds
const totalOutstandingUtang = computed(() => {
  return customers.value.reduce((sum, c) => {
    const val = parseFloat(c.total_utang) || 0
    return sum + (val > 0 ? val : 0)
  }, 0)
})

const customersWithBalanceCount = computed(() => {
  return customers.value.filter((c) => (parseFloat(c.total_utang) || 0) > 0).length
})

const totalDebtCollected = computed(() => {
  return transactions.value
    .filter((tx) => tx.transaction_type === 'DEBT_PAYMENT')
    .reduce((sum, tx) => sum + (parseFloat(tx.amount_paid) || 0), 0)
})

// Filtered Customer list
const filteredCustomers = computed(() => {
  return customers.value.filter((customer) => {
    const query = searchQuery.value.toLowerCase().trim()
    const matchesSearch =
      !query ||
      customer.name.toLowerCase().includes(query) ||
      (customer.contact_number && customer.contact_number.includes(query))

    const utang = parseFloat(customer.total_utang) || 0
    let matchesFilter = true
    if (filterMode.value === 'with_debt') {
      matchesFilter = utang > 0
    } else if (filterMode.value === 'zero') {
      matchesFilter = utang <= 0
    }

    return matchesSearch && matchesFilter
  })
})

// Transactions for selected customer
const customerTransactions = computed(() => {
  if (!selectedCustomer.value) return []
  return transactions.value.filter((tx) => tx.customer === selectedCustomer.value.id)
})

const selectedCustomerTotalInvoiced = computed(() => {
  return customerTransactions.value
    .filter((tx) => tx.transaction_type === 'CREDIT')
    .reduce((sum, tx) => sum + (parseFloat(tx.total_amount) || 0), 0)
})

const selectedCustomerTotalPaid = computed(() => {
  return customerTransactions.value.reduce(
    (sum, tx) => sum + (parseFloat(tx.amount_paid) || 0),
    0,
  )
})

const columns = [
  { name: 'created_at', label: 'Date / Time', field: 'created_at', align: 'left', sortable: true },
  {
    name: 'transaction_type',
    label: 'Record Type',
    field: 'transaction_type',
    align: 'left',
    sortable: true,
  },
  {
    name: 'total_amount',
    label: 'Total Bill',
    field: 'total_amount',
    align: 'right',
    sortable: true,
  },
  {
    name: 'amount_paid',
    label: 'Amount Paid',
    field: 'amount_paid',
    align: 'right',
    sortable: true,
  },
  {
    name: 'unpaid_balance',
    label: 'Balance Due',
    field: 'id',
    align: 'right',
    sortable: true,
  },
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
      const match = customers.value.find((c) => c.id === selectedCustomer.value.id)
      if (match) {
        selectedCustomer.value = match
      }
    }
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to synchronize credit database.',
      icon: 'error',
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
  paymentDialog.value.maxAmount = parseFloat(customer.total_utang) || 0
  paymentAmount.value = parseFloat(customer.total_utang) || 0 // Autofill full balance
  paymentDialog.value.open = true
}

function setQuickAmount(amt) {
  paymentAmount.value = Math.min(amt, paymentDialog.value.maxAmount)
}

// Post payment adjustment
async function submitPayment() {
  try {
    const currentUtang = paymentDialog.value.maxAmount
    const reduction = parseFloat(paymentAmount.value)
    const newUtang = Math.max(0, currentUtang - reduction)

    // PATCH update to customer total_utang
    await api.patch(`customers/${paymentDialog.value.customerId}/`, {
      total_utang: newUtang.toFixed(2),
    })

    // Also register this cash receipt by posting a dummy Transaction representing the debt payment
    await api.post('transactions/', {
      transaction_type: 'DEBT_PAYMENT',
      customer: paymentDialog.value.customerId,
      total_amount: reduction.toFixed(2),
      amount_paid: reduction.toFixed(2),
      change_given: '0.00',
      items: [],
    })

    playChime()
    $q.notify({
      color: 'positive',
      message: `Payment of ₱${reduction.toFixed(2)} recorded for ${paymentDialog.value.customerName}!`,
      icon: 'payments',
    })

    paymentDialog.value.open = false
    paymentAmount.value = null
    await fetchData()
  } catch {
    playWarning()
    $q.notify({
      color: 'negative',
      message: 'Failed to record payment transaction.',
      icon: 'error',
    })
  }
}

// Open Add/Edit Customer Dialog
function openAddCustomerDialog() {
  customerDialog.value = {
    open: true,
    editMode: false,
    customerId: null,
  }
  customerForm.value = {
    name: '',
    contact_number: '',
    notes: '',
  }
}

function openEditCustomerDialog(customer) {
  customerDialog.value = {
    open: true,
    editMode: true,
    customerId: customer.id,
  }
  customerForm.value = {
    name: customer.name,
    contact_number: customer.contact_number || '',
    notes: customer.notes || '',
  }
}

async function saveCustomer() {
  try {
    const payload = {
      name: customerForm.value.name.trim(),
      contact_number: customerForm.value.contact_number?.trim() || null,
      notes: customerForm.value.notes?.trim() || null,
    }

    if (customerDialog.value.editMode) {
      const res = await api.patch(`customers/${customerDialog.value.customerId}/`, payload)
      const index = customers.value.findIndex((c) => c.id === customerDialog.value.customerId)
      if (index > -1) {
        customers.value[index] = { ...customers.value[index], ...res.data }
      }
      if (selectedCustomer.value?.id === customerDialog.value.customerId) {
        selectedCustomer.value = { ...selectedCustomer.value, ...res.data }
      }
      $q.notify({
        color: 'positive',
        message: 'Customer profile updated!',
        icon: 'check',
      })
    } else {
      const res = await api.post('customers/', { ...payload, total_utang: '0.00' })
      customers.value.push(res.data)
      selectedCustomer.value = res.data
      $q.notify({
        color: 'positive',
        message: `Customer "${res.data.name}" registered!`,
        icon: 'person_add',
      })
    }

    customerDialog.value.open = false
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to save customer profile.',
      icon: 'error',
    })
  }
}

// Format Date string
function formatDate(dateTimeStr) {
  if (!dateTimeStr) return ''
  const date = new Date(dateTimeStr)
  return date.toLocaleString([], {
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.credit-tracker-page {
  background-color: #f1f5f9;
  min-height: 100vh;
}

.back-button {
  background-color: #ffffff;
  border: 1.5px solid #94a3b8;
  border-radius: 10px;
  width: 40px;
  height: 40px;
  transition: all 0.15s ease;
  &:hover {
    border-color: #475569;
    background-color: #f8fafc;
  }
}

.refresh-btn {
  background-color: #ffffff;
  border: 1.5px solid #94a3b8;
  border-radius: 10px;
  width: 40px;
  height: 40px;
}

.reports-search-input-long {
  :deep(.q-field__control) {
    border-radius: 12px;
    height: 40px;
    background-color: #ffffff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }
  :deep(.q-field--outlined .q-field__control:before) {
    border: 1.5px solid #94a3b8;
    border-radius: 12px;
    transition: border-color 0.15s ease;
  }
  :deep(.q-field--outlined:hover .q-field__control:before) {
    border-color: #475569;
  }
  :deep(.q-field--focused .q-field__control:after) {
    border: 2px solid #0d6832 !important;
    border-radius: 12px;
  }
}

.export-btn {
  height: 40px;
  border-radius: 10px;
  padding: 0 16px;
  font-size: 0.84rem;
  transition: all 0.15s ease;
}

.btn-agrivet-green {
  background-color: #0d6832 !important;
  color: #ffffff !important;
  &:hover {
    background-color: #0a5227 !important;
  }
}

.kpi-metric-card {
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  border-radius: 14px !important;
  border: 1.5px solid #94a3b8 !important;
  background-color: #ffffff !important;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.08),
    0 1px 2px -1px rgba(0, 0, 0, 0.05) !important;
  padding: 18px 16px;
  transition: all 0.15s ease;
  &:hover {
    border-color: #475569 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    transform: translateY(-1px);
  }
}

.kpi-metric-value {
  font-size: 1.8rem;
  font-weight: 800;
  line-height: 1.25;
  letter-spacing: -0.02em;
}

.kpi-icon-squircle {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.data-table-card {
  border-radius: 16px !important;
  border: 1.5px solid #94a3b8 !important;
  background-color: #ffffff !important;
  box-shadow:
    0 1px 3px rgba(0, 0, 0, 0.08),
    0 1px 2px -1px rgba(0, 0, 0, 0.05) !important;
  overflow: hidden;
}

.scroll-container {
  overflow-y: auto;
}

.customer-item-row {
  transition: background-color 0.12s ease;
  border-left: 4px solid transparent;
  &:hover {
    background-color: #f8fafc;
  }
}

.active-customer-ledger {
  background-color: #ecfdf5 !important;
  border-left: 4px solid #0d6832 !important;
}

.outstanding-banner {
  background-color: #fff1f2;
  border: 1.5px solid #fecdd3;
}

.border-slate {
  border: 1.5px solid #94a3b8;
}

.border-bottom-subtle {
  border-bottom: 1.5px solid #cbd5e1;
}

.num-tabular {
  font-variant-numeric: tabular-nums lining-nums;
}

:deep(.credit-history-table th) {
  font-weight: 800 !important;
  font-size: 0.9rem !important;
  color: #0f172a !important;
  background-color: #f8fafc !important;
  letter-spacing: 0.01em;
}
</style>
