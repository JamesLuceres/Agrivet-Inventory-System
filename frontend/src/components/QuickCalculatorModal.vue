<template>
  <q-dialog v-model="isOpen">
    <q-card
      style="width: 340px; max-width: 90vw; border-radius: 20px"
      class="q-pa-sm bg-slate-900 text-white"
    >
      <!-- Calculator Header -->
      <q-card-section class="row items-center justify-between q-pb-none">
        <div class="row items-center q-gutter-x-xs">
          <q-icon name="calculate" color="orange" size="22px" />
          <span class="text-subtitle1 text-weight-bold">Agrivet Calculator</span>
        </div>
        <q-btn flat round dense icon="close" color="grey-5" v-close-popup />
      </q-card-section>

      <!-- Calculator Screen Display -->
      <q-card-section class="q-pt-sm q-pb-xs">
        <div class="calc-screen q-pa-md rounded-borders bg-slate-800 text-right">
          <div class="calc-history text-slate-400 font-mono text-caption" style="min-height: 18px">
            {{ formula || '&nbsp;' }}
          </div>
          <div
            class="calc-display text-h5 text-weight-bolder text-white font-mono num-tabular q-mt-xs"
          >
            {{ currentInput || '0' }}
          </div>
        </div>
      </q-card-section>

      <!-- Calculator Keypad Grid -->
      <q-card-section class="q-pt-none">
        <div class="calc-grid">
          <q-btn
            unelevated
            class="calc-btn text-orange-4 bg-slate-700"
            label="C"
            @click="clearAll"
          />
          <q-btn
            unelevated
            class="calc-btn text-orange-4 bg-slate-700"
            icon="backspace"
            @click="backspace"
          />
          <q-btn
            unelevated
            class="calc-btn text-orange-4 bg-slate-700"
            label="%"
            @click="applyPercent"
          />
          <q-btn
            unelevated
            class="calc-btn text-white bg-deep-orange-7"
            label="÷"
            @click="setOperator('/')"
          />

          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="7"
            @click="appendDigit('7')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="8"
            @click="appendDigit('8')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="9"
            @click="appendDigit('9')"
          />
          <q-btn
            unelevated
            class="calc-btn text-white bg-deep-orange-7"
            label="×"
            @click="setOperator('*')"
          />

          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="4"
            @click="appendDigit('4')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="5"
            @click="appendDigit('5')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="6"
            @click="appendDigit('6')"
          />
          <q-btn
            unelevated
            class="calc-btn text-white bg-deep-orange-7"
            label="-"
            @click="setOperator('-')"
          />

          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="1"
            @click="appendDigit('1')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="2"
            @click="appendDigit('2')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="3"
            @click="appendDigit('3')"
          />
          <q-btn
            unelevated
            class="calc-btn text-white bg-deep-orange-7"
            label="+"
            @click="setOperator('+')"
          />

          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="0"
            @click="appendDigit('0')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="00"
            @click="appendDigit('00')"
          />
          <q-btn
            unelevated
            class="calc-btn bg-slate-800 text-white"
            label="."
            @click="appendDecimal"
          />
          <q-btn
            unelevated
            class="calc-btn text-white bg-positive text-weight-bold"
            label="="
            @click="calculateResult"
          />
        </div>

        <!-- Copy Action Button -->
        <q-btn
          unelevated
          outline
          color="orange"
          icon="content_copy"
          label="Copy Result"
          class="full-width q-mt-sm"
          @click="copyResult"
        />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { playBeep, playChime } from 'src/utils/audio'

const $q = useQuasar()
const isOpen = ref(false)

const formula = ref('')
const currentInput = ref('0')
const operator = ref(null)
const previousValue = ref(null)
const resetNext = ref(false)

function openModal() {
  isOpen.value = true
}

function appendDigit(digit) {
  playBeep()
  if (currentInput.value === '0' || resetNext.value) {
    currentInput.value = digit
    resetNext.value = false
  } else {
    currentInput.value += digit
  }
}

function appendDecimal() {
  playBeep()
  if (resetNext.value) {
    currentInput.value = '0.'
    resetNext.value = false
    return
  }
  if (!currentInput.value.includes('.')) {
    currentInput.value += '.'
  }
}

function clearAll() {
  playBeep()
  formula.value = ''
  currentInput.value = '0'
  operator.value = null
  previousValue.value = null
  resetNext.value = false
}

function backspace() {
  playBeep()
  if (currentInput.value.length > 1) {
    currentInput.value = currentInput.value.slice(0, -1)
  } else {
    currentInput.value = '0'
  }
}

function applyPercent() {
  playBeep()
  const val = parseFloat(currentInput.value) || 0
  currentInput.value = String(val / 100)
}

function setOperator(op) {
  playBeep()
  const val = parseFloat(currentInput.value) || 0
  if (previousValue.value !== null && operator.value && !resetNext.value) {
    calculateResult(false)
  } else {
    previousValue.value = val
  }
  operator.value = op
  const opSymbol = op === '*' ? '×' : op === '/' ? '÷' : op
  formula.value = `${previousValue.value} ${opSymbol}`
  resetNext.value = true
}

function calculateResult(isEqualKey = true) {
  if (previousValue.value === null || !operator.value) return
  const current = parseFloat(currentInput.value) || 0
  let res = 0

  if (operator.value === '+') res = previousValue.value + current
  else if (operator.value === '-') res = previousValue.value - current
  else if (operator.value === '*') res = previousValue.value * current
  else if (operator.value === '/') res = current !== 0 ? previousValue.value / current : 0

  const rounded = parseFloat(res.toFixed(4))
  if (isEqualKey) {
    playChime()
    formula.value = `${previousValue.value} ${operator.value === '*' ? '×' : operator.value === '/' ? '÷' : operator.value} ${current} =`
    currentInput.value = String(rounded)
    previousValue.value = null
    operator.value = null
    resetNext.value = true
  } else {
    previousValue.value = rounded
    currentInput.value = String(rounded)
    resetNext.value = true
  }
}

function copyResult() {
  playBeep()
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(currentInput.value).then(() => {
      $q.notify({
        color: 'positive',
        message: `Copied ${currentInput.value} to clipboard!`,
        icon: 'content_paste',
        timeout: 1200,
      })
    })
  }
}

defineExpose({
  openModal,
})
</script>

<style scoped>
.calc-screen {
  border: 1px solid #334155;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
}
.calc-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}
.calc-btn {
  height: 52px;
  font-size: 1.15rem;
  border-radius: 12px;
}
</style>
