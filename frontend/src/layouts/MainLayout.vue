<template>
  <q-layout view="hHh lpR fFf">
    <!-- Main App Header -->
    <q-header elevated class="bg-slate-900 text-white shadow-2">
      <q-toolbar class="q-py-xs q-px-md">
        <!-- Store Logo & Title -->
        <q-toolbar-title class="row items-center cursor-pointer min-width-auto q-mr-lg" @click="$router.push('/')">
          <q-avatar size="44px" class="q-mr-sm bg-white shadow-2 overflow-hidden" style="border: 2px solid #059669">
            <img :src="logoUrl" alt="Nichole Agrivet Logo" style="object-fit: cover; transform: scale(1.15);" />
          </q-avatar>
          <div>
            <div class="text-weight-bold text-subtitle1 leading-tight tracking-tight">
              Nichole Agrivet
            </div>
            <div class="text-caption text-emerald-400 leading-none text-weight-medium gt-xs">
              Inventory System
            </div>
          </div>
        </q-toolbar-title>

        <!-- Top Navigation Links -->
        <div class="row items-center q-gutter-x-xs q-mr-md">
          <q-btn
            v-for="nav in navItems"
            :key="nav.to"
            flat
            dense
            no-caps
            :to="nav.to"
            :label="nav.label"
            :icon="nav.icon"
            class="header-nav-btn q-px-sm"
            :class="{ 'header-nav-active': $route.path === nav.to }"
          />
        </div>

        <q-space />

        <!-- API Connection Status Badge -->
        <div class="row items-center q-mr-md">
          <div
            class="status-pill row items-center q-px-sm q-py-xs rounded-borders"
            :class="apiConnected ? 'status-online' : 'status-offline'"
          >
            <span class="status-dot q-mr-xs" :class="apiConnected ? 'dot-online' : 'dot-offline'"></span>
            <span class="text-caption text-weight-semibold">
              {{ apiConnected ? 'API Online' : 'API Offline' }}
            </span>
          </div>
        </div>

        <!-- Clock Widget -->
        <div class="clock-widget gt-xs row items-center text-caption text-weight-medium q-px-sm q-py-xs rounded-borders">
          <q-icon name="schedule" class="q-mr-xs" size="16px" />
          <span>{{ currentTime }}</span>
        </div>

        <!-- User Profile & Log Out Button -->
        <div class="row items-center q-ml-md q-gutter-x-xs">
          <q-btn flat no-caps dense class="user-pill q-px-sm">
            <q-avatar size="26px" color="positive" text-color="white" icon="person" class="q-mr-xs" />
            <span class="text-caption text-weight-bold text-slate-200 gt-xs">{{ userName }}</span>
            <q-menu auto-close anchor="bottom right" self="top right">
              <q-list style="min-width: 180px">
                <q-item class="text-slate-700">
                  <q-item-section avatar><q-icon name="person" color="primary" /></q-item-section>
                  <q-item-section>
                    <q-item-label class="text-weight-bold">{{ userName }}</q-item-label>
                  </q-item-section>
                </q-item>
                <q-separator />
                <q-item clickable class="text-negative" @click="handleLogout">
                  <q-item-section avatar><q-icon name="logout" color="negative" /></q-item-section>
                  <q-item-section class="text-weight-bold">Log Out</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>

          <q-btn
            flat
            dense
            color="rose-4"
            icon="logout"
            label="Log Out"
            class="gt-xs text-weight-bold q-px-sm rounded-borders"
            style="background: rgba(244, 63, 94, 0.15); border: 1px solid rgba(244, 63, 94, 0.3);"
            @click="handleLogout"
          >
            <q-tooltip>Sign out of system</q-tooltip>
          </q-btn>
        </div>
      </q-toolbar>
    </q-header>

    <!-- Page Content Container -->
    <q-page-container class="bg-slate-100">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import logoUrl from 'src/images/Nichole Agrivet.png'

const router = useRouter()
const $q = useQuasar()

const apiConnected = ref(false)
const currentTime = ref('')

const userName = ref(localStorage.getItem('userName') || 'admin')

function handleLogout() {
  $q.dialog({
    title: 'Confirm Logout',
    message: 'Are you sure you want to log out of Nichole Agrivet System?',
    cancel: {
      flat: true,
      color: 'grey-7',
      label: 'Cancel'
    },
    ok: {
      color: 'negative',
      label: 'Log Out',
      unelevated: true,
      icon: 'logout'
    },
    persistent: true
  }).onOk(() => {
    localStorage.removeItem('isLoggedIn')
    localStorage.removeItem('userName')

    $q.notify({
      color: 'info',
      message: 'You have logged out successfully.',
      icon: 'lock'
    })

    router.push('/login')
  })
}

const navItems = [
  { label: 'Dashboard', caption: 'Overview & Analytics', icon: 'dashboard', to: '/' },
  { label: 'Cashier', caption: 'Process Sales & Cash', icon: 'point_of_sale', to: '/pos' },
  { label: 'Inventory', caption: 'Stock List & Products', icon: 'inventory_2', to: '/inventory' },
  { label: 'Credit Tracker', caption: 'Customer Accounts & Utang', icon: 'account_balance_wallet', to: '/credit' },
  { label: 'Sales Reports', caption: 'Daily & Monthly Logs', icon: 'bar_chart', to: '/sales' }
]

// Update clock every second
let clockInterval
function updateTime() {
  const options = {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  }
  currentTime.value = new Date().toLocaleString('en-US', options)
}

// Check Django API status
let apiInterval
async function checkApiStatus() {
  try {
    await api.get('categories/')
    apiConnected.value = true
  } catch {
    apiConnected.value = false
  }
}

onMounted(() => {
  updateTime()
  clockInterval = setInterval(updateTime, 1000)

  checkApiStatus()
  apiInterval = setInterval(checkApiStatus, 5000)
})

onBeforeUnmount(() => {
  clearInterval(clockInterval)
  clearInterval(apiInterval)
})
</script>

<style scoped>
.bg-slate-900 {
  background-color: #0f172a !important;
}
.bg-slate-100 {
  background-color: #f8fafc !important;
}
.bg-slate-50 {
  background-color: #f8fafc !important;
}
.text-slate-200 {
  color: #e2e8f0 !important;
}
.text-slate-400 {
  color: #94a3b8 !important;
}
.text-slate-500 {
  color: #64748b !important;
}
.text-emerald-400 {
  color: #34d399 !important;
}

.brand-avatar {
  width: 32px;
  height: 32px;
  background: #059669;
  border-radius: 8px;
}

.header-nav-btn {
  color: #94a3b8;
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.15s ease;
}
.header-nav-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.08);
}
.header-nav-active {
  color: #ffffff !important;
  background: rgba(5, 150, 105, 0.3) !important;
  font-weight: 600;
}

.status-pill {
  border-radius: 9999px;
  font-size: 0.75rem;
}
.status-online {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.status-offline {
  background: rgba(244, 63, 94, 0.15);
  color: #fb7185;
  border: 1px solid rgba(244, 63, 94, 0.3);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}
.dot-online {
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
}
.dot-offline {
  background-color: #f43f5e;
  box-shadow: 0 0 8px #f43f5e;
}

.clock-widget {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: #cbd5e1;
}

.border-bottom-slate {
  border-bottom: 1.5px solid #cbd5e1;
}
.border-top-slate {
  border-top: 1.5px solid #cbd5e1;
}
.min-width-auto {
  min-width: auto;
}
</style>

