<template>
  <q-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)">
    <q-card
      style="width: 820px; max-width: 96vw; max-height: 92vh"
      class="column no-wrap rounded-borders-xl shadow-24"
    >
      <!-- 1. Header with Mascot & Title -->
      <q-card-section
        class="row items-center justify-between bg-slate-900 text-white q-py-md q-px-lg"
      >
        <div class="row items-center q-gutter-x-md">
          <q-avatar size="44px" class="bg-white q-pa-xs shadow-1">
            <img :src="logoUrl" alt="Mascot" style="object-fit: contain" />
          </q-avatar>
          <div>
            <div class="text-h6 text-weight-bolder leading-tight">
              Nichole Agrivet • Complete User & Cashier Guide
            </div>
            <div class="text-caption text-slate-400 font-medium" style="font-size: 0.78rem">
              Step-by-step instructions, offline tablet tips, and store workflows
            </div>
          </div>
        </div>
        <q-btn flat round dense icon="close" color="white" v-close-popup />
      </q-card-section>

      <!-- 2. Navigation Tabs (Scrollable & Responsive) -->
      <q-card-section class="q-pa-none bg-white border-bottom-subtle">
        <q-tabs
          v-model="activeTab"
          dense
          no-caps
          align="left"
          active-color="primary"
          indicator-color="primary"
          class="text-slate-600 text-weight-bolder guide-tabs"
          outside-arrows
          mobile-arrows
        >
          <q-tab name="pos" icon="point_of_sale" label="1. POS & Selling" />
          <q-tab name="budget" icon="scale" label="2. By Kilo & Budget" />
          <q-tab name="gcash" icon="smartphone" label="3. GCash & Services" />
          <q-tab name="credit" icon="account_balance_wallet" label="4. Credit & Utang" />
          <q-tab name="inventory" icon="inventory_2" label="5. Inventory & Sacks" />
          <q-tab name="reports" icon="bar_chart" label="6. Reports & Z-Reading" />
          <q-tab name="offline" icon="tablet_android" label="7. Offline & Backups" />
        </q-tabs>
      </q-card-section>

      <!-- 3. Tab Panels Content -->
      <q-card-section class="col q-pa-lg scroll-y bg-slate-50">
        <q-tab-panels v-model="activeTab" animated class="bg-transparent">
          
          <!-- TAB 1: POS & CASHIER CHECKOUT -->
          <q-tab-panel name="pos" class="q-pa-none q-gutter-y-md">
            <!-- Basic POS Flow -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="shopping_cart" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >1. Basic Cashier Checkout Flow</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                The POS screen is optimized for high-speed tablet cashiering:
              </p>
              <div class="row q-col-gutter-sm text-caption">
                <div class="col-12 col-sm-4">
                  <div class="q-pa-sm bg-slate-50 rounded-borders border-slate full-height">
                    <strong class="text-slate-900 block q-mb-xs">Step 1: Pick Products</strong>
                    Tap product cards in the catalog, or use the top search bar (<code>Search product name...</code>) to instantly filter feeds, medicines, or services.
                  </div>
                </div>
                <div class="col-12 col-sm-4">
                  <div class="q-pa-sm bg-slate-50 rounded-borders border-slate full-height">
                    <strong class="text-slate-900 block q-mb-xs">Step 2: Choose Payment</strong>
                    Tap <strong>Cash</strong>, <strong>GCash</strong>, or <strong>Credit</strong> at the bottom of your order list.
                  </div>
                </div>
                <div class="col-12 col-sm-4">
                  <div class="q-pa-sm bg-slate-50 rounded-borders border-slate full-height">
                    <strong class="text-slate-900 block q-mb-xs">Step 3: Tender & Receipt</strong>
                    Use the side-by-side Numpad or quick bills (₱100, ₱500, ₱1,000) to enter cash. Change due is computed automatically.
                  </div>
                </div>
              </div>
            </div>

            <!-- Payment Methods Explained -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="payments" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >2. The 3 Payment Methods</span
                >
              </div>
              <div class="q-gutter-y-sm text-caption text-slate-700">
                <div class="row items-start q-pa-sm bg-amber-50 rounded-borders border-slate">
                  <span class="badge-tag-amber q-mr-sm text-weight-bold" style="min-width: 65px; text-align: center">CASH</span>
                  <span><strong>Physical Cash:</strong> Numpad opens with quick bills. Exact Change button fills total due in 1 tap. Shows change due immediately.</span>
                </div>
                <div class="row items-start q-pa-sm bg-blue-50 rounded-borders border-slate">
                  <span class="badge-tag-blue q-mr-sm text-weight-bold" style="min-width: 65px; text-align: center">GCASH</span>
                  <span><strong>E-Wallet Transfer:</strong> Customer pays via GCash QR/number. Enters reference number (optional). Exact total billed with ₱0 change.</span>
                </div>
                <div class="row items-start q-pa-sm bg-purple-50 rounded-borders border-slate">
                  <span class="badge-tag-purple q-mr-sm text-weight-bold" style="min-width: 65px; text-align: center">CREDIT</span>
                  <span><strong>Utang Account:</strong> For trusted farmers/customers. Bill is charged directly to their customer ledger and recorded in the Credit Tracker.</span>
                </div>
              </div>
            </div>

            <!-- Thermal Receipts -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="receipt_long" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >3. Thermal Receipts (Side-by-Side Slip)</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-none">
                When payment completes, the receipt modal shows the slip on the left and options on the right:
                Toggle between <strong>80mm (Standard Desktop Thermal)</strong> and <strong>58mm (Handheld Mobile Thermal)</strong>. 
                Your paper preference is permanently remembered for all future sales!
              </p>
            </div>
          </q-tab-panel>

          <!-- TAB 2: BY KILO & PESO BUDGET -->
          <q-tab-panel name="budget" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="scale" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >1. Default Retail: Selling By Kilo</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Whenever you tap any feed or grain product, the item modal <strong>defaults automatically to By Kilo</strong>.
              </p>
              <div class="row q-gutter-xs q-mb-sm">
                <span class="badge-tag-blue text-caption">1 Tap Presets: +1 kg</span>
                <span class="badge-tag-blue text-caption">+2 kg</span>
                <span class="badge-tag-blue text-caption">+5 kg</span>
                <span class="badge-tag-blue text-caption">+10 kg</span>
              </div>
              <div class="text-caption text-slate-500">
                You can also type exact fractional quantities like <code>0.75</code> kg or <code>2.5</code> kg on the touch numpad.
              </div>
            </div>

            <!-- Selling by Peso Budget (New Feature) -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="calculate" size="24px" color="emerald-8" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >2. Selling by Peso Budget (e.g. "Pabili ₱50")</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Customers frequently ask for feeds by fixed peso budget rather than kilos. Here is how to handle it in 2 seconds:
              </p>
              <ol class="text-caption text-slate-700 q-pl-md q-my-none q-gutter-y-xs">
                <li>Tap the feed product card in the catalog.</li>
                <li>Tap the <strong>"₱ By Peso Budget"</strong> toggle button.</li>
                <li>Enter the customer's budget (e.g. <code>₱50</code>, <code>₱100</code>, <code>₱150</code>).</li>
                <li>
                  The green <strong>⚖️ WEIGH ON SCALE</strong> box instantly calculates the exact weight to scoop!
                  <div class="q-mt-xs q-pa-xs bg-emerald-50 text-emerald-9 rounded-borders border-slate font-tabular">
                    <em>Example:</em> ₱50 budget at ₱38.00/kg → <strong>1.32 Kilos</strong> on your scale!
                  </div>
                </li>
                <li>Tap <strong>Add to Order</strong> — the line item correctly records 1.32 kg at ₱50.00 subtotal!</li>
              </ol>
            </div>

            <!-- Selling By Sack -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="inventory" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >3. Selling Whole Sacks</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-none">
                When a customer buys an unopened bag, tap <strong>"📦 By Sack"</strong>. 
                Deducts 1 full sack (and 50 kg from the warehouse pool) at the wholesale sack price (e.g. ₱1,650.00/sack).
              </p>
            </div>
          </q-tab-panel>

          <!-- TAB 3: GCASH & CUSTOM SERVICES -->
          <q-tab-panel name="gcash" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="smartphone" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >1. GCash Cash In & Cash Out Workflow</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Tap the blue <strong>GCash (Cash In / Cash Out)</strong> card in the catalog:
              </p>
              <div class="row q-col-gutter-sm text-caption">
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-blue-50 text-blue-9 rounded-borders border-slate full-height">
                    <strong class="block q-mb-xs">📥 Cash In:</strong>
                    Customer gives cash to store. Store sends GCash to customer + charges store fee (patong).
                  </div>
                </div>
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-teal-50 text-teal-9 rounded-borders border-slate full-height">
                    <strong class="block q-mb-xs">📤 Cash Out:</strong>
                    Customer transfers GCash to store phone/QR. Store hands cash to customer + charges store fee.
                  </div>
                </div>
              </div>

              <div class="q-mt-md q-pa-sm bg-slate-50 border-slate rounded-borders text-caption">
                <div class="text-weight-bold text-slate-900">
                  Sales Accounting:
                </div>
                <div class="text-slate-600 q-mt-xs">
                  The line total equals <strong>Principal + Fee</strong>. GCash transactions are recorded cleanly without deducting warehouse feeds.
                </div>
              </div>
            </div>

            <!-- Other Custom Items -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="add_shopping_cart" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >2. Other / Non-Catalog Items & Services</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Tap <strong>Other / Custom Items</strong> for miscellaneous items or store services:
              </p>
              <div class="row q-gutter-xs q-mb-sm">
                <span class="badge-tag-amber text-caption">Empty Sacks</span>
                <span class="badge-tag-amber text-caption">Egg Trays</span>
                <span class="badge-tag-amber text-caption">Delivery / Hauling</span>
                <span class="badge-tag-amber text-caption">Corn Milling Fee</span>
                <span class="badge-tag-amber text-caption">Custom Amount</span>
              </div>
            </div>
          </q-tab-panel>

          <!-- TAB 4: CREDIT & UTANG TRACKER -->
          <q-tab-panel name="credit" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="badge" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >1. Registering Customer Ledgers</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                To issue credit (utang), a customer must have a registered ledger:
              </p>
              <ul class="text-caption text-slate-700 q-pl-md q-my-none q-gutter-y-xs">
                <li>From the <strong>Credit Tracker</strong> page: Tap the green <strong>"+ Add Customer"</strong> button. Enter their name, phone number, and address notes.</li>
                <li>From the <strong>POS screen</strong>: Tap <strong>[Switch]</strong> on the customer bar → tap <strong>"+ New Customer"</strong> without leaving your current sale.</li>
              </ul>
            </div>

            <!-- Collecting Bayad -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="price_check" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >2. Recording "Bayad" (Debt Payments)</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                When a farmer arrives to pay down their credit balance:
              </p>
              <ol class="text-caption text-slate-700 q-pl-md q-my-none q-gutter-y-xs">
                <li>Open <strong>Credit Tracker</strong> (or click Credit Tracker in the menu).</li>
                <li>Search or tap the customer's ledger from the left list.</li>
                <li>Tap the green <strong>"Bayad"</strong> button.</li>
                <li>
                  Use the quick amount buttons (<code>[Full Balance]</code>, <code>[₱100]</code>, <code>[₱500]</code>, <code>[₱1,000]</code>) or type the exact partial payment.
                </li>
                <li>
                  Tap <strong>Post Payment Receipt</strong>. 
                  The balance reduces instantly, and the payment is added to your daily cash collection!
                </li>
              </ol>
            </div>
          </q-tab-panel>

          <!-- TAB 5: INVENTORY & SACKS -->
          <q-tab-panel name="inventory" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="sync_alt" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >1. Unified Sack & Kilo Inventory Pool</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Nichole Agrivet uses a unified inventory formula: 
                <strong>1 Sack = 50 Kilos</strong> (or custom bag weight). 
                Whether you sell 1 sack or 2.5 kilos, stock automatically deducts from the same pool.
              </p>
              <div class="q-pa-sm bg-slate-50 border-slate rounded-borders text-caption text-slate-700">
                <strong>Warehouse Conversion:</strong> When physically slicing open a new sack in the store, go to <strong>Inventory</strong> → tap <strong>"Convert to Kilos"</strong> to move 1 sack into 50 loose retail kilos.
              </div>
            </div>

            <!-- Adding & Editing Products -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="add_box" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >2. Adding Products & Setting Low Stock Alerts</span
                >
              </div>
              <ul class="text-caption text-slate-700 q-pl-md q-my-none q-gutter-y-xs">
                <li>Tap <strong>"+ Add Product"</strong> in the top header of the Inventory page.</li>
                <li>Choose a preset (Feeds & Grains, Drinks, Box/Piece, or Custom).</li>
                <li>Set both <strong>Sack Price</strong> and <strong>Kilo Price</strong>.</li>
                <li>Set the <strong>Low Stock Threshold</strong> (e.g. 5 sacks) so the system warns you before running out!</li>
              </ul>
            </div>
          </q-tab-panel>

          <!-- TAB 6: REPORTS & Z-READING -->
          <q-tab-panel name="reports" class="q-pa-none q-gutter-y-md">
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="receipt" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >1. Daily Shift Summary (Z-Reading)</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                At the top left of the POS header, tap the <strong>"TODAY'S SHIFT"</strong> pill button to open the shift reading:
              </p>
              <div class="row q-col-gutter-sm text-caption">
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-slate-50 rounded-borders border-slate">
                    <strong>💵 Cash in Drawer:</strong> Total physical cash sales + debt payments collected today.
                  </div>
                </div>
                <div class="col-12 col-sm-6">
                  <div class="q-pa-sm bg-slate-50 rounded-borders border-slate">
                    <strong>📱 GCash Total:</strong> Electronic sales recorded through GCash transfers.
                  </div>
                </div>
              </div>
              <div class="text-caption text-slate-500 q-mt-sm">
                Tap <strong>"Print Shift Z-Reading"</strong> to print a compact closing slip on thermal paper for store records!
              </div>
            </div>

            <!-- Sales Tracker Page -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="analytics" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >2. Reports & Analytics Page</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-none">
                Visit the <strong>Reports & Analytics</strong> page to filter sales by date (Today, Yesterday, Last 7 Days, Month). 
                Export data to Excel/CSV or inspect voided and completed transactions.
              </p>
            </div>
          </q-tab-panel>

          <!-- TAB 7: OFFLINE & TABLET TIPS -->
          <q-tab-panel name="offline" class="q-pa-none q-gutter-y-md">
            <!-- 100% Offline Standalone -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="offline_bolt" size="24px" color="positive" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >1. 100% Offline Standalone Operation</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Nichole Agrivet is engineered to run completely standalone on your Android tablet or phone:
              </p>
              <div class="q-pa-sm bg-emerald-50 text-emerald-9 rounded-borders border-slate text-caption">
                ✅ <strong>Zero PC Required:</strong> All product listings, inventory changes, customer utang, and transactions are stored directly in the tablet's fast internal storage.
                <br />
                ✅ <strong>Zero Internet Needed:</strong> The store can operate during power outages, mobile signal drops, or remote farm locations.
              </div>
            </div>

            <!-- Database Backup & Safety -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="cloud_download" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >2. Database Backup & Recovery (1-Tap Export)</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-sm">
                Keep your store records safe! We recommend doing a backup once a week:
              </p>
              <ol class="text-caption text-slate-700 q-pl-md q-my-none q-gutter-y-xs">
                <li>Tap the <strong>Cloud Download</strong> icon at the top right (or in the cashier dropdown menu).</li>
                <li>Tap <strong>"Export & Download Store Backup"</strong>.</li>
                <li>A clean `.json` file is saved to your tablet's Downloads folder. You can copy it to a flash drive or Google Drive for safekeeping.</li>
              </ol>
            </div>

            <!-- Changing Cashier Name -->
            <div class="q-pa-md bg-white border-slate rounded-borders-md shadow-sm">
              <div class="row items-center q-mb-sm">
                <q-icon name="badge" size="24px" color="primary" class="q-mr-xs" />
                <span class="text-subtitle1 text-weight-bolder text-slate-900"
                  >3. Changing Cashier Name</span
                >
              </div>
              <p class="text-caption text-slate-600 q-mb-none">
                Tap your name pill at the top right → select <strong>"Change Cashier Name"</strong>. 
                Enter your name (e.g. <code>J-ar</code>). The app permanently remembers it across logins, logouts, and restarts!
              </p>
            </div>
          </q-tab-panel>

        </q-tab-panels>
      </q-card-section>

      <!-- 4. Footer -->
      <q-card-actions align="between" class="q-px-lg q-py-sm bg-white border-top-subtle">
        <div class="row items-center text-caption text-slate-500 font-medium">
          <q-icon name="verified" color="primary" size="16px" class="q-mr-xs" />
          <span>Nichole Agrivet POS v1.0 • Offline Ready Terminal</span>
        </div>
        <q-btn
          unelevated
          class="btn-agrivet-green text-weight-bold q-px-xl"
          label="Got It, Close Guide"
          v-close-popup
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref } from 'vue'
import logoUrl from 'src/images/Nichole Agrivet.png'

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
.rounded-borders-xl {
  border-radius: 20px !important;
  overflow: hidden;
}
.rounded-borders-md {
  border-radius: 12px;
}
.border-bottom-subtle {
  border-bottom: 1.5px solid #e2e8f0;
}
.border-top-subtle {
  border-top: 1.5px solid #e2e8f0;
}
.border-slate {
  border: 1.5px solid #cbd5e1;
}

.guide-tabs {
  background-color: #ffffff;
}

.btn-agrivet-green {
  background-color: #0d6832 !important;
  color: #ffffff !important;
  border-radius: 10px;
  height: 40px;
  &:hover {
    background-color: #0a5227 !important;
  }
}

.badge-tag-amber {
  background: #fef3c7;
  color: #92400e;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 700;
}

.badge-tag-blue {
  background: #dbeafe;
  color: #1e40af;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 700;
}

.badge-tag-purple {
  background: #f3e8ff;
  color: #6b21a8;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 700;
}
</style>
