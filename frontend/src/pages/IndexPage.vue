<template>
  <q-page class="q-pa-md q-pa-md-lg max-width-container">
    <!-- Dashboard Header Banner -->
    <div class="dashboard-hero q-pa-md q-pa-md-lg rounded-borders-lg q-mb-lg bg-white border-slate shadow-xs">
      <div class="row items-center justify-between">
        <div class="row items-center no-wrap">
          <q-avatar size="90px" class="q-mr-lg shadow-3 bg-white gt-xs overflow-hidden" style="border: 2.5px solid #059669; min-width: 96px;">
            <img :src="logoUrl" alt="Nichole Agrivet Logo" style="object-fit: cover; transform: scale(1.15);" />
          </q-avatar>
          <div>
            <div class="row items-center q-mb-xs">
              <q-badge color="emerald-1" text-color="emerald-9" class="q-px-sm q-py-xs text-caption text-weight-bold q-mr-sm">
                Live Operations
              </q-badge>
              <span class="text-caption text-slate-500">{{ currentDateFormatted }}</span>
            </div>
            <h1 class="text-h4 text-weight-bold text-slate-900 q-my-none tracking-tight">
              Nichole Agrivet Dashboard
            </h1>
            <p class="text-body2 text-slate-600 q-mt-xs q-mb-none max-w-65ch">
              Manage your daily transactions, monitor store stock, track customer credit ledgers, and analyze sales reports.
            </p>
          </div>
        </div>

        <div class="gt-xs q-mt-md q-mt-sm-none">
          <q-btn
            color="primary"
            icon="point_of_sale"
            label="Open Cashier"
            to="/pos"
            unelevated
            class="q-px-md q-py-sm"
          />
        </div>
      </div>
    </div>

    <!-- Quick KPI Overview Metrics Bar -->
    <div class="row q-col-gutter-md q-mb-lg">
      <!-- Daily Sales Count Stat -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat class="stat-card bg-white q-pa-md">
          <div class="row items-center justify-between">
            <div>
              <div class="text-caption text-slate-500 text-weight-semibold text-uppercase tracking-wider">
                Sales Today
              </div>
              <div class="text-h5 text-weight-bold text-slate-900 num-tabular q-mt-xs">
                <template v-if="loadingStats">
                  <q-skeleton type="text" width="60px" />
                </template>
                <template v-else>
                  {{ dailySalesCount !== null ? `${dailySalesCount} Transactions` : '0' }}
                </template>
              </div>
            </div>
            <q-avatar size="44px" class="bg-indigo-50 text-indigo-7">
              <q-icon name="payments" size="24px" />
            </q-avatar>
          </div>
        </q-card>
      </div>

      <!-- Low Stock Alert Stat -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat class="stat-card bg-white q-pa-md">
          <div class="row items-center justify-between">
            <div>
              <div class="text-caption text-slate-500 text-weight-semibold text-uppercase tracking-wider">
                Stock Alerts
              </div>
              <div class="text-h5 text-weight-bold num-tabular q-mt-xs" :class="lowStockCount > 0 ? 'text-rose-6' : 'text-slate-900'">
                <template v-if="loadingStats">
                  <q-skeleton type="text" width="60px" />
                </template>
                <template v-else>
                  {{ lowStockCount !== null ? `${lowStockCount} Low Items` : '0' }}
                </template>
              </div>
            </div>
            <q-avatar size="44px" class="bg-rose-50 text-rose-6">
              <q-icon name="warning_amber" size="24px" />
            </q-avatar>
          </div>
        </q-card>
      </div>

      <!-- Total Utang Ledger Stat -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat class="stat-card bg-white q-pa-md">
          <div class="row items-center justify-between">
            <div>
              <div class="text-caption text-slate-500 text-weight-semibold text-uppercase tracking-wider">
                Total Credit
              </div>
              <div class="text-h5 text-weight-bold text-slate-900 num-tabular q-mt-xs">
                <template v-if="loadingStats">
                  <q-skeleton type="text" width="80px" />
                </template>
                <template v-else>
                  {{ totalUtang !== null ? `₱${totalUtang.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}` : '₱0.00' }}
                </template>
              </div>
            </div>
            <q-avatar size="44px" class="bg-amber-50 text-amber-8">
              <q-icon name="account_balance_wallet" size="24px" />
            </q-avatar>
          </div>
        </q-card>
      </div>

      <!-- Active Customers Count Stat -->
      <div class="col-12 col-sm-6 col-md-3">
        <q-card flat class="stat-card bg-white q-pa-md">
          <div class="row items-center justify-between">
            <div>
              <div class="text-caption text-slate-500 text-weight-semibold text-uppercase tracking-wider">
                Customers
              </div>
              <div class="text-h5 text-weight-bold text-slate-900 num-tabular q-mt-xs">
                <template v-if="loadingStats">
                  <q-skeleton type="text" width="50px" />
                </template>
                <template v-else>
                  {{ totalCustomers !== null ? `${totalCustomers} Registered` : '0' }}
                </template>
              </div>
            </div>
            <q-avatar size="44px" class="bg-emerald-50 text-emerald-7">
              <q-icon name="people" size="24px" />
            </q-avatar>
          </div>
        </q-card>
      </div>
    </div>

    <!-- Main Module Action Cards Grid -->
    <div class="row q-col-gutter-md">
      <!-- Cashier Card -->
      <div class="col-12 col-sm-6">
        <q-card
          flat
          clickable
          v-ripple
          class="module-card bg-white hover-grow cursor-pointer q-pa-md"
          @click="$router.push('/pos')"
        >
          <div class="column full-height justify-between">
            <div>
              <div class="row items-center justify-between q-mb-md">
                <q-avatar size="52px" class="bg-emerald-50 text-emerald-7">
                  <q-icon name="point_of_sale" size="30px" />
                </q-avatar>
                <q-icon name="arrow_forward" size="20px" class="text-slate-400 module-arrow" />
              </div>
              <div class="text-h6 text-weight-bold text-slate-900 q-mb-xs">
                Cashier
              </div>
              <p class="text-body2 text-slate-600 q-mb-md">
                Scan products, handle cash or credit checkout, generate receipts, and manage active shopping carts.
              </p>
            </div>

            <div class="row items-center justify-between pt-sm border-top-slate">
              <span class="text-caption text-slate-500">Quick Cash & Credit</span>
              <q-badge color="emerald-1" text-color="emerald-9" class="q-px-sm q-py-xs">
                Launch Cashier
              </q-badge>
            </div>
          </div>
        </q-card>
      </div>

      <!-- Inventory Management Card -->
      <div class="col-12 col-sm-6">
        <q-card
          flat
          clickable
          v-ripple
          class="module-card bg-white hover-grow cursor-pointer q-pa-md"
          @click="$router.push('/inventory')"
        >
          <div class="column full-height justify-between">
            <div>
              <div class="row items-center justify-between q-mb-md">
                <q-avatar size="52px" class="bg-sky-50 text-sky-7">
                  <q-icon name="inventory_2" size="30px" />
                </q-avatar>
                <q-icon name="arrow_forward" size="20px" class="text-slate-400 module-arrow" />
              </div>
              <div class="text-h6 text-weight-bold text-slate-900 q-mb-xs">
                Available Stock & Inventory
              </div>
              <p class="text-body2 text-slate-600 q-mb-md">
                View catalog products, update prices, adjust inventory stock levels, and monitor low-stock warnings.
              </p>
            </div>

            <div class="row items-center justify-between pt-sm border-top-slate">
              <span class="text-caption text-slate-500">Stock Catalog</span>
              <q-badge color="sky-1" text-color="sky-9" class="q-px-sm q-py-xs">
                {{ lowStockCount !== null ? `${lowStockCount} Low Stock` : 'Check Stock' }}
              </q-badge>
            </div>
          </div>
        </q-card>
      </div>

      <!-- Customer Credit Ledger Card -->
      <div class="col-12 col-sm-6">
        <q-card
          flat
          clickable
          v-ripple
          class="module-card bg-white hover-grow cursor-pointer q-pa-md"
          @click="$router.push('/credit')"
        >
          <div class="column full-height justify-between">
            <div>
              <div class="row items-center justify-between q-mb-md">
                <q-avatar size="52px" class="bg-amber-50 text-amber-8">
                  <q-icon name="account_balance_wallet" size="30px" />
                </q-avatar>
                <q-icon name="arrow_forward" size="20px" class="text-slate-400 module-arrow" />
              </div>
              <div class="text-h6 text-weight-bold text-slate-900 q-mb-xs">
                Credit Tracker & Ledger
              </div>
              <p class="text-body2 text-slate-600 q-mb-md">
                Track customer utang balances, record partial or full payments, and manage customer profile records.
              </p>
            </div>

            <div class="row items-center justify-between pt-sm border-top-slate">
              <span class="text-caption text-slate-500">Utang Accounts</span>
              <q-badge color="amber-1" text-color="amber-10" class="q-px-sm q-py-xs">
                {{ totalUtang !== null ? `₱${totalUtang.toLocaleString('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0})} Outstanding` : 'Open Ledger' }}
              </q-badge>
            </div>
          </div>
        </q-card>
      </div>

      <!-- Sales Analytics Card -->
      <div class="col-12 col-sm-6">
        <q-card
          flat
          clickable
          v-ripple
          class="module-card bg-white hover-grow cursor-pointer q-pa-md"
          @click="$router.push('/sales')"
        >
          <div class="column full-height justify-between">
            <div>
              <div class="row items-center justify-between q-mb-md">
                <q-avatar size="52px" class="bg-indigo-50 text-indigo-7">
                  <q-icon name="bar_chart" size="30px" />
                </q-avatar>
                <q-icon name="arrow_forward" size="20px" class="text-slate-400 module-arrow" />
              </div>
              <div class="text-h6 text-weight-bold text-slate-900 q-mb-xs">
                Sales Reports & Analytics
              </div>
              <p class="text-body2 text-slate-600 q-mb-md">
                Review daily transaction logs, filter sales date ranges, export store reports, and track revenue totals.
              </p>
            </div>

            <div class="row items-center justify-between pt-sm border-top-slate">
              <span class="text-caption text-slate-500">Reports & Summaries</span>
              <q-badge color="indigo-1" text-color="indigo-9" class="q-px-sm q-py-xs">
                {{ dailySalesCount !== null ? `${dailySalesCount} Sales Today` : 'View Reports' }}
              </q-badge>
            </div>
          </div>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from 'boot/axios'
import logoUrl from 'src/images/Nichole Agrivet.png'

const lowStockCount = ref(null)
const totalUtang = ref(null)
const dailySalesCount = ref(null)
const totalCustomers = ref(null)
const loadingStats = ref(true)

const currentDateFormatted = computed(() => {
  return new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

async function fetchStats() {
  loadingStats.value = true
  try {
    // 1. Fetch low stock items count
    const lowStockRes = await api.get('products/low-stock/')
    lowStockCount.value = Array.isArray(lowStockRes.data) ? lowStockRes.data.length : 0

    // 2. Fetch customer utang totals and customer count
    const customerRes = await api.get('customers/')
    if (Array.isArray(customerRes.data)) {
      totalCustomers.value = customerRes.data.length
      totalUtang.value = customerRes.data.reduce((sum, cust) => sum + parseFloat(cust.total_utang || 0), 0)
    } else {
      totalCustomers.value = 0
      totalUtang.value = 0
    }

    // 3. Fetch daily sales summaries
    const salesRes = await api.get('transactions/daily-summary/')
    dailySalesCount.value = salesRes.data ? (salesRes.data.total_sales_count || 0) : 0
  } catch (error) {
    console.error('Failed to fetch dashboard statistics:', error)
  } finally {
    loadingStats.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.max-width-container {
  max-width: 1200px;
  margin: 0 auto;
}

.max-w-65ch {
  max-width: 65ch;
}

.rounded-borders-lg {
  border-radius: 12px;
}

.border-slate {
  border: 1.5px solid #cbd5e1;
}

.border-top-slate {
  border-top: 1.5px solid #cbd5e1;
  padding-top: 12px;
}

.stat-card {
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
}

.module-card {
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  min-height: 220px;
}

.module-card:hover .module-arrow {
  color: #059669 !important;
  transform: translateX(4px);
  transition: all 0.2s ease;
}

.bg-emerald-50 { background-color: #ecfdf5 !important; }
.text-emerald-7 { color: #047857 !important; }
.text-emerald-9 { color: #064e3b !important; }
.bg-emerald-1 { background-color: #d1fae5 !important; }

.bg-indigo-50 { background-color: #e0e7ff !important; }
.text-indigo-7 { color: #4338ca !important; }
.text-indigo-9 { color: #312e81 !important; }
.bg-indigo-1 { background-color: #e0e7ff !important; }

.bg-sky-50 { background-color: #f0f9ff !important; }
.text-sky-7 { color: #0369a1 !important; }
.text-sky-9 { color: #0c4a6e !important; }
.bg-sky-1 { background-color: #e0f2fe !important; }

.bg-amber-50 { background-color: #fffbeb !important; }
.text-amber-8 { color: #92400e !important; }
.text-amber-10 { color: #451a03 !important; }
.bg-amber-1 { background-color: #fef3c7 !important; }

.bg-rose-50 { background-color: #ffe4e6 !important; }
.text-rose-6 { color: #e11d48 !important; }
</style>

