<template>
  <q-layout view="lHh lpR lFf" class="tablet-layout-root">
    <!-- Collapsible Tablet Left Sidebar (Floating Overlay Drawer: Never squishes screen) -->
    <q-drawer
      v-model="drawer"
      side="left"
      :breakpoint="0"
      :width="230"
      overlay
      bordered
      class="tablet-sidebar bg-white"
    >
      <div class="column full-height justify-between q-pa-md">
        <!-- Top: Brand Header & Nav List -->
        <div>
          <!-- Brand Logo Header with Close Button -->
          <div class="row items-center justify-between no-wrap q-mb-lg q-pt-xs">
            <div
              class="row items-center no-wrap cursor-pointer"
              @click="
                $router.push('/');
                drawer = false
              "
            >
              <img :src="logoUrl" alt="Nichole Agrivet" class="brand-mascot-raw q-mr-sm" />
              <div class="row items-center no-wrap">
                <span
                  class="text-weight-bolder text-subtitle2 text-slate-900 leading-tight q-mr-xs tracking-tight"
                >
                  NICHOLE AGRIVET
                </span>
                <span class="badge-mint text-caption" style="font-size: 0.65rem">Tablet #01</span>
              </div>
            </div>
            <q-btn
              flat
              round
              dense
              icon="close"
              color="slate-6"
              size="11px"
              class="bg-slate-100"
              @click="drawer = false"
            />
          </div>

          <!-- Main Navigation Links -->
          <div
            class="text-caption text-weight-bold text-slate-400 text-uppercase tracking-wider q-mb-xs q-px-sm"
          >
            Menu
          </div>
          <q-list class="q-gutter-y-xs no-border">
            <q-item
              v-for="nav in navItems"
              :key="nav.to"
              clickable
              v-ripple
              :to="nav.to"
              exact
              class="sidebar-nav-item"
              :active-class="'sidebar-nav-active'"
              @click="drawer = false"
            >
              <q-item-section avatar class="min-width-auto q-pr-sm">
                <q-icon :name="nav.icon" size="20px" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-medium text-body2">{{ nav.label }}</q-item-label>
              </q-item-section>
            </q-item>

            <!-- Help & User Guide Link -->
            <q-item
              clickable
              v-ripple
              class="sidebar-nav-item"
              @click="
                showHelpGuide = true;
                drawer = false
              "
            >
              <q-item-section avatar class="min-width-auto q-pr-sm">
                <q-icon name="help_outline" size="20px" color="primary" />
              </q-item-section>
              <q-item-section>
                <q-item-label class="text-weight-medium text-body2">Help & Guide</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </div>

        <!-- Bottom: Status & Quick Info -->
        <div class="q-pt-md border-top-slate">
          <!-- Connection Status Pill -->
          <div
            class="status-pill row items-center q-px-sm q-py-xs rounded-borders q-mb-sm"
            :class="apiConnected ? 'status-online' : 'status-standalone'"
          >
            <span
              class="status-dot q-mr-xs"
              :class="apiConnected ? 'dot-online' : 'dot-standalone'"
            ></span>
            <span class="text-caption text-weight-semibold">
              {{ apiConnected ? 'Server Online' : '📱 Standalone Tablet' }}
            </span>
          </div>

          <!-- Time Display -->
          <div class="row items-center text-caption text-slate-500 q-mb-sm q-px-xs">
            <q-icon name="schedule" size="14px" class="q-mr-xs text-slate-400" />
            <span class="num-tabular">{{ currentTime }}</span>
          </div>

          <!-- Log Out Button -->
          <q-btn
            flat
            dense
            no-caps
            icon="logout"
            label="Log Out"
            color="negative"
            class="full-width sidebar-logout-btn q-py-xs text-weight-bold"
            @click="handleLogout"
          />
        </div>
      </div>
    </q-drawer>

    <!-- Top Tablet Header (Hidden on POS to match full-screen mockup) -->
    <q-header
      v-if="route.path !== '/pos'"
      class="tablet-header bg-white text-slate-900 border-bottom-slate"
    >
      <q-toolbar class="q-px-md q-py-xs">
        <!-- Toggle button for drawer navigation -->
        <q-btn
          flat
          dense
          round
          icon="menu"
          color="slate-7"
          class="q-mr-sm"
          @click="drawer = !drawer"
        />

        <!-- Active View Title (Lowered to sit balanced in header) -->
        <q-toolbar-title
          class="text-weight-bold text-h6 text-slate-900 q-pl-none"
          style="margin-top: 5px"
        >
          {{ currentViewTitle }}
        </q-toolbar-title>

        <q-space />

        <!-- Right Header Items: Notifications & Cashier User Profile -->
        <TopHeaderControls />
      </q-toolbar>
    </q-header>

    <!-- Page Content Container -->
    <q-page-container class="tablet-main-bg">
      <router-view />
    </q-page-container>

    <!-- Help & Guide Modal Component -->
    <HelpGuideModal v-model="showHelpGuide" />
  </q-layout>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, provide } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import logoUrl from 'src/images/Nichole Agrivet.png'
import TopHeaderControls from 'src/components/TopHeaderControls.vue'
import HelpGuideModal from 'src/components/HelpGuideModal.vue'

const router = useRouter()
const route = useRoute()
const $q = useQuasar()

const drawer = ref(false)
const showHelpGuide = ref(false)
const apiConnected = ref(false)
const currentTime = ref('')

function toggleDrawer() {
  drawer.value = !drawer.value
}
provide('toggleDrawer', toggleDrawer)

const currentViewTitle = computed(() => {
  if (route.path === '/pos') return 'Orders'
  if (route.path === '/inventory') return 'Inventory Catalog'
  if (route.path === '/credit') return 'Credit & Utang Tracker'
  if (route.path === '/sales') return 'Reports & Analytics'
  return 'Dashboard'
})

const navItems = [
  { label: 'Dashboard', icon: 'grid_view', to: '/' },
  { label: 'Orders / POS', icon: 'receipt_long', to: '/pos' },
  { label: 'Inventory', icon: 'inventory_2', to: '/inventory' },
  { label: 'Credit Tracker', icon: 'account_balance_wallet', to: '/credit' },
  { label: 'Reports', icon: 'bar_chart', to: '/sales' },
]

function handleLogout() {
  $q.dialog({
    title: 'Confirm Logout',
    message: 'Are you sure you want to sign out of the POS system?',
    cancel: { flat: true, color: 'grey-7', label: 'Cancel' },
    ok: { color: 'primary', label: 'Log Out', unelevated: true, icon: 'logout' },
    persistent: true,
  }).onOk(() => {
    localStorage.setItem('isLoggedOut', 'true')
    localStorage.removeItem('isLoggedIn')
    $q.notify({
      color: 'info',
      message: 'Signed out successfully.',
      icon: 'lock',
    })
    router.push('/login')
  })
}

let clockInterval
function updateTime() {
  const options = {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  }
  currentTime.value = new Date().toLocaleString('en-US', options)
}

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

<style scoped lang="scss">
.tablet-layout-root {
  background-color: #f8f9fa;
}

.tablet-main-bg {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.tablet-sidebar {
  border-right: 1px solid #e5e7eb !important;
}

.sidebar-nav-item {
  border-radius: 10px;
  color: #64748b;
  margin-bottom: 4px;
  padding: 8px 12px;
  transition: all 0.15s ease;
}
.sidebar-nav-item:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

.brand-mascot-raw {
  height: 46px;
  width: auto;
  object-fit: contain;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
}

/* Active State matching user's Forest Green & Mint theme */
.sidebar-nav-active {
  background-color: #e6f4ea !important;
  color: #0d6832 !important;
  font-weight: 700 !important;
  border-left: 3.5px solid #0d6832 !important;
}
.sidebar-nav-active .q-icon {
  color: #0d6832 !important;
}

.header-icon-btn {
  background: #f8f9fa;
  border: 1px solid #e5e7eb;
}

.user-avatar-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #ff8a65;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-pill {
  background-color: #f8f9fa;
  border: 1px solid #e5e7eb;
  padding: 4px 8px;
}

.status-pill {
  border-radius: 9999px;
  font-size: 0.75rem;
}
.status-online {
  background: #ecfdf5;
  color: #059669;
  border: 1px solid #a7f3d0;
}
.status-standalone {
  background: #f0fdf4;
  color: #15803d;
  border: 1px solid #bbf7d0;
}
.status-offline {
  background: #fff1ee;
  color: #ef4444;
  border: 1px solid #fecaca;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  display: inline-block;
}
.dot-online,
.dot-standalone {
  background-color: #10b981;
}
.dot-offline {
  background-color: #ef4444;
}

.sidebar-logout-btn {
  background: #fff1f2;
  border: 1px solid #fecdd3;
  border-radius: 8px;
}

.border-top-slate {
  border-top: 1px solid #e5e7eb;
}
.border-bottom-slate {
  border-bottom: 1px solid #e5e7eb;
}
.min-width-auto {
  min-width: auto;
}
</style>
