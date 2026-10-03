<template>
  <q-dialog v-model="isOpen">
    <q-card style="width: 480px; max-width: 95vw; border-radius: 20px" class="q-pa-sm">
      <q-card-section class="row items-center justify-between q-pb-none">
        <div class="row items-center q-gutter-x-sm">
          <q-avatar size="40px" color="blue-1" text-color="primary" icon="settings_ethernet" />
          <div>
            <div class="text-h6 text-weight-bold text-slate-800">Server & Network Settings</div>
            <div class="text-caption text-slate-500">
              Configure counter PC or Standalone Tablet mode
            </div>
          </div>
        </div>
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>

      <q-card-section class="q-gutter-y-md q-pt-md">
        <!-- Connection Status -->
        <q-banner
          :class="[
            'rounded-borders q-pa-sm text-caption',
            isOnline ? 'bg-green-1 text-positive' : 'bg-amber-1 text-amber-9',
          ]"
        >
          <template v-slot:avatar>
            <q-icon
              :name="isOnline ? 'wifi' : 'wifi_off'"
              :color="isOnline ? 'positive' : 'amber-9'"
              size="20px"
            />
          </template>
          <div>
            <strong
              >Mode: {{ isOnline ? 'Connected to Store PC' : 'Standalone Offline Mode' }}</strong
            >
            <div class="text-slate-600 q-mt-xs">
              {{
                isOnline
                  ? 'Data syncs directly with counter PC database.'
                  : 'Tablet is running with local storage cache.'
              }}
            </div>
          </div>
        </q-banner>

        <!-- Server URL Input -->
        <div>
          <label class="text-caption text-weight-bold text-slate-700 q-mb-xs block">
            Counter PC Server URL
          </label>
          <q-input
            v-model="serverUrl"
            outlined
            dense
            placeholder="http://192.168.1.xxx:8000/api/"
            hint="Default: http://127.0.0.1:8000/api/"
            class="bg-white"
          >
            <template v-slot:prepend>
              <q-icon name="dns" color="grey-6" size="20px" />
            </template>
          </q-input>
        </div>

        <!-- Quick Preset Buttons -->
        <div class="row q-gutter-xs">
          <q-btn
            outline
            dense
            no-caps
            size="sm"
            label="Localhost (127.0.0.1)"
            color="primary"
            @click="serverUrl = 'http://127.0.0.1:8000/api/'"
          />
          <q-btn
            outline
            dense
            no-caps
            size="sm"
            label="Default Shop Wi-Fi"
            color="primary"
            @click="serverUrl = 'http://192.168.1.100:8000/api/'"
          />
        </div>

        <!-- Test Connection Result -->
        <div
          v-if="testResult"
          class="text-caption text-weight-medium"
          :class="testSuccess ? 'text-positive' : 'text-negative'"
        >
          <q-icon :name="testSuccess ? 'check_circle' : 'error'" class="q-mr-xs" />
          {{ testResult }}
        </div>
      </q-card-section>

      <q-card-actions align="between" class="q-px-md q-pb-md">
        <q-btn
          outline
          color="primary"
          icon="network_check"
          label="Test Ping"
          :loading="testing"
          @click="testConnection"
        />
        <div class="row q-gutter-x-sm">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            color="primary"
            icon="save"
            label="Save & Apply"
            @click="saveServerUrl"
          />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useQuasar } from 'quasar'
import { playBeep, playChime, playWarning } from 'src/utils/audio'

const $q = useQuasar()
const isOpen = ref(false)
const serverUrl = ref(localStorage.getItem('apiBaseURL') || 'http://127.0.0.1:8000/api/')
const isOnline = ref(true)
const testing = ref(false)
const testResult = ref('')
const testSuccess = ref(false)

function openModal() {
  serverUrl.value = localStorage.getItem('apiBaseURL') || 'http://127.0.0.1:8000/api/'
  testResult.value = ''
  isOpen.value = true
}

async function testConnection() {
  testing.value = true
  testResult.value = ''
  try {
    const formatted = serverUrl.value.endsWith('/') ? serverUrl.value : serverUrl.value + '/'
    const res = await axios.get(formatted + 'products/', { timeout: 3500 })
    if (res.status === 200) {
      testSuccess.value = true
      testResult.value = 'Connected! Server is online and responding.'
      isOnline.value = true
      playChime()
    }
  } catch (err) {
    testSuccess.value = false
    testResult.value = 'Could not reach server. Tablet will use offline local storage.'
    isOnline.value = false
    playWarning()
  } finally {
    testing.value = false
  }
}

function saveServerUrl() {
  let url = serverUrl.value.trim()
  if (!url.endsWith('/')) url += '/'
  localStorage.setItem('apiBaseURL', url)
  playBeep()
  $q.notify({
    color: 'positive',
    message: 'Server URL saved! Reloading application...',
    icon: 'save',
    timeout: 1500,
  })
  isOpen.value = false
  setTimeout(() => {
    window.location.reload()
  }, 800)
}

defineExpose({
  openModal,
})
</script>
