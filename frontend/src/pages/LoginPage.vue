<template>
  <div class="login-wrapper">
    <!-- Ambient Background Lighting & Floating Leaves -->
    <div class="ambient-glow glow-1"></div>
    <div class="ambient-glow glow-2"></div>
    <div class="ambient-glow glow-3"></div>

    <!-- Floating Decorative Leaves (matching reference aesthetic) -->
    <div class="floating-particle leaf-1">🍃</div>
    <div class="floating-particle leaf-2">🌾</div>
    <div class="floating-particle leaf-3">🍃</div>
    <div class="floating-particle leaf-4">🌾</div>
    <div class="floating-particle leaf-5">🍃</div>
    <div class="floating-particle leaf-6">✨</div>

    <!-- Main Container -->
    <div class="content-container">
      <!-- Left Side: Soft Frosted Login Card -->
      <div class="login-card-col">
        <div class="glass-card">
          <!-- Small Brand Subtitle -->
          <div class="brand-badge row items-center q-gutter-x-xs q-mb-xs">
            <q-icon name="pets" size="14px" color="deep-orange-6" />
            <span class="text-caption text-weight-bold text-deep-orange-7">Nichole Agrivet</span>
          </div>

          <!-- Main Title -->
          <h1 class="login-title q-my-none">Login</h1>
          <p class="login-subtitle text-slate-500 q-mt-xs q-mb-lg">
            Inventory & Point of Sale Management
          </p>

          <q-form @submit.prevent="handleLogin" class="q-gutter-y-md">
            <!-- Username Input -->
            <div class="input-group">
              <label class="input-label">Username</label>
              <q-input
                v-model="username"
                placeholder="Enter username"
                outlined
                dense
                class="custom-pill-input"
                :rules="[(val) => !!val || 'Username is required']"
              >
                <template v-slot:prepend>
                  <q-icon name="person_outline" color="grey-6" size="20px" />
                </template>
              </q-input>
            </div>

            <!-- Password Input -->
            <div class="input-group">
              <div class="row items-center justify-between">
                <label class="input-label">Password</label>
              </div>
              <q-input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Password"
                outlined
                dense
                class="custom-pill-input"
                :rules="[(val) => !!val || 'Password is required']"
              >
                <template v-slot:prepend>
                  <q-icon name="lock_outline" color="grey-6" size="20px" />
                </template>
                <template v-slot:append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer text-grey-6"
                    size="20px"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>
            </div>

            <!-- Options Row -->
            <div class="row items-center justify-between q-py-xs">
              <q-checkbox
                v-model="rememberMe"
                label="Remember me"
                color="deep-orange"
                dense
                size="sm"
                class="text-caption text-slate-600"
              />
              <span class="text-caption text-deep-orange-8 text-weight-medium cursor-pointer">
                Offline Terminal
              </span>
            </div>

            <!-- Error Banner -->
            <q-banner
              v-if="errorMessage"
              class="bg-red-1 text-negative rounded-borders border-red q-pa-sm text-caption"
            >
              <template v-slot:avatar>
                <q-icon name="error_outline" color="negative" size="20px" />
              </template>
              {{ errorMessage }}
            </q-banner>

            <!-- Sign In Action Button -->
            <div class="q-pt-xs">
              <q-btn
                type="submit"
                unelevated
                size="lg"
                class="full-width sign-in-btn text-weight-bold"
                :loading="loading"
                label="Sign In"
              />
            </div>

            <!-- Store Info Footer -->
            <div class="text-center text-caption text-slate-400 q-pt-md">
              Infinix XPAD 30 Pro • Standalone POS
            </div>
          </q-form>
        </div>
      </div>

      <!-- Right Side: Big Mascot Presentation -->
      <div class="mascot-col flex flex-center">
        <div class="mascot-stage text-center">
          <!-- Animated Mascot Character -->
          <div class="mascot-img-wrapper">
            <img :src="logoUrl" alt="Nichole Agrivet Mascot" class="mascot-img" />
          </div>
          <!-- Ground Ambient Shadow -->
          <div class="mascot-ground-shadow"></div>
          <!-- Warm Welcoming Caption -->
          <div class="mascot-caption q-mt-md">
            <div class="text-h6 text-weight-bold text-slate-800 tracking-tight">
              Welcome to Nichole Agrivet
            </div>
            <div class="text-caption text-slate-500 q-mt-xs">
              Quality Feeds, Veterinary Supplies & Fast Service
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import logoUrl from 'src/images/Nichole Agrivet.png'

const router = useRouter()
const $q = useQuasar()

const username = ref('Nichole_agrivet')
const password = ref('NicholeJarmai#0719')
const rememberMe = ref(true)
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  setTimeout(() => {
    const inputUser = username.value.trim().toLowerCase()
    const inputPass = password.value.trim()

    // Validate credentials
    const validUsernames = ['nichole_agrivet', 'nicholeagrivet', 'admin']
    const isCorrectUser = validUsernames.includes(inputUser)
    const isCorrectPass =
      inputPass === 'NicholeJarmai#0719' || (inputUser === 'admin' && inputPass === 'admin123')

    if (isCorrectUser && isCorrectPass) {
      localStorage.removeItem('isLoggedOut')
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('userName', 'Nichole_agrivet')

      $q.notify({
        color: 'positive',
        message: 'Welcome back, Nichole Agrivet! Successfully signed in.',
        icon: 'check_circle',
        timeout: 2500,
      })

      router.push('/')
    } else {
      errorMessage.value = 'Invalid username or password. Please check your credentials.'
    }
    loading.value = false
  }, 600)
}
</script>

<style scoped>
/* Page Container & Background */
.login-wrapper {
  min-height: 100vh;
  width: 100vw;
  background-color: #fcf1ea;
  background-image:
    radial-gradient(circle at 80% 30%, #ffdfd0 0%, transparent 45%),
    radial-gradient(circle at 20% 70%, #ffe9de 0%, transparent 40%),
    radial-gradient(circle at 50% 50%, #fbf3ee 0%, #f8ebe2 100%);
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
}

/* Ambient Glows */
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
}
.glow-1 {
  width: 420px;
  height: 420px;
  background: rgba(255, 170, 130, 0.35);
  top: -60px;
  right: 15%;
}
.glow-2 {
  width: 380px;
  height: 380px;
  background: rgba(255, 210, 180, 0.4);
  bottom: -40px;
  left: 10%;
}
.glow-3 {
  width: 250px;
  height: 250px;
  background: rgba(249, 115, 22, 0.15);
  top: 40%;
  left: 45%;
}

/* Floating Decorative Leaves */
.floating-particle {
  position: absolute;
  pointer-events: none;
  z-index: 1;
  user-select: none;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.05));
  animation: floatLeaf 6s ease-in-out infinite;
}
.leaf-1 {
  top: 18%;
  right: 36%;
  font-size: 24px;
  animation-duration: 5s;
  animation-delay: 0s;
}
.leaf-2 {
  top: 12%;
  right: 18%;
  font-size: 28px;
  animation-duration: 6.5s;
  animation-delay: 1s;
}
.leaf-3 {
  bottom: 24%;
  right: 42%;
  font-size: 22px;
  animation-duration: 4.8s;
  animation-delay: 0.5s;
}
.leaf-4 {
  bottom: 16%;
  right: 12%;
  font-size: 26px;
  animation-duration: 7s;
  animation-delay: 2s;
}
.leaf-5 {
  top: 30%;
  right: 8%;
  font-size: 20px;
  animation-duration: 5.4s;
  animation-delay: 1.5s;
}
.leaf-6 {
  top: 45%;
  right: 46%;
  font-size: 18px;
  animation-duration: 4.2s;
  animation-delay: 2.5s;
}

@keyframes floatLeaf {
  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-16px) rotate(14deg);
  }
}

/* Content Container (Two Column Layout) */
.content-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 1100px;
  z-index: 2;
  gap: 48px;
}

/* Left Column: Glass Card */
.login-card-col {
  flex: 0 0 420px;
  max-width: 440px;
  width: 100%;
}

.glass-card {
  background: rgba(255, 255, 255, 0.76);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1.5px solid rgba(255, 255, 255, 0.95);
  border-radius: 28px;
  box-shadow: 0 20px 45px -10px rgba(220, 120, 80, 0.18);
  padding: 40px 36px;
}

.login-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1.15;
  letter-spacing: -0.02em;
}

.login-subtitle {
  font-size: 0.92rem;
  line-height: 1.4;
}

/* Input Group Styles */
.input-group {
  display: flex;
  flex-direction: column;
}

.input-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #475569;
  margin-bottom: 6px;
}

:deep(.custom-pill-input .q-field__control) {
  background: #ffffff !important;
  border-radius: 12px !important;
  border: 1.5px solid #f1ded2 !important;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.02);
  transition: all 0.25s ease;
  height: 48px !important;
}

:deep(.custom-pill-input .q-field__control:hover) {
  border-color: #f97316 !important;
}

:deep(.custom-pill-input.q-field--focused .q-field__control) {
  border-color: #f97316 !important;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.15) !important;
}

:deep(.custom-pill-input .q-field__native) {
  font-size: 0.92rem;
  font-weight: 500;
  color: #1e293b;
}

/* Sign In Button */
.sign-in-btn {
  background: linear-gradient(135deg, #ff5722 0%, #f44336 100%) !important;
  color: #ffffff !important;
  border-radius: 12px !important;
  height: 48px;
  font-size: 1rem;
  letter-spacing: 0.01em;
  box-shadow: 0 10px 22px rgba(244, 67, 54, 0.32) !important;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease;
}

.sign-in-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 26px rgba(244, 67, 54, 0.42) !important;
}

.sign-in-btn:active {
  transform: translateY(0);
}

/* Right Column: Mascot Stage */
.mascot-col {
  flex: 1;
  max-width: 520px;
}

.mascot-stage {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.mascot-img-wrapper {
  animation: mascotFloat 4.5s ease-in-out infinite;
  display: inline-block;
}

.mascot-img {
  width: 100%;
  max-width: 380px;
  height: auto;
  max-height: 420px;
  object-fit: contain;
  filter: drop-shadow(0 15px 25px rgba(210, 110, 70, 0.18));
}

@keyframes mascotFloat {
  0%,
  100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-14px) rotate(1.2deg);
  }
}

.mascot-ground-shadow {
  width: 260px;
  height: 22px;
  background: radial-gradient(
    ellipse at center,
    rgba(180, 100, 70, 0.22) 0%,
    rgba(180, 100, 70, 0) 70%
  );
  border-radius: 50%;
  margin-top: -6px;
  animation: shadowPulse 4.5s ease-in-out infinite;
}

@keyframes shadowPulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(0.85);
    opacity: 0.5;
  }
}

.mascot-caption {
  max-width: 320px;
}

/* Responsive adjustments for mobile/smaller screens */
@media (max-width: 900px) {
  .content-container {
    flex-direction: column-reverse;
    gap: 24px;
    padding: 12px;
  }
  .login-card-col {
    flex: auto;
    width: 100%;
  }
  .mascot-img {
    max-width: 220px;
    max-height: 240px;
  }
  .mascot-caption {
    display: none;
  }
}
</style>
