<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated class="bg-indigo-10 text-white">
      <q-toolbar class="q-py-sm">
        <q-toolbar-title class="text-weight-bold row items-center text-uppercase tracking-wide text-h5 q-pl-md">
          <q-icon name="storefront" class="q-mr-sm" size="md" />
          Nichole Agrivet POS
        </q-toolbar-title>

        <!-- API Connection Status -->
        <div class="row items-center q-mr-lg">
          <q-badge :color="apiConnected ? 'positive' : 'negative'" class="q-pa-sm text-subtitle2">
            <q-icon :name="apiConnected ? 'cloud_done' : 'cloud_off'" class="q-mr-xs" size="xs" />
            {{ apiConnected ? 'API Online' : 'API Offline' }}
          </q-badge>
        </div>

        <!-- Clock -->
        <div class="text-subtitle2 text-weight-bold text-uppercase gt-xs bg-indigo-9 q-px-md q-py-sm rounded-borders">
          <q-icon name="schedule" class="q-mr-xs" />
          {{ currentTime }}
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container class="bg-grey-2">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { api } from 'boot/axios'

const apiConnected = ref(false)
const currentTime = ref('')

// Update clock every second
let clockInterval
function updateTime() {
  const options = {
    weekday: 'short',
    year: 'numeric',
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
    // Ping categories endpoint (lightweight check)
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
  apiInterval = setInterval(checkApiStatus, 5000) // Poll every 5s
})

onBeforeUnmount(() => {
  clearInterval(clockInterval)
  clearInterval(apiInterval)
})
</script>

<style scoped>
.bg-grey-2 {
  background-color: #f3f4f6 !important; /* Neutral-100 grey background */
}
.tracking-wide {
  letter-spacing: 0.05em;
}
.rounded-borders {
  border-radius: 4px;
}
</style>
