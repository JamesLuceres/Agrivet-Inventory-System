<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'

onMounted(async () => {
  // 1. Lock orientation to landscape on tablets / devices supporting Screen Orientation API
  try {
    if (window.screen?.orientation?.lock) {
      window.screen.orientation.lock('landscape').catch(() => {})
    }
  } catch {
    // Graceful fallback
  }

  // 2. Request Screen Wake Lock so tablet screen stays awake on counter
  try {
    if ('wakeLock' in navigator) {
      await navigator.wakeLock.request('screen').catch(() => {})
      document.addEventListener('visibilitychange', async () => {
        if (document.visibilityState === 'visible' && 'wakeLock' in navigator) {
          await navigator.wakeLock.request('screen').catch(() => {})
        }
      })
    }
  } catch {
    // Graceful fallback
  }
})
</script>
