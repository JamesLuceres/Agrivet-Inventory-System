<template>
  <transition name="splash-fade">
    <div v-if="isVisible" class="app-splash-screen" @click="dismissSplash">
      <!-- Ambient Glows -->
      <div class="ambient-glow glow-1"></div>
      <div class="ambient-glow glow-2"></div>

      <!-- Floating Decorative Elements -->
      <div class="floating-particle leaf-1">🌿</div>
      <div class="floating-particle leaf-2">🌾</div>
      <div class="floating-particle leaf-3">✨</div>
      <div class="floating-particle leaf-4">🍃</div>

      <!-- Center Mascot & Animated Branding -->
      <div class="splash-center-content">
        <div class="mascot-animation-wrapper">
          <img
            :src="logoUrl"
            alt="Nichole Agrivet Mascot"
            class="mascot-img"
          />
          <div class="mascot-ground-shadow"></div>
        </div>

        <div class="splash-text-group q-mt-md">
          <div class="splash-app-title">NICHOLE AGRIVET</div>
          <div class="splash-app-subtitle">Point of Sale & Inventory System</div>
        </div>

        <!-- Sleek Loading Bar -->
        <div class="splash-loader-bar q-mt-lg">
          <div class="splash-loader-progress"></div>
        </div>
        <div class="text-caption text-slate-500 q-mt-xs font-medium" style="font-size: 0.72rem">
          Initializing store terminal...
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import logoUrl from 'src/images/Nichole Agrivet.png'

const isVisible = ref(true)

function dismissSplash() {
  isVisible.value = false
}

onMounted(() => {
  // Check if splash was already shown in this browser session
  const alreadyShown = sessionStorage.getItem('splash_shown')
  if (alreadyShown) {
    isVisible.value = false
    return
  }

  // Display for 1.8 seconds then smoothly fade out
  setTimeout(() => {
    isVisible.value = false
    sessionStorage.setItem('splash_shown', 'true')
  }, 1800)
})
</script>

<style scoped>
.app-splash-screen {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 99999;
  background-color: #fcf1ea;
  background-image:
    radial-gradient(circle at 80% 30%, #ffdfd0 0%, transparent 45%),
    radial-gradient(circle at 20% 70%, #ffe9de 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, #fbf3ee 0%, #f8ebe2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  user-select: none;
  cursor: pointer;
}

/* Ambient Glows */
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}
.glow-1 {
  width: 450px;
  height: 450px;
  background: rgba(255, 170, 130, 0.4);
  top: -60px;
  right: 15%;
}
.glow-2 {
  width: 400px;
  height: 400px;
  background: rgba(255, 210, 180, 0.45);
  bottom: -40px;
  left: 10%;
}

/* Floating Decorative Elements */
.floating-particle {
  position: absolute;
  pointer-events: none;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.06));
  animation: floatParticle 5s ease-in-out infinite;
}
.leaf-1 {
  top: 20%;
  left: 22%;
  font-size: 28px;
  animation-duration: 4.8s;
}
.leaf-2 {
  top: 24%;
  right: 25%;
  font-size: 32px;
  animation-duration: 6s;
  animation-delay: 0.8s;
}
.leaf-3 {
  bottom: 22%;
  left: 28%;
  font-size: 26px;
  animation-duration: 5.2s;
  animation-delay: 1.2s;
}
.leaf-4 {
  bottom: 26%;
  right: 22%;
  font-size: 24px;
  animation-duration: 5.6s;
  animation-delay: 1.6s;
}

@keyframes floatParticle {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-16px) rotate(14deg);
  }
}

/* Center Content */
.splash-center-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  text-align: center;
}

.mascot-animation-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: mascotFloat 4.2s ease-in-out infinite;
}

.mascot-img {
  width: 220px;
  height: 220px;
  object-fit: contain;
  filter: drop-shadow(0 16px 28px rgba(210, 110, 70, 0.22));
}

@keyframes mascotFloat {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-15px) rotate(1.5deg);
  }
}

.mascot-ground-shadow {
  width: 170px;
  height: 18px;
  background: radial-gradient(
    ellipse at center,
    rgba(180, 100, 70, 0.25) 0%,
    rgba(180, 100, 70, 0) 70%
  );
  border-radius: 50%;
  margin-top: -6px;
  animation: shadowPulse 4.2s ease-in-out infinite;
}

@keyframes shadowPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.85;
  }
  50% {
    transform: scale(0.82);
    opacity: 0.45;
  }
}

.splash-app-title {
  font-size: 1.7rem;
  font-weight: 900;
  color: #1e293b;
  letter-spacing: 0.04em;
  line-height: 1.2;
}

.splash-app-subtitle {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
  letter-spacing: 0.02em;
  margin-top: 4px;
}

/* Loader Bar */
.splash-loader-bar {
  width: 180px;
  height: 4px;
  background: rgba(0, 0, 0, 0.08);
  border-radius: 99px;
  overflow: hidden;
  position: relative;
}

.splash-loader-progress {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #ff7a45, #0d6832);
  border-radius: 99px;
  animation: loadProgress 1.6s ease-in-out infinite;
}

@keyframes loadProgress {
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(0%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* Smooth Fade-out Transition */
.splash-fade-leave-active {
  transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
.splash-fade-leave-to {
  opacity: 0;
  transform: scale(1.04);
}
</style>
