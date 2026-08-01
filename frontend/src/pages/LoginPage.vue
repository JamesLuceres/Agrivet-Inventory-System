<template>
  <div class="login-container flex flex-center">
    <div class="login-card-wrapper q-pa-md">
      <!-- Main Login Card -->
      <q-card flat bordered class="login-card bg-white shadow-10 overflow-hidden">
        <!-- Brand Header Section -->
        <div class="brand-header q-pa-xl text-center text-white relative-position">
          <q-avatar size="72px" class="bg-white shadow-5 q-mb-md overflow-hidden" style="border: 3px solid #059669">
            <img :src="logoUrl" alt="Nichole Agrivet Logo" style="object-fit: cover; transform: scale(1.15);" />
          </q-avatar>
          <div class="text-h5 text-weight-bold tracking-tight">Nichole Agrivet</div>
          <div class="text-caption text-emerald-100 font-medium q-mt-xs">
            Inventory & Point of Sale System
          </div>
        </div>

        <!-- Form Section -->
        <q-card-section class="q-pa-xl">
          <div class="text-h6 text-weight-bold text-slate-800 q-mb-xs">Welcome Back</div>
          <div class="text-caption text-slate-500 q-mb-lg">Please sign in to access your dashboard</div>

          <q-form @submit.prevent="handleLogin" class="q-gutter-y-md">
            <!-- Username Input -->
            <div>
              <div class="text-caption text-weight-bold text-slate-700 q-mb-xs">Username or Staff ID</div>
              <q-input
                v-model="username"
                placeholder="Enter your username (e.g. admin)"
                outlined
                dense
                class="login-input"
                :rules="[val => !!val || 'Username is required']"
              >
                <template v-slot:prepend>
                  <q-icon name="person" color="slate-500" />
                </template>
              </q-input>
            </div>

            <!-- Password Input -->
            <div>
              <div class="text-caption text-weight-bold text-slate-700 q-mb-xs">Password</div>
              <q-input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Enter password"
                outlined
                dense
                class="login-input"
                :rules="[val => !!val || 'Password is required']"
              >
                <template v-slot:prepend>
                  <q-icon name="lock" color="slate-500" />
                </template>
                <template v-slot:append>
                  <q-icon
                    :name="showPassword ? 'visibility_off' : 'visibility'"
                    class="cursor-pointer"
                    @click="showPassword = !showPassword"
                  />
                </template>
              </q-input>
            </div>

            <!-- Remember Me -->
            <div class="row items-center justify-between q-py-xs">
              <q-checkbox v-model="rememberMe" label="Remember me" color="primary" dense size="sm" class="text-slate-600 text-caption" />
            </div>

            <!-- Error Banner -->
            <q-banner v-if="errorMessage" class="bg-red-1 text-negative rounded-borders border-red q-pa-sm text-caption">
              <template v-slot:avatar>
                <q-icon name="error_outline" color="negative" size="20px" />
              </template>
              {{ errorMessage }}
            </q-banner>

            <!-- Login Button -->
            <q-btn
              type="submit"
              color="positive"
              size="lg"
              class="full-width q-py-sm shadow-3 text-weight-bold"
              style="background-color: #059669 !important;"
              :loading="loading"
              label="Sign In to System"
              icon-right="login"
            />
          </q-form>
        </q-card-section>
      </q-card>
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

const username = ref('admin')
const password = ref('admin123')
const rememberMe = ref(true)
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

function handleLogin() {
  loading.value = true
  errorMessage.value = ''

  setTimeout(() => {
    // Validate credentials
    if (username.value.trim() && password.value.trim()) {
      localStorage.setItem('isLoggedIn', 'true')
      localStorage.setItem('userName', username.value.trim())

      $q.notify({
        color: 'positive',
        message: `Welcome back, ${username.value}! Successfully signed in.`,
        icon: 'check_circle',
        timeout: 2500
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
.login-container {
  min-height: 100vh;
  width: 100vw;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #064e3b 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card-wrapper {
  width: 100%;
  max-width: 480px;
}

.login-card {
  border-radius: 16px !important;
  border: 1.5px solid rgba(255, 255, 255, 0.15) !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.35) !important;
}

.brand-header {
  background: linear-gradient(135deg, #0f172a 0%, #059669 100%);
  border-bottom: 2px solid #047857;
}

.text-emerald-100 {
  color: #d1fae5 !important;
}

.bg-slate-50 {
  background-color: #f8fafc !important;
}

.bg-slate-200 {
  background-color: #e2e8f0 !important;
}

.border-slate {
  border: 1px solid #e2e8f0;
}

.border-red {
  border: 1px solid #fecdd3;
}

.bg-red-1 {
  background-color: #fff1f2 !important;
}
</style>
