<template>
  <q-dialog v-model="isOpen">
    <q-card style="width: 580px; max-width: 95vw; border-radius: 20px" class="q-pa-sm">
      <!-- Header -->
      <q-card-section class="row items-center justify-between q-pb-none">
        <div class="row items-center q-gutter-x-sm">
          <q-avatar size="40px" color="emerald-1" text-color="positive" icon="point_of_sale" />
          <div>
            <div class="text-h6 text-weight-bold text-slate-800">Shift Z-Reading & Cash Count</div>
            <div class="text-caption text-slate-500">End-of-day cash drawer balancing & reconciliation</div>
          </div>
        </div>
        <q-btn flat round dense icon="close" v-close-popup />
      </q-card-section>

      <!-- Content -->
      <q-card-section class="q-gutter-y-md q-pt-md">
        <!-- Expected Cash KPI -->
        <div class="row q-col-gutter-sm">
          <div class="col-6">
            <div class="bg-slate-50 border-slate rounded-borders q-pa-sm text-center">
              <div class="text-caption text-slate-500 font-medium">System Cash Sales</div>
              <div class="text-weight-bolder text-body1 text-slate-900 num-tabular">
                ₱{{ systemCashSales.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
              </div>
            </div>
          </div>
          <div class="col-6">
            <div class="bg-slate-50 border-slate rounded-borders q-pa-sm text-center">
              <div class="text-caption text-slate-500 font-medium">Debt Collected (Utang)</div>
              <div class="text-weight-bolder text-body1 text-slate-900 num-tabular">
                ₱{{ systemDebtCollected.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
              </div>
            </div>
          </div>
        </div>

        <div class="bg-blue-50 border-blue rounded-borders q-pa-md row items-center justify-between">
          <div>
            <div class="text-caption text-primary text-weight-bold">TOTAL EXPECTED CASH IN DRAWER</div>
            <div class="text-caption text-slate-500">Cash sales + debt repayments</div>
          </div>
          <div class="text-h5 text-weight-bolder text-primary num-tabular">
            ₱{{ expectedCashTotal.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
          </div>
        </div>

        <!-- Denomination Counter -->
        <div>
          <div class="text-caption text-weight-bold text-slate-700 q-mb-xs">
            Physical Cash Denominations (Quantity Counted)
          </div>
          <div class="bg-white border-slate rounded-borders q-pa-sm q-gutter-y-xs">
            <div
              v-for="denom in denominations"
              :key="denom.value"
              class="row items-center justify-between text-caption q-py-xs border-bottom-subtle"
            >
              <div class="row items-center q-gutter-x-sm" style="min-width: 90px">
                <span class="text-weight-bold text-slate-800">₱{{ denom.value }}</span>
              </div>
              <div style="width: 90px">
                <q-input
                  v-model.number="denom.count"
                  type="number"
                  dense
                  outlined
                  min="0"
                  class="text-right text-weight-bold"
                  input-class="text-right"
                  @update:model-value="onCountChanged"
                />
              </div>
              <div class="text-weight-bold text-slate-900 num-tabular text-right" style="min-width: 90px">
                ₱{{ ((denom.count || 0) * denom.value).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
              </div>
            </div>

            <!-- Loose Coins Row -->
            <div class="row items-center justify-between text-caption q-py-xs">
              <span class="text-weight-bold text-slate-800">Loose Coins</span>
              <div style="width: 120px">
                <q-input
                  v-model.number="looseCoinsTotal"
                  type="number"
                  dense
                  outlined
                  min="0"
                  step="0.25"
                  prefix="₱"
                  class="text-right text-weight-bold"
                  input-class="text-right"
                  @update:model-value="onCountChanged"
                />
              </div>
              <div class="text-weight-bold text-slate-900 num-tabular text-right" style="min-width: 90px">
                ₱{{ (looseCoinsTotal || 0).toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Total Counted & Variance Banner -->
        <div
          class="rounded-borders q-pa-md row items-center justify-between"
          :class="[
            cashVariance === 0
              ? 'bg-green-1 border-green'
              : cashVariance > 0
                ? 'bg-amber-1 border-amber'
                : 'bg-red-1 border-red'
          ]"
        >
          <div>
            <div class="text-caption text-slate-600 font-medium">TOTAL COUNTED CASH</div>
            <div class="text-h6 text-weight-bolder text-slate-900 num-tabular">
              ₱{{ totalCountedCash.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
            </div>
          </div>
          <div class="text-right">
            <div class="text-caption text-weight-bold" :class="varianceTextColor">
              {{ varianceStatusLabel }}
            </div>
            <div class="text-h6 text-weight-bolder num-tabular" :class="varianceTextColor">
              {{ cashVariance >= 0 ? '+' : '' }}₱{{ cashVariance.toLocaleString('en-US', { minimumFractionDigits: 2 }) }}
            </div>
          </div>
        </div>
      </q-card-section>

      <!-- Footer Buttons -->
      <q-card-actions align="between" class="q-px-md q-pb-md">
        <q-btn flat label="Close" color="grey-7" v-close-popup />
        <div class="row q-gutter-x-sm">
          <q-btn
            outline
            color="primary"
            icon="bluetooth"
            label="Share / Bluetooth"
            @click="shareZReadingBluetooth"
          />
          <q-btn
            unelevated
            class="btn-agrivet-green"
            icon="print"
            label="Print Z-Reading Slip"
            @click="printZReadingSlip"
          />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import { playBeep, playChime, playWarning } from 'src/utils/audio'

const $q = useQuasar()
const isOpen = ref(false)

const systemCashSales = ref(0)
const systemDebtCollected = ref(0)
const looseCoinsTotal = ref(0)
const cashierName = ref(localStorage.getItem('userName') || 'Nichole_agrivet')

const denominations = ref([
  { value: 1000, count: 0 },
  { value: 500, count: 0 },
  { value: 200, count: 0 },
  { value: 100, count: 0 },
  { value: 50, count: 0 },
  { value: 20, count: 0 },
])

const expectedCashTotal = computed(() => {
  return systemCashSales.value + systemDebtCollected.value
})

const totalCountedCash = computed(() => {
  const bills = denominations.value.reduce((sum, d) => sum + (d.count || 0) * d.value, 0)
  return bills + (parseFloat(looseCoinsTotal.value) || 0)
})

const cashVariance = computed(() => {
  return parseFloat((totalCountedCash.value - expectedCashTotal.value).toFixed(2))
})

const varianceStatusLabel = computed(() => {
  if (cashVariance.value === 0) return 'BALANCED (EXACT)'
  if (cashVariance.value > 0) return 'CASH OVER'
  return 'CASH SHORT'
})

const varianceTextColor = computed(() => {
  if (cashVariance.value === 0) return 'text-positive'
  if (cashVariance.value > 0) return 'text-amber-9'
  return 'text-negative'
})

function onCountChanged() {
  playBeep()
}

async function openModal() {
  cashierName.value = localStorage.getItem('userName') || 'Nichole_agrivet'
  isOpen.value = true
  try {
    const res = await api.get('transactions/daily-summary/')
    systemCashSales.value = parseFloat(res.data.total_cash_revenue || 0)
    systemDebtCollected.value = parseFloat(res.data.total_debt_collected || 0)
  } catch (err) {
    console.error(err)
  }
}

function printZReadingSlip() {
  playChime()
  const dateStr = new Date().toLocaleString('en-PH', { dateStyle: 'medium', timeStyle: 'short' })
  const is58 = true
  const slipWidth = is58 ? '54mm' : '76mm'

  const existingIframe = document.getElementById('z-reading-print-frame')
  if (existingIframe) existingIframe.remove()

  const iframe = document.createElement('iframe')
  iframe.id = 'z-reading-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow.document
  doc.open()

  let denomRows = ''
  denominations.value.forEach((d) => {
    if (d.count > 0) {
      denomRows += `<div style="display:flex; justify-content:space-between;"><span>₱${d.value} x ${d.count}</span><span>₱${(d.value * d.count).toFixed(2)}</span></div>`
    }
  })
  if (looseCoinsTotal.value > 0) {
    denomRows += `<div style="display:flex; justify-content:space-between;"><span>Coins</span><span>₱${parseFloat(looseCoinsTotal.value).toFixed(2)}</span></div>`
  }

  doc.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>Z-Reading Slip</title>
        <style>
          @page { size: 58mm auto; margin: 0mm; }
          body { font-family: monospace; font-size: 11px; margin: 0; padding: 4px; color: #000; }
          .slip { width: 100%; max-width: ${slipWidth}; margin: 0 auto; text-align: center; }
          .divider { border-top: 1px dashed #000; margin: 4px 0; }
          .row { display: flex; justify-content: space-between; margin: 2px 0; }
        </style>
      </head>
      <body>
        <div class="slip">
          <div style="font-weight:bold; font-size:1.2em;">NICHOLE AGRIVET</div>
          <div>END-OF-DAY Z-READING</div>
          <div class="divider"></div>
          <div class="row"><span>Date:</span><span>${dateStr}</span></div>
          <div class="row"><span>Cashier:</span><span>${cashierName.value}</span></div>
          <div class="divider"></div>
          <div class="row"><span>Cash Sales:</span><span>₱${systemCashSales.value.toFixed(2)}</span></div>
          <div class="row"><span>Debt Repayments:</span><span>₱${systemDebtCollected.value.toFixed(2)}</span></div>
          <div class="row" style="font-weight:bold;"><span>EXPECTED CASH:</span><span>₱${expectedCashTotal.value.toFixed(2)}</span></div>
          <div class="divider"></div>
          <div style="text-align:left; font-weight:bold; margin-bottom:2px;">PHYSICAL CASH COUNT:</div>
          <div style="text-align:left;">${denomRows}</div>
          <div class="divider"></div>
          <div class="row" style="font-weight:bold; font-size:1.1em;"><span>TOTAL COUNTED:</span><span>₱${totalCountedCash.value.toFixed(2)}</span></div>
          <div class="row" style="font-weight:bold;"><span>VARIANCE:</span><span>${varianceStatusLabel.value} (${cashVariance.value >= 0 ? '+' : ''}₱${cashVariance.value.toFixed(2)})</span></div>
          <div class="divider"></div>
          <br><br>
          <div style="border-top: 1px solid #000; width: 70%; margin: 0 auto;"></div>
          <div>Cashier Signature</div>
          <div style="margin-top:4px;">Official Z-Report Validated</div>
        </div>
      </body>
    </html>
  `)
  doc.close()

  setTimeout(() => {
    try {
      iframe.contentWindow.focus()
      iframe.contentWindow.print()
    } catch (e) {
      console.error(e)
    }
  }, 200)
}

async function shareZReadingBluetooth() {
  playBeep()
  const dateStr = new Date().toLocaleString('en-PH', { dateStyle: 'medium', timeStyle: 'short' })
  let text = `================================\n`
  text += `        NICHOLE AGRIVET        \n`
  text += `     END-OF-DAY Z-READING       \n`
  text += `--------------------------------\n`
  text += `Date: ${dateStr}\n`
  text += `Cashier: ${cashierName.value}\n`
  text += `--------------------------------\n`
  text += `Cash Sales:      PHP ${systemCashSales.value.toFixed(2)}\n`
  text += `Debt Collected:  PHP ${systemDebtCollected.value.toFixed(2)}\n`
  text += `EXPECTED CASH:   PHP ${expectedCashTotal.value.toFixed(2)}\n`
  text += `--------------------------------\n`
  text += `TOTAL COUNTED:   PHP ${totalCountedCash.value.toFixed(2)}\n`
  text += `VARIANCE:        ${varianceStatusLabel.value} (${cashVariance.value >= 0 ? '+' : ''}PHP ${cashVariance.value.toFixed(2)})\n`
  text += `================================\n`
  text += `Cashier Signature: _____________\n`

  if (navigator.share) {
    try {
      await navigator.share({ title: 'Nichole Agrivet Z-Reading', text })
    } catch (e) {
      if (e.name !== 'AbortError') {
        navigator.clipboard?.writeText(text)
      }
    }
  } else {
    navigator.clipboard?.writeText(text)
    $q.notify({ color: 'positive', message: 'Z-Reading copied for Bluetooth printer app!' })
  }
}

defineExpose({
  openModal,
})
</script>

<style scoped>
.border-slate { border: 1px solid #e2e8f0; }
.border-blue { border: 1.5px solid #bfdbfe; }
.border-green { border: 1.5px solid #bbf7d0; }
.border-amber { border: 1.5px solid #fde68a; }
.border-red { border: 1.5px solid #fecdd3; }
.btn-agrivet-green {
  background-color: #0d6832 !important;
  color: #ffffff !important;
}
</style>
