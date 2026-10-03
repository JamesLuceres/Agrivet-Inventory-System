import { defineRouter } from '#q-app/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory,
} from 'vue-router'
import routes from './routes'

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default defineRouter((/* { store, ssrContext } */) => {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : process.env.VUE_ROUTER_MODE === 'history'
      ? createWebHistory
      : createWebHashHistory

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,

    // Leave this as is and make changes in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    history: createHistory(process.env.VUE_ROUTER_BASE),
  })

  // Global Navigation Guard for Authentication
  Router.beforeEach((to) => {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'

    // If route requires authentication and user is not logged in -> redirect to /login
    if (to.matched.some((record) => record.meta.requiresAuth) && !isLoggedIn) {
      return '/login'
    }

    // If already logged in and navigating to /login -> redirect to dashboard
    if (to.path === '/login' && isLoggedIn) {
      return '/'
    }
  })

  // Global Error Handler for dynamic import/chunk loading
  Router.onError((error, to) => {
    if (error?.message?.includes('Failed to fetch dynamically imported module')) {
      if (to?.fullPath) {
        window.location.href = to.fullPath
      } else {
        window.location.reload()
      }
    }
  })

  return Router
})
