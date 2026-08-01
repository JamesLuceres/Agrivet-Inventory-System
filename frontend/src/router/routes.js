const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') },
      { path: 'pos', component: () => import('pages/POSPage.vue') },
      { path: 'inventory', component: () => import('pages/InventoryPage.vue') },
      { path: 'credit', component: () => import('pages/CreditPage.vue') },
      { path: 'sales', component: () => import('pages/SalesPage.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
