<template>
  <div class="row items-center q-gutter-x-sm no-wrap top-header-controls">
    <!-- 1. Notification Bell with interactive dropdown menu -->
    <q-btn flat round dense icon="notifications_none" color="slate-7" class="header-icon-btn">
      <q-badge v-if="unreadCount > 0" floating rounded color="primary" class="notification-badge">
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </q-badge>

      <q-menu
        anchor="bottom right"
        self="top right"
        class="notification-menu rounded-borders-lg shadow-md"
        style="width: 360px; max-width: 92vw"
      >
        <!-- Header -->
        <div class="row items-center justify-between q-pa-md bg-slate-50 border-bottom-subtle">
          <div class="row items-center q-gutter-x-xs">
            <span class="text-subtitle1 text-weight-bolder text-slate-900">Notifications</span>
            <q-badge v-if="unreadCount > 0" color="primary" class="q-ml-xs text-weight-bold">
              {{ unreadCount }} new
            </q-badge>
          </div>
          <q-btn
            v-if="unreadCount > 0"
            flat
            dense
            no-caps
            label="Mark all read"
            color="primary"
            class="text-caption text-weight-bold"
            @click="markAllRead"
          />
        </div>

        <!-- Notification List -->
        <q-list separator class="notification-list" style="max-height: 380px; overflow-y: auto">
          <template v-if="notifications.length > 0">
            <q-item
              v-for="item in notifications"
              :key="item.id"
              clickable
              v-ripple
              class="q-py-sm"
              :class="{ 'bg-slate-50': !item.read }"
              @click="handleNotificationClick(item)"
            >
              <q-item-section avatar top class="q-pr-sm" style="min-width: 40px">
                <div
                  class="notif-icon-circle"
                  :style="{ backgroundColor: item.bg, color: item.color }"
                >
                  <q-icon :name="item.icon" size="20px" />
                </div>
              </q-item-section>

              <q-item-section>
                <div class="row items-center justify-between no-wrap">
                  <span class="text-weight-bold text-body2 text-slate-900 leading-tight">{{
                    item.title
                  }}</span>
                  <span
                    class="text-caption text-slate-400 font-tabular text-right"
                    style="font-size: 0.68rem"
                    >{{ item.time }}</span
                  >
                </div>
                <div class="text-caption text-slate-600 q-mt-xs leading-normal">
                  {{ item.message }}
                </div>
              </q-item-section>

              <q-item-section side v-if="!item.read">
                <div class="unread-dot"></div>
              </q-item-section>
            </q-item>
          </template>

          <template v-else>
            <div class="column items-center justify-center q-pa-xl text-center">
              <q-icon name="check_circle" size="44px" color="primary" class="q-mb-sm opacity-80" />
              <div class="text-weight-bold text-slate-800 text-body1">All Caught Up!</div>
              <div class="text-caption text-slate-400 q-mt-xs">
                No low-stock alerts or pending urgent notifications.
              </div>
            </div>
          </template>
        </q-list>

        <!-- Footer link -->
        <div class="q-pa-sm text-center bg-slate-50 border-top-subtle">
          <q-btn
            flat
            dense
            no-caps
            color="primary"
            label="View Inventory Catalog →"
            class="text-caption text-weight-bold full-width"
            to="/inventory"
          />
        </div>
      </q-menu>
    </q-btn>

    <!-- 2. Sound Effects Toggle (Audio feedback) -->
    <q-btn
      flat
      round
      dense
      :icon="soundOn ? 'volume_up' : 'volume_off'"
      :color="soundOn ? 'positive' : 'grey-5'"
      class="header-icon-btn"
      @click="toggleSound"
    >
      <q-tooltip>{{
        soundOn ? 'Sound Effects: ON (Click to Mute)' : 'Sound Effects: MUTED (Click to Unmute)'
      }}</q-tooltip>
    </q-btn>

    <!-- 3. Database Backup & Recovery Button -->
    <q-btn
      flat
      round
      dense
      icon="cloud_download"
      color="slate-7"
      class="header-icon-btn"
      @click="openBackupModal"
    >
      <q-tooltip>Database Backup & Recovery</q-tooltip>
    </q-btn>

    <!-- 4. Help & User Guide Button -->
    <q-btn
      flat
      round
      dense
      icon="help_outline"
      color="slate-7"
      class="header-icon-btn"
      @click="showHelpGuide = true"
    >
      <q-tooltip>Help & User Guide</q-tooltip>
    </q-btn>

    <!-- 3. Cashier User Squircle Pill (Exact replica of user's photo!) -->
    <q-btn flat no-caps dense class="user-pill q-px-sm rounded-borders">
      <div class="user-avatar-circle q-mr-sm">
        {{ userInitials }}
      </div>
      <div class="column text-left gt-xs">
        <span class="text-weight-bold text-caption text-slate-900 leading-tight">{{
          userName
        }}</span>
        <span class="text-caption text-slate-400 font-medium" style="font-size: 0.7rem"
          >Main Branch</span
        >
      </div>
      <q-icon name="keyboard_arrow_down" size="16px" color="slate-5" class="q-ml-xs gt-xs" />

      <!-- Interactive User Menu -->
      <q-menu
        anchor="bottom right"
        self="top right"
        class="user-menu rounded-borders-lg shadow-md"
        style="min-width: 230px"
      >
        <div class="q-pa-md bg-slate-50 border-bottom-subtle">
          <div class="row items-center q-gutter-x-sm">
            <div class="user-avatar-circle" style="width: 38px; height: 38px; font-size: 0.95rem">
              {{ userInitials }}
            </div>
            <div class="column">
              <span class="text-weight-bold text-body2 text-slate-900 leading-tight">{{
                userName
              }}</span>
              <span class="text-caption text-slate-500 font-medium" style="font-size: 0.72rem"
                >Cashier • Main Branch</span
              >
            </div>
          </div>
        </div>

        <q-list class="q-py-xs">
          <q-item clickable v-ripple @click="showHelpGuide = true">
            <q-item-section avatar style="min-width: 36px">
              <q-icon name="help_outline" color="primary" size="20px" />
            </q-item-section>
            <q-item-section class="text-body2 text-slate-800">Help & User Guide</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="promptEditName">
            <q-item-section avatar style="min-width: 36px">
              <q-icon name="badge" color="primary" size="20px" />
            </q-item-section>
            <q-item-section class="text-body2 text-slate-800">Change Cashier Name</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/pos">
            <q-item-section avatar style="min-width: 36px">
              <q-icon name="receipt_long" color="primary" size="20px" />
            </q-item-section>
            <q-item-section class="text-body2 text-slate-800">POS Register</q-item-section>
          </q-item>

          <q-item clickable v-ripple to="/sales">
            <q-item-section avatar style="min-width: 36px">
              <q-icon name="bar_chart" color="primary" size="20px" />
            </q-item-section>
            <q-item-section class="text-body2 text-slate-800">Sales Tracker</q-item-section>
          </q-item>

          <q-item clickable v-ripple @click="openBackupModal">
            <q-item-section avatar style="min-width: 36px">
              <q-icon name="cloud_download" color="primary" size="20px" />
            </q-item-section>
            <q-item-section class="text-body2 text-slate-800"
              >Database Backup & Recovery</q-item-section
            >
          </q-item>

          <q-separator class="q-my-xs" />

          <q-item clickable v-ripple class="text-negative" @click="handleLogout">
            <q-item-section avatar style="min-width: 36px">
              <q-icon name="logout" color="negative" size="20px" />
            </q-item-section>
            <q-item-section class="text-body2 text-weight-bold">Log Out</q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>

    <!-- Help & Guide Modal Component -->
    <HelpGuideModal v-model="showHelpGuide" />

    <!-- Backup & Restore Modal Component -->
    <BackupRestoreModal ref="backupModalRef" />

    <!-- Server & Network Settings Modal Component -->
    <ServerSettingsModal ref="serverSettingsModalRef" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'
import HelpGuideModal from 'src/components/HelpGuideModal.vue'
import BackupRestoreModal from 'src/components/BackupRestoreModal.vue'
import ServerSettingsModal from 'src/components/ServerSettingsModal.vue'
import { isAudioEnabled, setAudioEnabled, playBeep } from 'src/utils/audio'

const router = useRouter()
const $q = useQuasar()

const showHelpGuide = ref(false)
const backupModalRef = ref(null)
const serverSettingsModalRef = ref(null)

function openServerSettings() {
  if (serverSettingsModalRef.value) {
    serverSettingsModalRef.value.openModal()
  }
}
const soundOn = ref(isAudioEnabled())

function toggleSound() {
  soundOn.value = !soundOn.value
  setAudioEnabled(soundOn.value)
  if (soundOn.value) {
    playBeep()
    $q.notify({
      color: 'positive',
      message: 'Sound effects enabled',
      icon: 'volume_up',
      timeout: 1200,
    })
  } else {
    $q.notify({
      color: 'grey-8',
      message: 'Sound effects muted',
      icon: 'volume_off',
      timeout: 1200,
    })
  }
}

function openBackupModal() {
  if (backupModalRef.value) {
    backupModalRef.value.openModal()
  }
}

const userName = ref(localStorage.getItem('userName') || 'Nichole_agrivet')
const notifications = ref([])
const hasMarkedAllRead = ref(false)

const userInitials = computed(() => {
  const name = userName.value.trim()
  if (!name) return 'AD'
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.slice(0, 2).toUpperCase()
})

const unreadCount = computed(() => {
  if (hasMarkedAllRead.value) return 0
  return notifications.value.filter((n) => !n.read).length
})

async function fetchNotifications() {
  try {
    const list = []
    // 1. Fetch low stock products
    const lowStockRes = await api.get('products/low-stock/')
    if (Array.isArray(lowStockRes.data)) {
      lowStockRes.data.forEach((p) => {
        const isBulk = p.unit_bulk_name && parseFloat(p.price_per_sack || 0) > 0
        const totalBase =
          parseFloat(p.stock_sacks || 0) * (parseFloat(p.units_per_bulk) || 50) +
          parseFloat(p.stock_kilos || 0)
        const isZero = isBulk ? totalBase <= 0 : parseFloat(p.stock_kilos || 0) <= 0
        const stockQty = isBulk ? parseFloat(p.stock_sacks || 0) : parseFloat(p.stock_kilos || 0)
        const unitName = isBulk ? p.unit_bulk_name || 'sack' : p.unit_retail_name || 'item'

        if (isZero) {
          list.push({
            id: `out-of-stock-${p.id}`,
            title: `Out of Stock: ${p.name}`,
            message: `0 ${unitName}s available. Replenish inventory immediately.`,
            time: 'Out of Stock',
            icon: 'remove_shopping_cart',
            color: '#dc2626',
            bg: '#fee2e2',
            route: '/inventory',
            read: false,
          })
        } else {
          list.push({
            id: `low-stock-${p.id}`,
            title: `Low Stock: ${p.name}`,
            message: `Only ${stockQty} ${unitName}(s) remaining (Alert threshold: ${p.low_stock_threshold || 5}).`,
            time: 'Low Stock',
            icon: 'warning',
            color: '#d97706',
            bg: '#fef3c7',
            route: '/inventory',
            read: false,
          })
        }
      })
    }

    // 2. Fetch customers with high utang
    const custRes = await api.get('customers/')
    if (Array.isArray(custRes.data)) {
      const debtCusts = custRes.data.filter((c) => parseFloat(c.total_utang || 0) >= 1000)
      debtCusts.slice(0, 3).forEach((c) => {
        list.push({
          id: `debt-cust-${c.id}`,
          title: `Utang Balance: ${c.name}`,
          message: `Has an outstanding balance of ₱${parseFloat(c.total_utang).toFixed(2)}.`,
          time: 'Notice',
          icon: 'account_balance_wallet',
          color: '#e11d48',
          bg: '#ffe4e6',
          route: '/credit',
          read: false,
        })
      })
    }

    notifications.value = list
  } catch (err) {
    console.error('Failed to load notifications:', err)
  }
}

function markAllRead() {
  hasMarkedAllRead.value = true
  notifications.value.forEach((n) => {
    n.read = true
  })
  $q.notify({
    message: 'All notifications marked as read',
    color: 'primary',
    icon: 'done_all',
    position: 'top',
    timeout: 1200,
  })
}

function handleNotificationClick(item) {
  item.read = true
  if (item.route) {
    router.push(item.route)
  }
}

function promptEditName() {
  $q.dialog({
    title: 'Cashier Profile',
    message: 'Enter Cashier / User Name:',
    prompt: {
      model: userName.value,
      type: 'text',
      isValid: (val) => val.trim().length > 0,
    },
    cancel: true,
    persistent: true,
  }).onOk((data) => {
    const trimmed = data.trim()
    if (trimmed) {
      userName.value = trimmed
      localStorage.setItem('userName', trimmed)
      $q.notify({
        color: 'positive',
        message: `Cashier name updated to "${trimmed}"`,
        icon: 'check',
        timeout: 1500,
      })
    }
  })
}

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

onMounted(() => {
  fetchNotifications()
})
</script>

<style scoped lang="scss">
.top-header-controls {
  user-select: none;
}

.header-icon-btn {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: all 0.15s ease;
  &:hover {
    background-color: #f8fafc;
    border-color: #cbd5e1;
  }
}

.notification-badge {
  top: -2px;
  right: -2px;
  font-size: 0.65rem;
  font-weight: 800;
  padding: 3px 5px;
}

.user-pill {
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  padding: 4px 10px;
  border-radius: 12px;
  height: 42px;
  transition: all 0.15s ease;
  &:hover {
    border-color: #cbd5e1;
    background-color: #f8fafc;
  }
}

.user-avatar-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #ff7043; /* Exact coral/orange tone from user screenshot */
  color: #ffffff;
  font-weight: 800;
  font-size: 0.78rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notif-icon-circle {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.unread-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #0d6832;
}

.border-bottom-subtle {
  border-bottom: 1px solid #f1f5f9;
}
.border-top-subtle {
  border-top: 1px solid #f1f5f9;
}
</style>
