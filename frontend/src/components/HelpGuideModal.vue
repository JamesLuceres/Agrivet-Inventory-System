<template>
  <q-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)">
    <q-card style="width: 760px; max-width: 96vw; max-height: 90vh" class="column no-wrap rounded-borders-lg">
      <!-- 1. Header with Mascot & Title -->
      <q-card-section class="row items-center justify-between bg-slate-50 q-py-sm q-px-md border-bottom-subtle">
        <div class="row items-center q-gutter-x-sm">
          <div class="badge-mint q-pa-xs" style="width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center">
            <q-icon name="menu_book" size="22px" color="primary" />
          </div>
          <div>
            <div class="text-subtitle1 text-weight-bolder text-slate-900 leading-tight">
              Nichole Agrivet • POS User Guide & Ideas
            </div>
            <div class="text-caption text-slate-500" style="font-size: 0.75rem">
              Quick operating guide, tips, and best practices for tablet cashiers
            </div>
          </div>
        </div>
        <q-btn flat round dense icon="close" color="slate-6" v-close-popup />
      </q-card-section>

      <!-- 2. Navigation Tabs -->
      <q-card-section class="q-pa-none bg-white border-bottom-subtle">
        <q-tabs
          v-model="activeTab"
          dense
          no-caps
          align="left"
          active-color="primary"
          indicator-color="primary"
          class="text-slate-600 text-weight-bold"
        >
          <q-tab name="pos" icon="point_of_sale" label="POS & Cashier" />
          <q-tab name="gcash" icon="smartphone" label="GCash & Custom" />
          <q-tab name="credit" icon="account_balance_wallet" label="Credit & Utang" />
          <q-tab name="inventory" icon="inventory_2" label="Inventory & Sacks" />
          <q-tab name="tablet" icon="tablet_android" label="Offline Tablet Tips" />
        </q-tabs>
      </q-card-section>

      <!-- 3. Tab Panels Content -->
      <q-card-section class="col q-pa-md scroll-y bg-slate-50">
        <q-tab-panels v-model="activeTab" animated class="bg-transparent">
          
          <!-- TAB 1: POS & CASHIER -->
          <q-tab-panel name="pos" class="q-pa-none q-gutter-y-md">
            <!-- Selling by Sack vs Kilo -->
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="swap_horiz" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">1. Selling by Sack vs Retail Kilo</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Nichole Agrivet feeds are linked in a unified auto-converting pool. You can sell either a whole sack or loose retail kilos from the same batch.
              </p>
              <div class="row q-col-gutter-sm text-caption">
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-slate-50 rounded-borders border-slate">
                    <strong class="text-slate-900">📦 By Sack:</strong> Tap product card → select <strong>"By Sack"</strong> (e.g. ₱1,680.00). Deducts 50 kilos (or bag ratio) from warehouse stock.
                  </div>
                </div>
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-slate-50 rounded-borders border-slate">
                    <strong class="text-slate-900">⚖️ By Kilo:</strong> Tap product card → select <strong>"By Kilo"</strong> (e.g. ₱35.00/kg). Enter exact weight or tap <code>+1</code>, <code>+2</code>, <code>+5</code>, <code>+10</code>.
                  </div>
                </div>
              </div>
            </div>

            <!-- Payment Methods -->
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="payments" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">2. Processing Payments</span>
              </div>
              <div class="q-gutter-y-xs text-caption text-slate-700">
                <div class="row items-start">
                  <span class="badge-tag-amber q-mr-sm text-weight-bold" style="min-width: 60px; text-align: center">CASH</span>
                  <span>Tap <strong>Cash</strong>. Use the quick bill presets (₱100, ₱500, ₱1,000, ₱2,000) or exact change. Automatically computes change for the customer.</span>
                </div>
                <div class="row items-start q-mt-xs">
                  <span class="badge-tag-blue q-mr-sm text-weight-bold" style="min-width: 60px; text-align: center">GCASH</span>
                  <span>Tap <strong>GCash</strong> for direct e-wallet payment of merchandise. Zero cash change needed.</span>
                </div>
                <div class="row items-start q-mt-xs">
                  <span class="badge-tag-purple q-mr-sm text-weight-bold" style="min-width: 60px; text-align: center">CREDIT</span>
                  <span>Tap <strong>Credit</strong> for customer utang. Select or add a registered customer ledger. Walk-in customers cannot borrow on credit.</span>
                </div>
              </div>
            </div>

            <!-- Receipt Thermal Printing -->
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="print" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">3. Thermal Receipts (58mm / 80mm)</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-none">
                After checkout, the Official Receipt slip pops up. Toggle between <strong>58mm Handheld Thermal</strong> or <strong>80mm Counter Desktop</strong> paper sizes. Prints clean itemized descriptions with no browser margins or URL headers.
              </p>
            </div>
          </q-tab-panel>

          <!-- TAB 2: GCASH & CUSTOM SERVICES -->
          <q-tab-panel name="gcash" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="smartphone" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">1. GCash Cash In & Cash Out Workflow</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                To process GCash transactions, tap the <strong>GCash (Cash In / Cash Out)</strong> card in the catalog:
              </p>
              <div class="row q-col-gutter-sm text-caption">
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-blue-50 text-blue-9 rounded-borders border-slate">
                    <strong>📥 Cash In:</strong> Customer gives physical cash to store. Cashier sends GCash transfer to customer phone + adds store charge/patong.
                  </div>
                </div>
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-teal-50 text-teal-9 rounded-borders border-slate">
                    <strong>📤 Cash Out:</strong> Customer transfers GCash to store phone/QR. Cashier dispenses cash to customer + charges store fee.
                  </div>
                </div>
              </div>

              <div class="q-mt-md q-pa-sm bg-slate-50 border-slate rounded-borders text-caption">
                <div class="text-weight-bold text-slate-900 q-mb-xs">Formula for Sales Calculation:</div>
                <div class="text-primary text-weight-bold font-tabular" style="font-size: 0.95rem">
                  Total Line Sale = Principal Amount + Charge / Patong
                </div>
                <div class="text-slate-500 q-mt-xs">
                  Example: ₱1,000 Cash In + ₱20 Patong = <strong>₱1,020.00 Total Sale</strong> added to order.
                </div>
              </div>
            </div>

            <!-- Other / Custom Items -->
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="add_circle" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">2. Other & Custom Miscellaneous Items</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Tap <strong>Other / Custom Items</strong> card to quickly add non-inventory merchandise or service charges:
              </p>
              <div class="row q-gutter-xs q-mb-sm">
                <span v-for="item in ['Empty Sacks', 'Egg Trays', 'Delivery / Transport', 'Repair / Milling Fee', 'Miscellaneous']" :key="item" class="badge-tag-amber text-caption">
                  {{ item }}
                </span>
              </div>
              <div class="text-caption text-slate-500">
                💡 <em>Note:</em> Service and custom items do not deduct physical feed or sack stock from your warehouse.
              </div>
            </div>
          </q-tab-panel>

          <!-- TAB 3: CREDIT & UTANG TRACKER -->
          <q-tab-panel name="credit" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="contacts" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">1. Adding & Managing Farm Customers</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Register recurring farmers and customers to track their purchases and debt history:
              </p>
              <ul class="text-caption text-slate-700 q-pl-md q-my-none">
                <li>From the POS screen, tap <strong>[Switch]</strong> on the customer card to search or add a customer.</li>
                <li>From the <strong>Credit Tracker</strong> page, browse customer profiles, contact numbers, and total balance.</li>
              </ul>
            </div>

            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="price_check" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">2. Collecting Debt Payments</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                When a customer arrives to pay their outstanding utang:
              </p>
              <ol class="text-caption text-slate-700 q-pl-md q-my-none">
                <li>Go to <strong>Credit Tracker</strong>.</li>
                <li>Tap the customer's card to view their ledger and past purchase slips.</li>
                <li>Tap <strong>"Pay Balance"</strong>, enter the payment amount (partial or full), and confirm.</li>
                <li>The balance decreases automatically, and the cash is added to today's shift cash collection.</li>
              </ol>
            </div>
          </q-tab-panel>

          <!-- TAB 4: INVENTORY & SACKS -->
          <q-tab-panel name="inventory" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="rule" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">1. Understanding Stock Badges</span>
              </div>
              <div class="q-gutter-y-xs text-caption text-slate-700">
                <div class="row items-center">
                  <span class="badge-tag-amber q-mr-sm text-weight-bold" style="min-width: 90px; text-align: center">By Sack</span>
                  <span>Full unopened sacks in stock. (e.g. 83 sacks & 17 kilos).</span>
                </div>
                <div class="row items-center q-mt-xs">
                  <span class="badge-tag-blue q-mr-sm text-weight-bold" style="min-width: 90px; text-align: center">Loose Kilos</span>
                  <span>Loose/opened sack kilos available for retail weighing.</span>
                </div>
                <div class="row items-center q-mt-xs">
                  <span class="badge-tag-red q-mr-sm text-weight-bold" style="min-width: 90px; text-align: center">Low Stock</span>
                  <span>Urgent alert! Stock has fallen below minimum alert threshold (e.g. 5 sacks left).</span>
                </div>
                <div class="row items-center q-mt-xs">
                  <span class="badge-tag-out-of-stock q-mr-sm text-weight-bold" style="min-width: 90px; text-align: center">Out of Stock</span>
                  <span>Stock is depleted (0 left). Automatically prevented from POS checkout.</span>
                </div>
              </div>
            </div>

            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="unarchive" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">2. Manual Sack-to-Kilo Conversion</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-none">
                When you physically slice open a fresh sack in the store, go to <strong>Inventory</strong> → tap <strong>"Convert to Kilos"</strong> on that product. Enter 1 sack and it converts into 50 loose kilos for retail weighing.
              </p>
            </div>
          </q-tab-panel>

          <!-- TAB 5: OFFLINE TABLET TIPS -->
          <q-tab-panel name="tablet" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="wifi_off" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">1. Offline Operation on Infinix XPAD</span>
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                The Nichole Agrivet app is built to run 100% offline. No internet connection is required to make sales, calculate change, or print receipts.
              </p>
              <div class="q-pa-sm bg-emerald-50 text-emerald-9 rounded-borders border-slate text-caption">
                ✅ Transactions are stored locally on the tablet and never lost during network drops or power outages.
              </div>
            </div>

            <div class="q-pa-md bg-white border-slate rounded-borders">
              <div class="row items-center q-mb-sm">
                <q-icon name="battery_charging_full" size="22px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle2 text-weight-bolder text-slate-900">2. Tablet Battery & Care Tips</span>
              </div>
              <ul class="text-caption text-slate-700 q-pl-md q-my-none">
                <li><strong>Screen Brightness:</strong> Set brightness to ~60% for all-day battery life (10+ hours of continuous cashiering on the Infinix XPAD).</li>
                <li><strong>Collapsible Sidebar:</strong> Use the ☰ hamburger button to hide the sidebar while cashiering for bigger touch targets.</li>
                <li><strong>Bluetooth Printer:</strong> Ensure your 58mm/80mm thermal printer is paired via Bluetooth or USB OTG cable.</li>
              </ul>
            </div>
          </q-tab-panel>

        </q-tab-panels>
      </q-card-section>

      <!-- 4. Footer -->
      <q-card-actions align="between" class="q-px-md q-py-sm bg-white border-top-subtle">
        <span class="text-caption text-slate-400 font-medium">Nichole Agrivet POS v1.0 • System Ready</span>
        <q-btn unelevated color="primary" label="Got It, Thanks!" v-close-popup class="text-weight-bold q-px-lg" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['update:modelValue'])

const activeTab = ref('pos')
</script>

<style scoped>
.rounded-borders-lg {
  border-radius: 18px !important;
}
.border-bottom-subtle {
  border-bottom: 1px solid #f1f5f9;
}
.border-top-subtle {
  border-top: 1px solid #f1f5f9;
}
.border-slate {
  border: 1px solid #e2e8f0;
}
</style>
