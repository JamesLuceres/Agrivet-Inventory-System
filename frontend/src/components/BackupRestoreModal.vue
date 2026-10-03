<template>
  <q-dialog v-model="isOpen">
    <q-card style="width: 580px; max-width: 95vw; border-radius: 20px" class="q-pa-sm">
      <!-- Modal Header -->
      <q-card-section class="row items-center justify-between q-pb-none">
        <div class="row items-center q-gutter-x-sm">
          <q-avatar size="40px" color="orange-1" text-color="deep-orange-8" icon="cloud_download" />
          <div>
            <div class="text-h6 text-weight-bold text-slate-800">Database Backup & Recovery</div>
            <div class="text-caption text-slate-500">Safeguard your sales records and customer utang</div>
          </div>
        </div>
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>

      <!-- Main Body -->
      <q-card-section class="q-gutter-y-md q-pt-md">
        <!-- Info Alert -->
        <q-banner class="bg-blue-1 text-slate-800 rounded-borders q-pa-sm text-caption">
          <template v-slot:avatar>
            <q-icon name="shield" color="primary" size="24px" />
          </template>
          Regularly exporting a backup ensures your store data is safe if your tablet is replaced, damaged, or formatted.
        </q-banner>

        <!-- 1. Export Backup Card -->
        <q-card flat bordered class="q-pa-md rounded-borders bg-slate-50 border-slate">
          <div class="row items-center justify-between q-mb-sm">
            <div class="row items-center q-gutter-x-sm">
              <q-icon name="file_download" color="positive" size="24px" />
              <div>
                <div class="text-weight-bold text-slate-800">1-Click Full Backup (JSON)</div>
                <div class="text-caption text-slate-500">All products, stock counts, customers, utang, and sales</div>
              </div>
            </div>
            <q-btn
              unelevated
              color="positive"
              icon="download"
              label="Download Backup"
              :loading="exporting"
              @click="handleExportBackup"
            />
          </div>
        </q-card>

        <!-- 2. Restore Backup Card -->
        <q-card flat bordered class="q-pa-md rounded-borders bg-orange-1 border-orange-2">
          <div class="row items-start justify-between q-mb-sm">
            <div class="row items-center q-gutter-x-sm">
              <q-icon name="restore_page" color="deep-orange-8" size="24px" />
              <div>
                <div class="text-weight-bold text-slate-800">Restore Database from Backup</div>
                <div class="text-caption text-slate-600">Select a previously exported <code>.json</code> backup file</div>
              </div>
            </div>
          </div>

          <div class="q-mt-sm">
            <q-file
              v-model="backupFile"
              outlined
              dense
              bg-color="white"
              accept=".json"
              label="Select .json backup file"
              class="q-mb-sm"
            >
              <template v-slot:prepend>
                <q-icon name="attach_file" />
              </template>
            </q-file>

            <q-btn
              unelevated
              color="deep-orange-7"
              class="full-width"
              icon="cloud_upload"
              label="Restore Selected Backup"
              :disable="!backupFile"
              :loading="restoring"
              @click="confirmRestore"
            />
          </div>
        </q-card>

        <!-- Status Result Banner -->
        <q-banner
          v-if="statusMessage"
          :class="[
            'rounded-borders q-pa-sm text-caption',
            isSuccess ? 'bg-green-1 text-positive' : 'bg-red-1 text-negative'
          ]"
        >
          <template v-slot:avatar>
            <q-icon :name="isSuccess ? 'check_circle' : 'error'" :color="isSuccess ? 'positive' : 'negative'" size="20px" />
          </template>
          {{ statusMessage }}
        </q-banner>
      </q-card-section>

      <!-- Footer Actions -->
      <q-card-actions align="right" class="q-px-md q-pb-md">
        <q-btn flat label="Close" color="grey-7" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { playChime, playWarning } from 'src/utils/audio'

const $q = useQuasar()
const isOpen = ref(false)
const exporting = ref(false)
const restoring = ref(false)
const backupFile = ref(null)
const statusMessage = ref('')
const isSuccess = ref(true)

function openModal() {
  statusMessage.value = ''
  backupFile.value = null
  isOpen.value = true
}

async function handleExportBackup() {
  exporting.value = true
  statusMessage.value = ''
  try {
    const res = await api.get('backup/export/')
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(res.data, null, 2))
    const downloadAnchor = document.createElement('a')
    const dateTag = new Date().toISOString().slice(0, 10)
    downloadAnchor.setAttribute('href', dataStr)
    downloadAnchor.setAttribute('download', `nichole_agrivet_backup_${dateTag}.json`)
    document.body.appendChild(downloadAnchor)
    downloadAnchor.click()
    downloadAnchor.remove()

    playChime()
    $q.notify({
      color: 'positive',
      message: 'Backup downloaded successfully! Save it to your Google Drive or USB drive.',
      icon: 'download_done',
      timeout: 3500,
    })
    statusMessage.value = 'Backup generated and downloaded successfully!'
    isSuccess.value = true
  } catch (err) {
    console.error(err)
    playWarning()
    $q.notify({ color: 'negative', message: 'Failed to generate backup.' })
    statusMessage.value = 'Error exporting backup. Please verify server connection.'
    isSuccess.value = false
  } finally {
    exporting.value = false
  }
}

function confirmRestore() {
  if (!backupFile.value) return

  $q.dialog({
    title: 'Confirm Database Restore',
    message: 'Restoring a backup will merge and update products, categories, customers, and transactions. Are you sure you want to proceed?',
    cancel: { flat: true, color: 'grey-7', label: 'Cancel' },
    ok: { color: 'deep-orange-8', label: 'Yes, Restore Now', unelevated: true, icon: 'warning' },
    persistent: true,
  }).onOk(() => {
    executeRestore()
  })
}

function executeRestore() {
  restoring.value = true
  statusMessage.value = ''

  const reader = new FileReader()
  reader.onload = async (e) => {
    try {
      const parsedData = JSON.parse(e.target.result)
      const res = await api.post('backup/restore/', parsedData)

      playChime()
      $q.notify({
        color: 'positive',
        message: 'Database restored successfully! Reloading data...',
        icon: 'cloud_done',
        timeout: 3000,
      })
      statusMessage.value = `Success: ${res.data.message || 'Data restored'}. Stats: ${JSON.stringify(res.data.stats || {})}`
      isSuccess.value = true
      backupFile.value = null

      setTimeout(() => {
        window.location.reload()
      }, 1500)
    } catch (err) {
      console.error(err)
      playWarning()
      const errMsg = err.response?.data?.error || 'Invalid backup JSON file or server error.'
      statusMessage.value = `Restore failed: ${errMsg}`
      isSuccess.value = false
      $q.notify({ color: 'negative', message: errMsg })
    } finally {
      restoring.value = false
    }
  }
  reader.onerror = () => {
    restoring.value = false
    statusMessage.value = 'Failed to read backup file.'
    isSuccess.value = false
  }
  reader.readAsText(backupFile.value)
}

defineExpose({
  openModal,
})
</script>

<style scoped>
.border-slate {
  border: 1px solid #e2e8f0;
}
.border-orange-2 {
  border: 1px solid #fed7aa;
}
</style>
