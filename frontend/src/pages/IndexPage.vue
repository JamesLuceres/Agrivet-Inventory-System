<template>
  <q-page class="q-pa-lg flex flex-center">
    <div class="full-width" style="max-width: 1000px">
      <!-- Title & Greeting -->
      <div class="q-mb-xl text-center">
        <h2 class="text-h3 text-weight-bold text-indigo-10 q-my-none">Nichole Agrivet Dashboard</h2>
        <p class="text-subtitle1 text-grey-7 q-mt-sm">Select an option below to manage sales and inventory.</p>
      </div>

      <!-- Action Card Grid -->
      <div class="row q-col-gutter-lg justify-center">
        <!-- POS Card -->
        <div class="col-12 col-sm-6">
          <q-card 
            flat 
            bordered 
            class="dashboard-card cursor-pointer bg-white text-green-10 hover-green shadow-1 text-center q-pa-lg" 
            v-ripple
            @click="$router.push('/pos')"
          >
            <q-card-section>
              <q-icon name="shopping_cart" size="100px" color="positive" class="q-mb-md" />
              <div class="text-h4 text-weight-bold text-uppercase">Pay (Checkout)</div>
              <div class="text-subtitle1 text-grey-7 q-mt-sm">Start a new cash or credit transaction</div>
            </q-card-section>
            
            <q-card-actions align="center" class="q-pt-none">
              <q-badge color="positive" text-color="white" class="q-px-md q-py-xs text-subtitle2 rounded-borders">
                Launch Register
              </q-badge>
            </q-card-actions>
          </q-card>
        </div>

        <!-- Inventory Card -->
        <div class="col-12 col-sm-6">
          <q-card 
            flat 
            bordered 
            class="dashboard-card cursor-pointer bg-white text-blue-10 hover-blue shadow-1 text-center q-pa-lg" 
            v-ripple
            @click="$router.push('/inventory')"
          >
            <q-card-section>
              <q-icon name="inventory_2" size="100px" color="primary" class="q-mb-md" />
              <div class="text-h4 text-weight-bold text-uppercase">Available Items</div>
              <div class="text-subtitle1 text-grey-7 q-mt-sm">Stock list and low-stock alerts</div>
            </q-card-section>
            
            <q-card-actions align="center" class="q-pt-none">
              <q-badge color="primary" text-color="white" class="q-px-md q-py-xs text-subtitle2 rounded-borders">
                {{ lowStockCount !== null ? `${lowStockCount} Items Low` : 'Check Stock' }}
              </q-badge>
            </q-card-actions>
          </q-card>
        </div>

        <!-- Credit Tracker Card -->
        <div class="col-12 col-sm-6">
          <q-card 
            flat 
            bordered 
            class="dashboard-card cursor-pointer bg-white text-orange-10 hover-orange shadow-1 text-center q-pa-lg" 
            v-ripple
            @click="$router.push('/credit')"
          >
            <q-card-section>
              <q-icon name="payment" size="100px" color="warning" class="q-mb-md" />
              <div class="text-h4 text-weight-bold text-uppercase">Credit Tracker</div>
              <div class="text-subtitle1 text-grey-7 q-mt-sm">Manage customer credit and accounts</div>
            </q-card-section>
            
            <q-card-actions align="center" class="q-pt-none">
              <q-badge color="warning" text-color="dark" class="q-px-md q-py-xs text-subtitle2 rounded-borders">
                {{ totalUtang !== null ? `₱${totalUtang.toLocaleString('en-US', {minimumFractionDigits: 2})} Total` : 'Open Ledger' }}
              </q-badge>
            </q-card-actions>
          </q-card>
        </div>

        <!-- Sales Tracker Card -->
        <div class="col-12 col-sm-6">
          <q-card 
            flat 
            bordered 
            class="dashboard-card cursor-pointer bg-white text-purple-10 hover-purple shadow-1 text-center q-pa-lg" 
            v-ripple
            @click="$router.push('/sales')"
          >
            <q-card-section>
              <q-icon name="bar_chart" size="100px" color="purple" class="q-mb-md" />
              <div class="text-h4 text-weight-bold text-uppercase">Sales Tracker</div>
              <div class="text-subtitle1 text-grey-7 q-mt-sm">Track daily and monthly sales reporting and breakdowns</div>
            </q-card-section>
            
            <q-card-actions align="center" class="q-pt-none">
              <q-badge color="purple" text-color="white" class="q-px-md q-py-xs text-subtitle2 rounded-borders">
                {{ dailySalesCount !== null ? `${dailySalesCount} Sales Today` : 'View Reports' }}
              </q-badge>
            </q-card-actions>
          </q-card>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const lowStockCount = ref(null)
const totalUtang = ref(null)
const dailySalesCount = ref(null)

async function fetchStats() {
  try {
    // 1. Fetch low stock items count
    const lowStockRes = await api.get('products/low-stock/')
    lowStockCount.value = lowStockRes.data.length

    // 2. Fetch customer utang totals
    const customerRes = await api.get('customers/')
    totalUtang.value = customerRes.data.reduce((sum, cust) => sum + parseFloat(cust.total_utang || 0), 0)

    // 3. Fetch daily sales summaries
    const salesRes = await api.get('transactions/daily-summary/')
    dailySalesCount.value = salesRes.data.total_sales_count
  } catch (error) {
    console.error('Failed to fetch dashboard statistics:', error)
  }
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  border-radius: 12px;
  border-width: 2px;
}
.dashboard-card:hover {
  transform: translateY(-8px);
}
.hover-green:hover {
  border-color: var(--q-positive) !important;
  box-shadow: 0 10px 20px rgba(76, 175, 80, 0.15) !important;
}
.hover-blue:hover {
  border-color: var(--q-primary) !important;
  box-shadow: 0 10px 20px rgba(33, 150, 243, 0.15) !important;
}
.hover-orange:hover {
  border-color: var(--q-warning) !important;
  box-shadow: 0 10px 20px rgba(255, 152, 0, 0.15) !important;
}
.hover-purple:hover {
  border-color: purple !important;
  box-shadow: 0 10px 20px rgba(156, 39, 176, 0.15) !important;
}
.rounded-borders {
  border-radius: 6px;
}
</style>
