import LoginPage from 'pages/LoginPage.vue'
import MainLayout from 'layouts/MainLayout.vue'
import IndexPage from 'pages/IndexPage.vue'
import POSPage from 'pages/POSPage.vue'
import InventoryPage from 'pages/InventoryPage.vue'
import CreditPage from 'pages/CreditPage.vue'
import SalesPage from 'pages/SalesPage.vue'
import ErrorNotFound from 'pages/ErrorNotFound.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginPage,
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', component: IndexPage },
      { path: 'pos', component: POSPage },
      { path: 'inventory', component: InventoryPage },
      { path: 'credit', component: CreditPage },
      { path: 'sales', component: SalesPage },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: ErrorNotFound,
  },
]

export default routes
