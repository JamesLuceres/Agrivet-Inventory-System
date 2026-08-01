<template>
  <q-page class="q-pa-lg">
    <!-- Header -->
    <div class="row items-center q-mb-lg">
      <q-btn flat round dense icon="arrow_back" size="lg" color="green-10" class="q-mr-md" @click="$router.push('/')">
        <q-tooltip>Back to Dashboard</q-tooltip>
      </q-btn>
      <q-icon name="shopping_cart" size="lg" color="green-10" class="q-mr-sm" />
      <h1 class="text-h4 text-weight-bold text-green-10 q-my-none">Cashier</h1>
    </div>

    <div class="row q-col-gutter-lg">
      <!-- 1. LEFT COLUMN: PRODUCT SEARCH & CATALOG -->
      <div class="col-12 col-md-7 col-lg-8">
        <q-card flat bordered class="bg-white shadow-1 fit-height">
          <q-card-section class="q-pb-none">
            <div class="text-h6 text-weight-bold text-indigo-10 q-mb-md">Product Catalog</div>
            <div class="row q-col-gutter-sm q-mb-md">
              <!-- Search Bar -->
              <div class="col-12 col-sm-8">
                <q-input
                  v-model="searchQuery"
                  placeholder="Search products by name..."
                  outlined
                  dense
                  clearable
                >
                  <template v-slot:prepend>
                    <q-icon name="search" />
                  </template>
                </q-input>
              </div>
              <!-- Category Filter -->
              <div class="col-12 col-sm-4">
                <q-select
                  v-model="selectedCategory"
                  :options="categoryOptions"
                  label="Category"
                  outlined
                  dense
                  emit-value
                  map-options
                />
              </div>
            </div>
          </q-card-section>

          <q-separator />

          <!-- Products Grid -->
          <q-card-section class="q-pa-md scroll-container">
            <div v-if="filteredProducts.length === 0" class="text-center text-grey-6 q-py-xl">
              <q-icon name="inventory_2" size="xl" class="q-mb-sm" />
              <div>No products found matching the criteria.</div>
            </div>
            
            <div class="row q-col-gutter-md">
              <div
                v-for="product in filteredProducts"
                :key="product.id"
                class="col-12 col-sm-6 col-md-6 col-lg-4"
              >
                <q-card
                  flat
                  bordered
                  class="product-item-card hover-grow cursor-pointer q-pa-sm"
                  @click="openAddProductModal(product)"
                >
                  <q-card-section class="q-pa-sm">
                    <div class="row items-center justify-between no-wrap q-mb-xs">
                      <div class="text-subtitle1 text-weight-bold text-slate-900 ellipsis">{{ product.name }}</div>
                      <q-icon name="add_shopping_cart" color="emerald-7" size="20px" />
                    </div>

                    <q-badge color="emerald-1" text-color="emerald-9" class="q-mb-xs text-weight-bold">
                      {{ product.category_name }}
                    </q-badge>

                    <div class="row justify-between text-caption q-mt-xs text-slate-500">
                      <div v-if="product.unit_bulk_name && product.price_per_sack">
                        {{ product.unit_bulk_name }} Stock: 
                        <span :class="parseFloat(product.stock_sacks) < product.low_stock_threshold ? 'text-rose-6 text-weight-bold' : 'text-slate-900 text-weight-medium'">
                          {{ parseFloat(product.stock_sacks) }}
                        </span>
                      </div>
                      <div>
                        {{ product.unit_retail_name || 'Stock' }}: 
                        <span :class="parseFloat(product.stock_kilos) < product.low_stock_threshold ? 'text-rose-6 text-weight-bold' : 'text-slate-900 text-weight-medium'">
                          {{ parseFloat(product.stock_kilos) }}
                        </span>
                      </div>
                    </div>

                    <div class="q-mt-sm row q-gutter-xs text-caption">
                      <div v-if="product.price_per_kilo" class="bg-slate-100 q-px-xs q-py-xs rounded-borders border-slate">
                        {{ product.unit_retail_name || 'Item' }}: <span class="text-weight-bold text-emerald-7 num-tabular">₱{{ parseFloat(product.price_per_kilo).toFixed(2) }}</span>
                      </div>
                      <div v-if="product.price_per_sack && product.unit_bulk_name" class="bg-slate-100 q-px-xs q-py-xs rounded-borders border-slate">
                        {{ product.unit_bulk_name }}: <span class="text-weight-bold text-indigo-7 num-tabular">₱{{ parseFloat(product.price_per_sack).toFixed(2) }}</span>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </q-card-section>
        </q-card>
      </div>

      <!-- 2. RIGHT COLUMN: ACTIVE SHOPPING CART & CHECKOUT -->
      <div class="col-12 col-md-5 col-lg-4">
        <q-card flat bordered class="bg-white shadow-1 fit-height column justify-between">
          <q-card-section class="q-pa-md">
            <div class="row items-center justify-between q-mb-md">
              <div class="text-h6 text-weight-bold text-slate-900">Cart Items</div>
              <q-btn flat dense no-caps color="rose-6" icon="delete_sweep" label="Clear" @click="clearCart" :disable="cart.length === 0" />
            </div>

            <!-- Empty Cart Placeholder -->
            <div v-if="cart.length === 0" class="text-center text-slate-400 q-py-xl">
              <q-icon name="remove_shopping_cart" size="48px" class="q-mb-xs" />
              <div>Cart is empty. Click a product to add items.</div>
            </div>

            <!-- Cart Items List -->
            <q-list separator v-else class="scroll-container">
              <q-item v-for="(item, index) in cart" :key="index" class="q-px-none q-py-sm">
                <q-item-section>
                  <q-item-label class="text-weight-bold text-slate-900">{{ item.product.name }}</q-item-label>
                  <q-item-label caption>
                    <q-badge :color="item.unitType === 'SACK' ? 'indigo-1' : 'emerald-1'" :text-color="item.unitType === 'SACK' ? 'indigo-9' : 'emerald-9'" class="text-weight-bold q-mr-xs">
                      {{ item.unitType === 'SACK' ? (item.product.unit_bulk_name || 'Bulk') : (item.product.unit_retail_name || 'Retail') }}
                    </q-badge>
                    ₱{{ item.price.toFixed(2) }} / {{ item.unitType === 'SACK' ? (item.product.unit_bulk_name || 'unit') : (item.product.unit_retail_name || 'unit') }}
                  </q-item-label>
                </q-item-section>

                <q-item-section side class="row items-center no-wrap">
                  <q-input
                    v-model.number="item.quantity"
                    type="number"
                    step="0.05"
                    min="0.01"
                    dense
                    outlined
                    class="quantity-input num-tabular q-mr-xs text-caption"
                    @update:model-value="validateQuantity(item)"
                  />
                  <q-btn flat round dense color="rose-6" icon="remove_circle_outline" @click="removeFromCart(index)" />
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>

          <!-- Checkout Calculation Footer -->
          <q-card-section class="q-pa-md bg-slate-50 border-top-slate">
            <div class="row justify-between items-center q-mb-md">
              <div class="text-subtitle1 text-slate-700">Grand Total:</div>
              <div class="text-h4 text-weight-bold text-emerald-7 num-tabular">
                ₱{{ grandTotal.toFixed(2) }}
              </div>
            </div>

            <!-- Payment Type Switch -->
            <div class="q-mb-md">
              <div class="text-caption text-weight-bold text-slate-700 text-uppercase q-mb-xs">Payment Method:</div>
              <q-btn-toggle
                v-model="paymentMethod"
                toggle-color="emerald-7"
                flat
                bordered
                spread
                :options="[
                  { label: '💵 CASH', value: 'CASH' },
                  { label: '📱 GCASH', value: 'GCASH' },
                  { label: '📝 CREDIT (Utang)', value: 'CREDIT' }
                ]"
              />
            </div>

            <!-- CASH METHOD: Cash Tendered, Quick Bills & Interactive Numpad -->
            <div v-if="paymentMethod === 'CASH'" class="q-mb-md">
              <q-input
                v-model.number="cashTendered"
                type="number"
                step="1"
                label="Cash Tendered"
                outlined
                dense
                prefix="₱"
                class="num-tabular q-mb-xs"
              />

              <!-- Quick Bill Denominations Row -->
              <div class="row q-gutter-xs q-mb-xs">
                <q-btn
                  v-for="bill in [50, 100, 200, 500, 1000]"
                  :key="bill"
                  outline
                  dense
                  no-caps
                  color="slate-7"
                  class="col text-caption text-weight-medium"
                  @click="selectQuickBill(bill)"
                >
                  ₱{{ bill }}
                </q-btn>
              </div>

              <!-- Touch Keypad / Numpad Grid -->
              <div class="numpad-container bg-slate-100 q-pa-xs rounded-borders border-slate">
                <div class="row q-col-gutter-xs q-mb-xs">
                  <div class="col-4" v-for="num in ['7', '8', '9']" :key="num">
                    <q-btn color="white" text-color="slate-900" class="full-width text-weight-bold text-subtitle1" unelevated @click="handleNumpadKey(num)">
                      {{ num }}
                    </q-btn>
                  </div>
                </div>
                <div class="row q-col-gutter-xs q-mb-xs">
                  <div class="col-4" v-for="num in ['4', '5', '6']" :key="num">
                    <q-btn color="white" text-color="slate-900" class="full-width text-weight-bold text-subtitle1" unelevated @click="handleNumpadKey(num)">
                      {{ num }}
                    </q-btn>
                  </div>
                </div>
                <div class="row q-col-gutter-xs q-mb-xs">
                  <div class="col-4" v-for="num in ['1', '2', '3']" :key="num">
                    <q-btn color="white" text-color="slate-900" class="full-width text-weight-bold text-subtitle1" unelevated @click="handleNumpadKey(num)">
                      {{ num }}
                    </q-btn>
                  </div>
                </div>
                <div class="row q-col-gutter-xs">
                  <div class="col-4">
                    <q-btn color="white" text-color="slate-900" class="full-width text-weight-bold text-subtitle1" unelevated @click="handleNumpadKey('0')">
                      0
                    </q-btn>
                  </div>
                  <div class="col-4">
                    <q-btn color="amber-1" text-color="amber-10" class="full-width text-weight-bold" unelevated icon="backspace" @click="handleNumpadKey('BACKSPACE')">
                    </q-btn>
                  </div>
                  <div class="col-4">
                    <q-btn color="rose-1" text-color="rose-9" class="full-width text-weight-bold text-subtitle1" unelevated label="C" @click="handleNumpadKey('C')">
                    </q-btn>
                  </div>
                </div>
              </div>

              <!-- Change Given Banner -->
              <div class="row justify-between items-center text-subtitle2 q-mt-xs bg-slate-50 q-pa-sm rounded-borders border-slate" v-if="cashTendered !== null">
                <span class="text-slate-700">Change Given:</span>
                <span :class="cashTendered >= grandTotal ? 'text-emerald-7 text-weight-bold' : 'text-rose-6 text-weight-bold'" class="num-tabular text-h6">
                  ₱{{ (cashTendered - grandTotal).toFixed(2) }}
                </span>
              </div>
            </div>

            <!-- GCASH METHOD: Exact Digital Payment & Optional Ref Number -->
            <div v-else-if="paymentMethod === 'GCASH'" class="q-mb-md">
              <div class="bg-indigo-1 border-slate rounded-borders q-pa-md text-center q-mb-sm">
                <q-icon name="smartphone" color="indigo-7" size="32px" class="q-mb-xs" />
                <div class="text-subtitle1 text-weight-bold text-slate-900">GCash Payment</div>
                <div class="text-caption text-indigo-9 text-weight-bold q-mt-xs">
                  Exact Amount Transferred: ₱{{ grandTotal.toFixed(2) }}
                </div>
                <div class="text-caption text-slate-500">No change required. Recorded for GCash sales tracking.</div>
              </div>

              <q-input
                v-model="gcashRef"
                label="GCash Reference Number (Optional)"
                placeholder="e.g. 1002 9384 1120"
                outlined
                dense
                class="num-tabular"
              >
                <template v-slot:prepend>
                  <q-icon name="receipt" color="primary" />
                </template>
              </q-input>
            </div>

            <!-- CREDIT METHOD: Select Customer & Amount Paid -->
            <div v-else class="q-mb-md">
              <div class="row q-col-gutter-xs items-center q-mb-xs">
                <div class="col">
                  <q-select
                    v-model="selectedCustomer"
                    :options="customerOptions"
                    option-label="name"
                    label="Select Customer"
                    outlined
                    dense
                  />
                </div>
                <div class="col-auto">
                  <q-btn color="primary" icon="person_add" dense flat @click="openNewCustomerDialog">
                    <q-tooltip>Add New Customer</q-tooltip>
                  </q-btn>
                </div>
              </div>

              <q-input
                v-model.number="amountPaid"
                type="number"
                step="1"
                label="Initial Payment Paid Today (Optional)"
                outlined
                dense
                prefix="₱"
                class="num-tabular q-mt-xs"
              />

              <div class="row justify-between text-caption q-mt-xs" v-if="selectedCustomer">
                <span class="text-slate-600">Remaining Balance Added to Credit:</span>
                <span class="text-rose-6 text-weight-bold num-tabular">
                  ₱{{ (grandTotal - (amountPaid || 0)).toFixed(2) }}
                </span>
              </div>
            </div>

            <!-- Submit Transaction Action -->
            <q-btn
              color="emerald-7"
              icon="check_circle"
              label="Complete Transaction"
              size="lg"
              class="full-width text-weight-bold"
              :disable="!canCheckout"
              @click="submitTransaction"
            />
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- New Customer Dialog -->
    <q-dialog v-model="customerDialog.open">
      <q-card style="width: 400px; max-width: 90vw;">
        <q-card-section class="bg-indigo-10 text-white q-py-md">
          <div class="text-h6 text-weight-bold">Add New Customer</div>
        </q-card-section>

        <q-card-section class="q-py-md row q-col-gutter-sm">
          <div class="col-12">
            <q-input v-model="customerDialog.name" label="Customer Name" outlined dense />
          </div>
          <div class="col-12">
            <q-input v-model="customerDialog.contact" label="Contact Number" outlined dense />
          </div>
          <div class="col-12">
            <q-input v-model="customerDialog.notes" label="Notes" outlined dense type="textarea" rows="3" />
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn label="Save Customer" color="primary" @click="saveNewCustomer" :disable="!customerDialog.name" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Transaction Finished / Receipt Modal -->
    <q-dialog v-model="receiptDialog.open" persistent>
      <q-card style="width: 520px; max-width: 95vw;" class="receipt-dialog-card">
        <!-- Success Banner Header -->
        <q-card-section class="bg-emerald-7 text-white q-py-md text-center">
          <q-icon name="check_circle" size="48px" class="q-mb-xs" />
          <div class="text-h5 text-weight-bold tracking-tight">Transaction Finished</div>
          <div class="text-caption text-emerald-100">
            Receipt #{{ receiptDialog.tx.id }} • {{ formatDateTime(receiptDialog.tx.created_at) }}
          </div>
        </q-card-section>

        <!-- Printable Paper Receipt Body -->
        <q-card-section class="q-pa-lg printable-area">
          <div class="receipt-paper bg-slate-50 border-slate q-pa-md rounded-borders">
            <!-- Store Branding Header -->
            <div class="text-center q-mb-md">
              <q-avatar size="50px" class="bg-white shadow-1 q-mb-xs overflow-hidden" style="border: 1.5px solid #059669">
                <img :src="logoUrl" alt="Nichole Agrivet Logo" style="object-fit: cover; transform: scale(1.15);" />
              </q-avatar>
              <div class="text-h6 text-weight-bold text-slate-900 leading-tight">Nichole Agrivet</div>
              <div class="text-caption text-slate-500">Official Store Receipt</div>
            </div>

            <q-separator class="q-mb-md" />

            <!-- Receipt Meta Info -->
            <div class="row q-col-gutter-xs text-caption q-mb-md">
              <div class="col-6 text-slate-500">Receipt No:</div>
              <div class="col-6 text-weight-bold text-right text-slate-900">#{{ receiptDialog.tx.id }}</div>

              <div class="col-6 text-slate-500">Customer:</div>
              <div class="col-6 text-weight-bold text-right text-slate-900">{{ receiptDialog.tx.customer_name || 'Walk-in Guest' }}</div>

              <div class="col-6 text-slate-500">Payment Method:</div>
              <div class="col-6 text-weight-bold text-right text-uppercase" :class="receiptDialog.tx.transaction_type === 'CASH' ? 'text-emerald-7' : (receiptDialog.tx.transaction_type === 'GCASH' ? 'text-indigo-7' : 'text-amber-8')">
                {{ receiptDialog.tx.transaction_type }}
              </div>

              <template v-if="receiptDialog.tx.reference_number">
                <div class="col-6 text-slate-500">GCash Ref No:</div>
                <div class="col-6 text-weight-bold text-right text-indigo-9 num-tabular">
                  {{ receiptDialog.tx.reference_number }}
                </div>
              </template>
            </div>

            <!-- Items Purchased List -->
            <div class="text-caption text-weight-bold text-slate-700 text-uppercase q-mb-xs">Items Purchased</div>
            <q-list bordered separator class="rounded-borders bg-white q-mb-md">
              <q-item v-for="item in receiptDialog.tx.items" :key="item.id" class="q-py-xs">
                <q-item-section>
                  <q-item-label class="text-weight-bold text-body2 text-slate-900">{{ item.product_name }}</q-item-label>
                  <q-item-label caption class="text-slate-500">
                    {{ item.quantity }} {{ item.unit_type }}(s) @ ₱{{ parseFloat(item.unit_price).toFixed(2) }}
                  </q-item-label>
                </q-item-section>
                <q-item-section side class="text-weight-bold text-slate-900 num-tabular">
                  ₱{{ parseFloat(item.subtotal).toFixed(2) }}
                </q-item-section>
              </q-item>
            </q-list>

            <!-- Financial Totals Breakdown -->
            <div class="row q-col-gutter-xs text-body2 q-pt-xs">
              <div class="col-6 text-slate-600">Grand Total:</div>
              <div class="col-6 text-weight-bold text-right text-h6 text-slate-900 num-tabular">
                ₱{{ parseFloat(receiptDialog.tx.total_amount || 0).toFixed(2) }}
              </div>

              <div class="col-6 text-slate-600">Amount Tendered:</div>
              <div class="col-6 text-weight-bold text-right text-emerald-7 num-tabular">
                ₱{{ parseFloat(receiptDialog.tx.amount_paid || 0).toFixed(2) }}
              </div>

              <div class="col-6 text-slate-600">
                {{ receiptDialog.tx.transaction_type === 'CASH' ? 'Change Given:' : 'Remaining Balance:' }}
              </div>
              <div class="col-6 text-weight-bold text-right num-tabular" :class="receiptDialog.tx.transaction_type === 'CASH' ? 'text-indigo-7' : 'text-rose-6'">
                ₱{{ receiptDialog.tx.transaction_type === 'CASH'
                      ? parseFloat(receiptDialog.tx.change_given || 0).toFixed(2)
                      : (parseFloat(receiptDialog.tx.total_amount || 0) - parseFloat(receiptDialog.tx.amount_paid || 0)).toFixed(2) }}
              </div>
            </div>

            <!-- Footer Message -->
            <div class="text-center text-caption text-slate-400 q-mt-md pt-xs border-top-slate">
              Thank you for shopping at Nichole Agrivet!
            </div>
          </div>
        </q-card-section>

        <!-- Actions -->
        <q-card-actions align="between" class="q-px-lg q-pb-md">
          <q-btn outline color="primary" icon="print" label="Print Receipt" @click="printReceipt" />
          <q-btn color="positive" icon="check" label="Done / New Sale" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Add Product to Cart Dialog (Kilo & Sack Selector with Presets) -->
    <q-dialog v-model="addItemModal.open">
      <q-card style="width: 500px; max-width: 95vw; max-height: 90vh; display: flex; flex-direction: column;" class="rounded-borders-lg border-slate">
        <!-- Dialog Header -->
        <q-card-section class="bg-slate-900 text-white q-py-md row items-center justify-between">
          <div class="row items-center">
            <q-avatar size="36px" color="positive" text-color="white" class="q-mr-sm">
              <q-icon name="shopping_basket" size="20px" />
            </q-avatar>
            <div>
              <div class="text-h6 text-weight-bold leading-tight">{{ addItemModal.product?.name }}</div>
              <div class="text-caption text-slate-400">{{ addItemModal.product?.category_name }}</div>
            </div>
          </div>
          <q-btn flat round dense icon="close" color="slate-400" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-md scroll" style="flex: 1;" v-if="addItemModal.product">
          <!-- 1. Unit Type Selection Cards (Retail vs Bulk) -->
          <div class="q-mb-md" v-if="hasKiloPrice && hasSackPrice">
            <div class="text-caption text-weight-bold text-slate-700 text-uppercase q-mb-xs">Select Selling Unit</div>
            <div class="row q-col-gutter-sm">
              <!-- Retail Option Card -->
              <div class="col-6">
                <div
                  class="unit-select-card cursor-pointer q-pa-sm text-center relative-position"
                  :class="addItemModal.unitType === 'KILO' ? 'unit-card-active-kilo' : 'unit-card-inactive'"
                  @click="addItemModal.unitType = 'KILO'; onUnitTypeChange()"
                >
                  <q-icon :name="addItemModal.product.unit_retail_name === 'Kilo' ? 'scale' : 'local_offer'" size="26px" :color="addItemModal.unitType === 'KILO' ? 'positive' : 'slate-500'" class="q-mb-xs" />
                  <div class="text-subtitle2 text-weight-bold" :class="addItemModal.unitType === 'KILO' ? 'text-emerald-9' : 'text-slate-700'">
                    By {{ addItemModal.product.unit_retail_name || 'Item' }}
                  </div>
                  <div class="text-caption num-tabular text-weight-bold" :class="addItemModal.unitType === 'KILO' ? 'text-emerald-7' : 'text-slate-500'">
                    ₱{{ parseFloat(addItemModal.product.price_per_kilo).toFixed(2) }} / {{ addItemModal.product.unit_retail_name || 'item' }}
                  </div>
                  <q-badge v-if="addItemModal.unitType === 'KILO'" color="positive" class="absolute-top-right q-ma-xs">
                    ✓ Selected
                  </q-badge>
                </div>
              </div>

              <!-- Bulk Option Card -->
              <div class="col-6">
                <div
                  class="unit-select-card cursor-pointer q-pa-sm text-center relative-position"
                  :class="addItemModal.unitType === 'SACK' ? 'unit-card-active-sack' : 'unit-card-inactive'"
                  @click="addItemModal.unitType = 'SACK'; onUnitTypeChange()"
                >
                  <q-icon name="inventory_2" size="26px" :color="addItemModal.unitType === 'SACK' ? 'indigo-7' : 'slate-500'" class="q-mb-xs" />
                  <div class="text-subtitle2 text-weight-bold" :class="addItemModal.unitType === 'SACK' ? 'text-indigo-9' : 'text-slate-700'">
                    By {{ addItemModal.product.unit_bulk_name || 'Bulk' }}
                  </div>
                  <div class="text-caption num-tabular text-weight-bold" :class="addItemModal.unitType === 'SACK' ? 'text-indigo-7' : 'text-slate-500'">
                    ₱{{ parseFloat(addItemModal.product.price_per_sack).toFixed(2) }} / {{ addItemModal.product.unit_bulk_name || 'unit' }}
                  </div>
                  <q-badge v-if="addItemModal.unitType === 'SACK'" color="primary" class="absolute-top-right q-ma-xs">
                    ✓ Selected
                  </q-badge>
                </div>
              </div>
            </div>
          </div>
          <div class="q-mb-md" v-else>
            <div class="text-caption text-weight-bold text-slate-700 text-uppercase q-mb-xs">Selling Unit</div>
            <div class="bg-slate-100 border-slate rounded-borders q-pa-sm text-weight-bold text-slate-900">
              <span v-if="hasKiloPrice">🏷️ By {{ addItemModal.product.unit_retail_name || 'Item' }} • ₱{{ parseFloat(addItemModal.product.price_per_kilo).toFixed(2) }} / {{ addItemModal.product.unit_retail_name || 'item' }}</span>
              <span v-else>📦 By {{ addItemModal.product.unit_bulk_name || 'Bulk' }} • ₱{{ parseFloat(addItemModal.product.price_per_sack).toFixed(2) }} / {{ addItemModal.product.unit_bulk_name || 'unit' }}</span>
            </div>
          </div>

          <!-- 2. Quick Quantity Presets -->
          <div class="q-mb-md">
            <div class="row items-center justify-between q-mb-xs">
              <span class="text-caption text-weight-bold text-slate-700 text-uppercase">
                Quick Quantity Presets
              </span>
              <span class="text-caption text-slate-500">Click to select quantity</span>
            </div>

            <!-- Kilo Fraction Presets (Only if unit is Kilo) -->
            <div v-if="addItemModal.unitType === 'KILO' && isKiloUnit" class="row q-gutter-xs">
              <q-btn
                v-for="preset in kiloPresets"
                :key="preset.value"
                outline
                dense
                no-caps
                :color="addItemModal.quantity === preset.value ? 'positive' : 'grey-7'"
                :class="{ 'bg-green-1 text-weight-bold': addItemModal.quantity === preset.value }"
                class="q-px-sm text-caption"
                @click="addItemModal.quantity = preset.value"
              >
                {{ preset.label }}
              </q-btn>
            </div>

            <!-- Piece / Item Presets (If retail unit is Piece / Bottle / Item) -->
            <div v-else-if="addItemModal.unitType === 'KILO'" class="row q-gutter-xs">
              <q-btn
                v-for="preset in piecePresets"
                :key="preset.value"
                outline
                dense
                no-caps
                :color="addItemModal.quantity === preset.value ? 'positive' : 'grey-7'"
                :class="{ 'bg-green-1 text-weight-bold': addItemModal.quantity === preset.value }"
                class="q-px-sm text-caption"
                @click="addItemModal.quantity = preset.value"
              >
                {{ preset.label }}
              </q-btn>
            </div>

            <!-- Bulk Quantity Presets -->
            <div v-else class="row q-gutter-xs">
              <q-btn
                v-for="preset in getBulkPresets()"
                :key="preset.value"
                outline
                dense
                no-caps
                :color="addItemModal.quantity === preset.value ? 'primary' : 'grey-7'"
                :class="{ 'bg-indigo-1 text-weight-bold': addItemModal.quantity === preset.value }"
                class="q-px-sm text-caption"
                @click="addItemModal.quantity = preset.value"
              >
                {{ preset.label }}
              </q-btn>
            </div>
          </div>

          <!-- 3. Custom Quantity Input -->
          <div class="q-mb-md">
            <div class="text-caption text-weight-bold text-slate-700 text-uppercase q-mb-xs">
              Quantity (Custom Amount)
            </div>
            <q-input
              v-model.number="addItemModal.quantity"
              type="number"
              step="0.05"
              min="0.01"
              outlined
              dense
              class="num-tabular text-h6"
              @update:model-value="validateModalQuantity"
            >
              <template v-slot:append>
                <span class="text-caption text-weight-bold text-slate-600">
                  {{ addItemModal.unitType === 'SACK' ? (addItemModal.product.unit_bulk_name || 'Bulk') : (addItemModal.product.unit_retail_name || 'Item') }}(s)
                </span>
              </template>
            </q-input>
          </div>

          <!-- 4. Subtotal Calculation Box -->
          <div class="bg-slate-50 border-slate rounded-borders q-pa-md">
            <div class="row justify-between text-caption text-slate-600 q-mb-xs">
              <span>Unit Price:</span>
              <span class="text-weight-bold num-tabular">₱{{ currentUnitPrice.toFixed(2) }} / {{ addItemModal.unitType === 'SACK' ? (addItemModal.product.unit_bulk_name || 'unit') : (addItemModal.product.unit_retail_name || 'item') }}</span>
            </div>

            <div class="row justify-between text-caption text-slate-600 q-mb-sm">
              <span>Stock Available:</span>
              <span class="text-weight-medium num-tabular">
                {{ addItemModal.unitType === 'SACK' ? (parseFloat(addItemModal.product.stock_sacks) + ' ' + (addItemModal.product.unit_bulk_name || 'Bulk') + 's') : (parseFloat(addItemModal.product.stock_kilos) + ' ' + (addItemModal.product.unit_retail_name || 'Items')) }}
              </span>
            </div>

            <q-separator class="q-my-xs" />

            <div class="row justify-between items-center text-subtitle1 q-mt-xs">
              <span class="text-weight-bold text-slate-900">Calculated Subtotal:</span>
              <span class="text-h5 text-weight-bold text-positive num-tabular">₱{{ calculatedSubtotal.toFixed(2) }}</span>
            </div>
          </div>
        </q-card-section>

        <!-- Dialog Action Buttons -->
        <q-card-actions align="between" class="q-px-md q-py-sm bg-white border-top-slate">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            color="positive"
            unelevated
            icon="add_shopping_cart"
            :label="'Add to Cart • ₱' + calculatedSubtotal.toFixed(2)"
            class="q-px-md text-weight-bold"
            :disable="addItemModal.quantity <= 0 || isNaN(addItemModal.quantity)"
            @click="confirmAddToCart"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import logoUrl from 'src/images/Nichole Agrivet.png'

const $q = useQuasar()

// State lists
const products = ref([])
const customers = ref([])
const categories = ref([])

// Filtering state
const searchQuery = ref('')
const selectedCategory = ref(null)

// Cart & Checkout state
const cart = ref([])
const paymentMethod = ref('CASH')
const cashTendered = ref(null)
const gcashRef = ref('')
const selectedCustomer = ref(null)
const amountPaid = ref(null)

// Numpad & Quick Bills helpers
function selectQuickBill(amount) {
  cashTendered.value = Math.ceil(amount)
}

function handleNumpadKey(key) {
  let currentStr = cashTendered.value !== null && cashTendered.value !== undefined ? String(cashTendered.value) : ''

  if (key === 'C') {
    cashTendered.value = null
  } else if (key === 'BACKSPACE') {
    if (currentStr.length > 1) {
      cashTendered.value = parseFloat(currentStr.slice(0, -1))
    } else {
      cashTendered.value = null
    }
  } else {
    if (currentStr === '0' || currentStr === '') {
      currentStr = key
    } else {
      currentStr += key
    }
    cashTendered.value = parseFloat(currentStr)
  }
}

// Dialog state
const customerDialog = ref({
  open: false,
  name: '',
  contact: '',
  notes: ''
})

const receiptDialog = ref({
  open: false,
  tx: {}
})

const addItemModal = ref({
  open: false,
  product: null,
  unitType: 'KILO',
  quantity: 1
})

// Presets for quick selection
const kiloPresets = [
  { label: '¼ kg (0.25)', value: 0.25 },
  { label: '½ kg (0.5)', value: 0.5 },
  { label: '¾ kg (0.75)', value: 0.75 },
  { label: '1 kg', value: 1 },
  { label: '1.5 kg', value: 1.5 },
  { label: '2 kg', value: 2 },
  { label: '3 kg', value: 3 },
  { label: '5 kg', value: 5 },
  { label: '10 kg', value: 10 }
]

const piecePresets = [
  { label: '1 Pc', value: 1 },
  { label: '2 Pcs', value: 2 },
  { label: '3 Pcs', value: 3 },
  { label: '5 Pcs', value: 5 },
  { label: '6 Pcs', value: 6 },
  { label: '10 Pcs', value: 10 },
  { label: '12 Pcs (1 Doz)', value: 12 },
  { label: '24 Pcs (2 Doz)', value: 24 }
]

const isKiloUnit = computed(() => {
  const retailName = (addItemModal.value.product?.unit_retail_name || 'Kilo').toLowerCase()
  return retailName === 'kilo' || retailName === 'kg'
})

function getBulkPresets() {
  const bulkName = addItemModal.value.product?.unit_bulk_name || 'Unit'
  return [
    { label: `1 ${bulkName}`, value: 1 },
    { label: `2 ${bulkName}s`, value: 2 },
    { label: `3 ${bulkName}s`, value: 3 },
    { label: `5 ${bulkName}s`, value: 5 },
    { label: `10 ${bulkName}s`, value: 10 }
  ]
}

// Modal calculations
const hasKiloPrice = computed(() => {
  return addItemModal.value.product && parseFloat(addItemModal.value.product.price_per_kilo || 0) > 0
})

const hasSackPrice = computed(() => {
  return addItemModal.value.product && parseFloat(addItemModal.value.product.price_per_sack || 0) > 0
})

const currentUnitPrice = computed(() => {
  if (!addItemModal.value.product) return 0
  if (addItemModal.value.unitType === 'SACK') {
    return parseFloat(addItemModal.value.product.price_per_sack || 0)
  }
  return parseFloat(addItemModal.value.product.price_per_kilo || 0)
})

const calculatedSubtotal = computed(() => {
  const qty = parseFloat(addItemModal.value.quantity) || 0
  return qty * currentUnitPrice.value
})

function openAddProductModal(product) {
  addItemModal.value.product = product
  if (parseFloat(product.price_per_kilo || 0) > 0) {
    addItemModal.value.unitType = 'KILO'
  } else {
    addItemModal.value.unitType = 'SACK'
  }
  addItemModal.value.quantity = 1
  addItemModal.value.open = true
}

function onUnitTypeChange() {
  addItemModal.value.quantity = 1
}

function validateModalQuantity() {
  if (addItemModal.value.quantity <= 0 || isNaN(addItemModal.value.quantity)) {
    addItemModal.value.quantity = 1
  }
}

function confirmAddToCart() {
  const product = addItemModal.value.product
  const unitType = addItemModal.value.unitType
  const quantity = parseFloat(addItemModal.value.quantity) || 1
  const price = currentUnitPrice.value

  if (quantity <= 0 || !product) return

  // Check if item already exists in cart with same unit type
  const existingIndex = cart.value.findIndex(item => item.product.id === product.id && item.unitType === unitType)

  if (existingIndex > -1) {
    cart.value[existingIndex].quantity += quantity
  } else {
    cart.value.push({
      product,
      unitType,
      quantity,
      price
    })
  }

  const unitLabel = unitType === 'SACK' ? (product.unit_bulk_name || 'Bulk') : (product.unit_retail_name || 'Item')
  $q.notify({
    color: 'emerald-8',
    message: `${product.name} (${quantity} ${unitLabel}) added to cart.`,
    icon: 'shopping_basket',
    timeout: 1200
  })

  addItemModal.value.open = false
}

// Options mappings
const categoryOptions = computed(() => {
  const list = categories.value.map(cat => ({ label: cat.name, value: cat.id }))
  return [{ label: 'All Categories', value: null }, ...list]
})

const customerOptions = computed(() => {
  return customers.value
})

// Filtered products list
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === null || product.category === selectedCategory.value
    return matchesSearch && matchesCategory && product.is_active
  })
})

// Cart calculations
const grandTotal = computed(() => {
  return cart.value.reduce((sum, item) => sum + (item.quantity * item.price), 0)
})

const canCheckout = computed(() => {
  if (cart.value.length === 0) return false
  if (paymentMethod.value === 'CASH') {
    return cashTendered.value >= grandTotal.value
  } else if (paymentMethod.value === 'GCASH') {
    return true
  } else {
    // CREDIT
    return selectedCustomer.value !== null
  }
})

// Formatting helper
function formatDateTime(dateTimeStr) {
  if (!dateTimeStr) return ''
  const date = new Date(dateTimeStr)
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

function printReceipt() {
  window.print()
}

// API Calls
async function fetchData() {
  try {
    const prodRes = await api.get('products/')
    products.value = prodRes.data

    const custRes = await api.get('customers/')
    customers.value = custRes.data

    const catRes = await api.get('categories/')
    categories.value = catRes.data
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to sync database data.',
      icon: 'report_problem'
    })
  }
}

function removeFromCart(index) {
  cart.value.splice(index, 1)
}

function clearCart() {
  cart.value = []
  cashTendered.value = null
  gcashRef.value = ''
  selectedCustomer.value = null
  amountPaid.value = null
}

function validateQuantity(item) {
  if (item.quantity <= 0 || isNaN(item.quantity)) {
    item.quantity = 1
  }
}

// Dialog management
function openNewCustomerDialog() {
  customerDialog.value.name = ''
  customerDialog.value.contact = ''
  customerDialog.value.notes = ''
  customerDialog.value.open = true
}

async function saveNewCustomer() {
  try {
    const res = await api.post('customers/', {
      name: customerDialog.value.name,
      contact_number: customerDialog.value.contact,
      notes: customerDialog.value.notes
    })
    customers.value.push(res.data)
    selectedCustomer.value = res.data // Set as active
    customerDialog.value.open = false
    $q.notify({
      color: 'positive',
      message: `Customer ${res.data.name} added!`,
      icon: 'person'
    })
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to create new customer.',
      icon: 'error'
    })
  }
}

// Submit Transaction
async function submitTransaction() {
  try {
    let paidAmount = grandTotal.value
    if (paymentMethod.value === 'CASH') {
      paidAmount = cashTendered.value
    } else if (paymentMethod.value === 'CREDIT') {
      paidAmount = amountPaid.value || 0.00
    }

    const payload = {
      transaction_type: paymentMethod.value,
      reference_number: paymentMethod.value === 'GCASH' ? (gcashRef.value || null) : null,
      customer: paymentMethod.value === 'CREDIT' ? selectedCustomer.value.id : null,
      total_amount: grandTotal.value,
      amount_paid: paidAmount,
      change_given: paymentMethod.value === 'CASH' ? Math.max(0, cashTendered.value - grandTotal.value) : 0.00,
      items: cart.value.map(item => ({
        product: item.product.id,
        unit_type: item.unitType,
        quantity: item.quantity,
        unit_price: item.price,
        subtotal: item.quantity * item.price
      }))
    }

    const res = await api.post('transactions/', payload)
    
    // Open Transaction Finished Receipt Modal
    receiptDialog.value.tx = res.data
    receiptDialog.value.open = true

    $q.notify({
      color: 'positive',
      message: 'Transaction finished successfully!',
      icon: 'check_circle'
    })

    clearCart()
    fetchData() // Refresh stock levels
  } catch (err) {
    console.error(err)
    $q.notify({
      color: 'negative',
      message: 'Failed to complete transaction. Check stock limits.',
      icon: 'error'
    })
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
h1 {
  font-size: 2rem;
  line-height: 2.5rem;
}
.fit-height {
  height: 100%;
}
.scroll-container {
  overflow-y: auto;
  max-height: 60vh;
}
.product-item-card {
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.hover-grow:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.quantity-input {
  width: 70px;
}
.bg-indigo-10 {
  background-color: #1a237e !important;
}
.bg-indigo-1 {
  background-color: #e8eaf6 !important;
}
.bg-green-1 {
  background-color: #e8f5e9 !important;
}
.bg-orange-1 {
  background-color: #fff3e0 !important;
}
.rounded-borders {
  border-radius: 6px;
}
.receipt-paper {
  background: #f8fafc;
}
.border-slate {
  border: 1.5px solid #cbd5e1;
}
.border-top-slate {
  border-top: 1.5px solid #cbd5e1;
  padding-top: 8px;
}
.num-tabular {
  font-variant-numeric: tabular-nums lining-nums;
}

.unit-select-card {
  border-radius: 8px;
  transition: all 0.2s ease-in-out;
}
.unit-card-active-kilo {
  border: 2px solid #059669;
  background-color: #ecfdf5;
  box-shadow: 0 4px 12px -2px rgba(5, 150, 105, 0.25);
}
.unit-card-active-sack {
  border: 2px solid #4338ca;
  background-color: #eef2ff;
  box-shadow: 0 4px 12px -2px rgba(67, 56, 202, 0.25);
}
.unit-card-inactive {
  border: 1.5px solid #cbd5e1;
  background-color: #f8fafc;
}
.unit-card-inactive:hover {
  border-color: #94a3b8;
  background-color: #ffffff;
  transform: translateY(-1px);
}

@media print {
  body * {
    visibility: hidden;
  }
  .printable-area, .printable-area * {
    visibility: visible;
  }
  .printable-area {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }
}
</style>
