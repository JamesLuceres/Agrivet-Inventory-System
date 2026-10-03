<template>
  <q-page class="pos-screen q-pa-md">
    <!-- 1. TOP HEADER BAR: Hamburger Menu + Shift Sales on Left, Search in Middle, Controls on Right -->
    <div class="row items-center justify-between no-wrap q-col-gutter-md q-mb-md top-pos-header">
      <!-- Left: Navigation Menu Hamburger Button + Today's Shift Counter -->
      <div class="col-auto row items-center no-wrap q-gutter-x-sm">
        <q-btn
          flat
          dense
          icon="menu"
          color="slate-8"
          class="bg-white border-slate header-hamburger-btn"
          @click="toggleDrawer"
        >
          <q-tooltip>Open Main Navigation Menu</q-tooltip>
        </q-btn>

        <div
          class="shift-counter-pill row items-center no-wrap bg-white cursor-pointer"
          @click="openShiftZReading"
        >
          <div class="shift-icon-wrap flex flex-center q-mr-sm">
            <q-icon name="point_of_sale" size="20px" color="primary" />
          </div>
          <div class="column justify-center no-wrap">
            <span class="shift-label text-uppercase text-weight-bold"> Today's Shift </span>
            <span class="shift-amount text-weight-bolder num-tabular">
              ₱{{
                todayShiftTotal.toLocaleString('en-US', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })
              }}
            </span>
          </div>
          <q-tooltip>Click for Shift Z-Reading & Cash Drawer Count</q-tooltip>
        </div>
      </div>

      <!-- Center: Clean SKU/Product Search Input with Quick Calculator -->
      <div class="col">
        <q-input
          v-model="searchQuery"
          placeholder="Tap to search SKU or product name..."
          outlined
          dense
          clearable
          class="bg-white tablet-sku-search"
        >
          <template v-slot:prepend>
            <q-icon name="search" color="slate-400" size="22px" />
          </template>
          <template v-slot:append>
            <q-btn
              flat
              round
              dense
              icon="calculate"
              color="deep-orange-7"
              class="q-mr-xs"
              @click="openCalculator"
            >
              <q-tooltip>Quick Price & Feeds Calculator</q-tooltip>
            </q-btn>
          </template>
        </q-input>
      </div>

      <!-- Right: Notifications & Cashier Profile Controls (Consistent across all pages) -->
      <div class="col-auto">
        <TopHeaderControls />
      </div>
    </div>

    <!-- 2. CATEGORIES FILTER BAR (Touch horizontal swipe) -->
    <div class="categories-scroll-wrapper q-mb-md">
      <div class="row items-center no-wrap q-gutter-x-sm no-scrollbar overflow-x-auto q-pb-xs">
        <!-- ALL Category Pill -->
        <div
          class="category-pill"
          :class="{ 'category-pill-active': selectedCategory === null }"
          @click="selectedCategory = null"
        >
          <span class="q-mr-xs">📦</span>
          <span>All ({{ products.length }})</span>
        </div>

        <!-- Dynamic Category Pills with Emojis -->
        <div
          v-for="cat in categoryPillList"
          :key="cat.id"
          class="category-pill"
          :class="{ 'category-pill-active': selectedCategory === cat.id }"
          @click="selectedCategory = cat.id"
        >
          <span class="q-mr-xs">{{ cat.emoji }}</span>
          <span>{{ cat.name }}</span>
        </div>
      </div>
    </div>

    <!-- 3. MAIN WORKSPACE: 2-COLUMN GRID (Catalog Cards on Left + Order Details on Right) -->
    <div class="row q-col-gutter-md items-start no-wrap pos-main-row">
      <!-- LEFT/CENTER SECTION: DYNAMIC PRODUCT CARDS GRID -->
      <div class="col pos-products-catalog">
        <div
          v-if="filteredProducts.length === 0"
          class="text-center text-slate-400 q-py-xl bg-white rounded-borders border-slate"
        >
          <q-icon name="inventory_2" size="48px" class="q-mb-xs" />
          <div class="text-weight-medium">No products found in this category.</div>
        </div>

        <div class="row q-col-gutter-sm">
          <div
            v-for="product in filteredProducts"
            :key="product.id"
            class="col-12 col-sm-6 col-md-4"
          >
            <q-card
              flat
              class="pos-product-card bg-white cursor-pointer q-pa-xs hover-grow"
              :class="{
                'pos-product-out-of-stock': isProductOutOfStock(product),
                'pos-product-low-stock':
                  !isProductOutOfStock(product) && isProductLowStock(product),
              }"
              @click="handleProductCardClick(product)"
            >
              <q-card-section class="q-pa-sm">
                <!-- Top Row: Icon Squircle + Unit/Stock Tag -->
                <div class="row items-center justify-between no-wrap q-mb-xs">
                  <div
                    class="product-icon-squircle"
                    :style="{ backgroundColor: getCategoryBg(product) }"
                  >
                    <span style="font-size: 1.15rem">{{ getProductEmoji(product) }}</span>
                  </div>

                  <!-- Tag: Out of Stock pill OR Low stock pill OR unit tag OR Service tag -->
                  <div
                    v-if="
                      product.is_service ||
                      product.name.includes('GCash') ||
                      product.name.includes('Other')
                    "
                  >
                    <span
                      :class="
                        product.name.includes('GCash') ? 'badge-tag-blue' : 'badge-tag-purple'
                      "
                    >
                      {{ product.name.includes('GCash') ? '📱 E-Money' : '🏷️ Custom' }}
                    </span>
                  </div>
                  <div v-else-if="isProductOutOfStock(product)">
                    <span class="badge-tag-out-of-stock"> Out of Stock </span>
                  </div>
                  <div v-else-if="isProductLowStock(product)">
                    <span class="badge-tag-red">
                      {{ getStockDisplay(product).badgeText }}
                    </span>
                  </div>
                  <div v-else>
                    <span :class="getProductTagClass(product)">
                      {{ getProductTagLabel(product) }}
                    </span>
                  </div>
                </div>

                <!-- Product Title -->
                <div
                  class="text-subtitle2 text-weight-bold text-slate-900 ellipsis q-mt-xs leading-tight"
                >
                  {{ product.name }}
                </div>

                <!-- Stock Subtitle -->
                <div
                  class="text-caption q-mt-xs"
                  :class="
                    product.is_service ||
                    product.name.includes('GCash') ||
                    product.name.includes('Other')
                      ? 'text-primary font-medium'
                      : isProductOutOfStock(product)
                        ? 'text-slate-400 font-medium'
                        : isProductLowStock(product)
                          ? 'text-negative text-weight-bold'
                          : 'text-slate-400'
                  "
                >
                  <span
                    v-if="
                      product.is_service ||
                      product.name.includes('GCash') ||
                      product.name.includes('Other')
                    "
                  >
                    Tap to set Amount & Charge
                  </span>
                  <span v-else-if="isProductOutOfStock(product)">Out of Stock</span>
                  <span v-else-if="isProductLowStock(product)">
                    <q-icon name="warning" size="13px" class="q-mr-xs" />
                    Low Stock: {{ getStockDisplay(product).fullText }}
                  </span>
                  <span v-else>
                    {{ getStockDisplay(product).fullText }}
                  </span>
                </div>

                <!-- Bottom Row: Price & Green Plus Button -->
                <div class="row items-center justify-between q-mt-md q-pt-xs border-top-subtle">
                  <div class="text-subtitle1 text-weight-bold text-slate-900 num-tabular">
                    <span
                      v-if="
                        product.is_service ||
                        product.name.includes('GCash') ||
                        product.name.includes('Other')
                      "
                      class="text-caption text-weight-bolder text-primary"
                    >
                      Custom Amount
                    </span>
                    <span v-else>
                      <template v-if="product.price_per_kilo">
                        ₱{{
                          parseFloat(product.price_per_kilo).toLocaleString('en-US', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })
                        }}
                        <span class="text-caption text-slate-500" style="font-size: 0.72rem"
                          >/{{ getRetailUnitLabel(product) }}</span
                        >
                      </template>
                      <template v-else>
                        ₱{{
                          (parseFloat(product.price_per_sack) || 0).toLocaleString('en-US', {
                            minimumFractionDigits: 2,
                            maximumFractionDigits: 2,
                          })
                        }}
                      </template>
                    </span>
                  </div>

                  <div
                    class="mint-plus-btn row items-center justify-center cursor-pointer"
                    :class="{
                      'mint-plus-btn-disabled cursor-not-allowed':
                        !product.is_service &&
                        !product.name.includes('GCash') &&
                        !product.name.includes('Other') &&
                        isProductOutOfStock(product),
                    }"
                    @click.stop="quickAddToCart(product, $event)"
                  >
                    <q-icon
                      :name="
                        !product.is_service &&
                        !product.name.includes('GCash') &&
                        !product.name.includes('Other') &&
                        isProductOutOfStock(product)
                          ? 'block'
                          : 'add'
                      "
                      size="18px"
                      :color="
                        !product.is_service &&
                        !product.name.includes('GCash') &&
                        !product.name.includes('Other') &&
                        isProductOutOfStock(product)
                          ? 'grey-5'
                          : 'primary'
                      "
                    />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>

      <!-- RIGHT SECTION: DEDICATED ORDER & CHECKOUT PANEL -->
      <div class="col-auto pos-checkout-column">
        <q-card flat class="pos-checkout-panel bg-white column no-wrap justify-between">
          <q-card-section class="q-pa-md">
            <!-- Customer Farm Card Header -->
            <div
              class="customer-farm-card row items-center justify-between q-pa-sm rounded-borders q-mb-md"
            >
              <div class="row items-center no-wrap">
                <div class="farm-icon-squircle q-mr-sm">
                  <span>🌾</span>
                </div>
                <div>
                  <div
                    class="text-subtitle2 text-weight-bold text-slate-900 leading-tight ellipsis"
                    style="max-width: 150px"
                  >
                    {{ selectedCustomer ? selectedCustomer.name : 'Walk-in Customer' }}
                  </div>
                  <div class="text-caption text-slate-500 font-medium" style="font-size: 0.72rem">
                    {{
                      selectedCustomer
                        ? selectedCustomer.contact_number || 'Registered Account'
                        : 'Direct Counter Sale'
                    }}
                  </div>
                </div>
              </div>

              <q-btn
                flat
                dense
                no-caps
                label="Switch"
                class="bg-white border-slate text-caption text-weight-bold q-px-sm text-slate-700"
                style="border-radius: 9999px"
                @click="showCustomerPicker = true"
              />
            </div>

            <!-- Cart Items List Header -->
            <div
              class="row items-center justify-between text-caption text-weight-bold text-slate-400 text-uppercase tracking-wider q-mb-xs"
            >
              <span>Current Order</span>
              <q-btn
                flat
                dense
                no-caps
                color="negative"
                icon="delete_sweep"
                label="Clear"
                size="xs"
                @click="clearCart"
                :disable="cart.length === 0"
              />
            </div>

            <!-- Empty State -->
            <div v-if="cart.length === 0" class="text-center text-slate-400 q-py-xl">
              <q-icon name="shopping_basket" size="40px" class="q-mb-xs" />
              <div class="text-weight-medium">Cart is empty</div>
              <div class="text-caption">Tap any item from the catalog to add.</div>
            </div>

            <!-- Items Rows -->
            <q-list v-else class="cart-items-scroll scroll no-border">
              <q-item
                v-for="(item, index) in cart"
                :key="index"
                class="q-px-none q-py-sm border-bottom-subtle"
              >
                <q-item-section>
                  <q-item-label class="text-weight-bold text-slate-900 text-body2 leading-tight">
                    {{ item.customName || item.product.name }}
                  </q-item-label>
                  <q-item-label caption class="text-slate-400 q-mt-xs num-tabular">
                    <span v-if="item.feeDetails" class="text-primary text-weight-medium q-mr-xs"
                      >{{ item.feeDetails }} •
                    </span>
                    ₱{{ item.price.toFixed(2) }} × {{ item.quantity }}
                  </q-item-label>
                </q-item-section>

                <!-- Steppers & Line Total -->
                <q-item-section side class="items-end">
                  <div class="row items-center q-gutter-x-sm no-wrap">
                    <!-- Clean [-] [Qty] [+] Stepper (Matches mockup!) -->
                    <div class="row items-center no-wrap q-gutter-x-xs">
                      <button class="cart-stepper-btn" @click="decreaseCartQty(item, index)">
                        -
                      </button>
                      <span
                        class="text-weight-bold num-tabular text-body2 q-px-xs text-center"
                        style="min-width: 24px"
                      >
                        {{ item.quantity }}
                      </span>
                      <button class="cart-stepper-btn" @click="increaseCartQty(item)">+</button>
                    </div>

                    <!-- Line Total -->
                    <div
                      class="text-weight-bold text-slate-900 num-tabular text-body2"
                      style="min-width: 75px; text-align: right"
                    >
                      ₱{{
                        (item.quantity * item.price).toLocaleString('en-US', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })
                      }}
                    </div>
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </q-card-section>

          <!-- BOTTOM FINANCIAL & PAYMENT SECTION -->
          <q-card-section class="q-pa-md bg-white border-top-slate">
            <!-- Subtotal & Total Rows (No discounts currently) -->
            <div class="q-mb-sm">
              <div class="row justify-between text-body2 text-slate-600 q-mb-xs">
                <span>Subtotal</span>
                <span class="num-tabular text-weight-medium text-slate-900">
                  ₱{{
                    subtotalAmount.toLocaleString('en-US', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })
                  }}
                </span>
              </div>
              <div
                class="row justify-between items-center text-subtitle1 q-pt-xs border-top-subtle"
              >
                <span
                  class="text-weight-bolder text-slate-900 text-uppercase tracking-wider"
                  style="font-size: 0.85rem"
                  >TOTAL DUE</span
                >
                <span class="text-h5 text-weight-bolder text-slate-900 num-tabular">
                  ₱{{
                    totalDueAmount.toLocaleString('en-US', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })
                  }}
                </span>
              </div>
            </div>

            <!-- Payment Switch Row: [Cash] [GCash] [Credit] -->
            <div class="row q-gutter-xs q-mb-md">
              <q-btn
                flat
                dense
                no-caps
                icon="payments"
                label="Cash"
                :class="
                  paymentMethod === 'CASH'
                    ? 'bg-primary text-white'
                    : 'bg-white border-slate text-slate-800'
                "
                class="col text-caption text-weight-bold rounded-borders"
                style="height: 36px"
                @click="paymentMethod = 'CASH'"
              />
              <q-btn
                flat
                dense
                no-caps
                icon="smartphone"
                label="GCash"
                :class="
                  paymentMethod === 'GCASH'
                    ? 'bg-primary text-white'
                    : 'bg-white border-slate text-slate-800'
                "
                class="col text-caption text-weight-bold rounded-borders"
                style="height: 36px"
                @click="paymentMethod = 'GCASH'"
              />
              <q-btn
                flat
                dense
                no-caps
                icon="receipt"
                label="Credit"
                :class="
                  paymentMethod === 'CREDIT'
                    ? 'bg-primary text-white'
                    : 'bg-white border-slate text-slate-800'
                "
                class="col text-caption text-weight-bold rounded-borders"
                style="height: 36px"
                @click="selectCreditPayment"
              />
            </div>

            <!-- BIG SOLID FOREST GREEN PRIMARY BUTTON -->
            <q-btn
              unelevated
              class="full-width btn-agrivet-green q-py-md text-subtitle1 row items-center justify-between"
              :disable="cart.length === 0"
              @click="paymentMethod === 'CASH' ? openCashTenderedModal() : submitTransaction()"
            >
              <div class="row items-center no-wrap">
                <q-icon name="credit_card" class="q-mr-sm" size="22px" />
                <span>CHARGE / PAY</span>
              </div>
              <div class="num-tabular text-weight-bold">
                ₱{{
                  totalDueAmount.toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                }}
                →
              </div>
            </q-btn>
          </q-card-section>
        </q-card>
      </div>
    </div>

    <!-- Add Product Dialog (Bulk/Retail Selector) -->
    <q-dialog v-model="addItemModal.open">
      <q-card style="width: 480px; max-width: 95vw" class="rounded-borders-lg">
        <q-card-section class="row items-center justify-between q-pb-none">
          <div class="row items-center no-wrap">
            <div
              class="product-icon-squircle q-mr-sm"
              :style="{ backgroundColor: getCategoryBg(addItemModal.product) }"
            >
              <span style="font-size: 1.25rem">{{ getProductEmoji(addItemModal.product) }}</span>
            </div>
            <div>
              <div class="text-subtitle1 text-weight-bold text-slate-900">
                {{ addItemModal.product?.name }}
              </div>
              <div class="text-caption text-slate-400">
                {{ addItemModal.product?.category_name }}
              </div>
            </div>
          </div>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>

        <q-card-section class="q-pa-md" v-if="addItemModal.product">
          <!-- Unit Selector -->
          <div class="q-mb-md" v-if="hasKiloPrice && hasSackPrice">
            <div class="text-caption text-weight-bold text-slate-700 text-uppercase q-mb-xs">
              Unit Type
            </div>
            <div class="row q-col-gutter-sm">
              <div class="col-6">
                <div
                  class="category-pill full-width justify-center cursor-pointer"
                  :class="{ 'category-pill-active': addItemModal.unitType === 'KILO' }"
                  @click="setUnitType('KILO')"
                >
                  By {{ getRetailUnitLabel(addItemModal.product) }} • ₱{{
                    parseFloat(addItemModal.product.price_per_kilo).toFixed(2)
                  }}
                </div>
              </div>
              <div class="col-6">
                <div
                  class="category-pill full-width justify-center cursor-pointer"
                  :class="{ 'category-pill-active': addItemModal.unitType === 'SACK' }"
                  @click="setUnitType('SACK')"
                >
                  By {{ getBulkUnitLabel(addItemModal.product) }} • ₱{{
                    parseFloat(addItemModal.product.price_per_sack).toFixed(2)
                  }}
                </div>
              </div>
            </div>
          </div>

          <!-- Live Available Stock Notice -->
          <div
            class="q-mb-md text-caption text-slate-600 bg-slate-50 border-slate rounded-borders q-pa-xs text-center"
            v-if="addItemModal.product"
          >
            <span>Available in Stock: </span>
            <strong class="text-slate-900 num-tabular">
              {{ getAvailableStockForUnit(addItemModal.product, addItemModal.unitType) }}
              {{
                addItemModal.unitType === 'SACK'
                  ? (addItemModal.product.unit_bulk_name || 'Sack') + 's'
                  : (addItemModal.product.unit_retail_name || 'Item') + 's'
              }}
            </strong>
            <span
              v-if="addItemModal.product.unit_bulk_name && addItemModal.product.price_per_sack"
              class="text-slate-400 q-ml-xs"
            >
              (Total Pool: {{ getProductTotalBaseStock(addItemModal.product).toFixed(1) }}
              {{ addItemModal.product.unit_retail_name || 'kilos' }})
            </span>
          </div>

          <!-- If Unit Type is KILO: Mode Selector (By Weight vs By Budget) -->
          <div class="q-mb-md" v-if="addItemModal.unitType === 'KILO'">
            <q-btn-toggle
              v-model="addItemModal.pricingMode"
              spread
              rounded
              unelevated
              dense
              toggle-color="primary"
              color="slate-100"
              text-color="slate-7"
              class="border-slate text-weight-bold text-caption"
              @update:model-value="onPricingModeSwitch"
              :options="[
                {
                  label: '⚖️ By Weight (' + getRetailUnitLabel(addItemModal.product) + ')',
                  value: 'WEIGHT',
                },
                { label: '₱ By Peso Budget', value: 'BUDGET' },
              ]"
            />
          </div>

          <!-- 1. BUDGET MODE: Customer has a budget in Pesos (e.g. ₱50) -->
          <div
            v-if="addItemModal.unitType === 'KILO' && addItemModal.pricingMode === 'BUDGET'"
            class="q-mb-md"
          >
            <div class="row justify-between items-center q-mb-xs">
              <span
                class="text-caption text-weight-bold text-slate-700 text-uppercase"
                style="font-size: 0.68rem; letter-spacing: 0.04em"
              >
                Customer Peso Budget (₱)
              </span>
              <span class="text-caption text-primary text-weight-bold" style="font-size: 0.72rem">
                @ ₱{{ currentUnitPrice.toFixed(2) }} /
                {{ getRetailUnitLabel(addItemModal.product) }}
              </span>
            </div>
            <q-input
              v-model.number="addItemModal.budgetAmount"
              type="number"
              prefix="₱"
              placeholder="e.g. 50"
              outlined
              dense
              class="text-weight-bold text-h6"
              autofocus
              @update:model-value="onBudgetAmountChange"
            />

            <!-- Quick Budget Presets -->
            <div class="row q-col-gutter-xs q-mt-xs">
              <div class="col-3" v-for="bAmt in [20, 50, 100, 200]" :key="bAmt">
                <q-btn
                  unelevated
                  no-caps
                  dense
                  :label="`₱${bAmt}`"
                  class="full-width text-weight-bold border-slate"
                  :class="
                    addItemModal.budgetAmount === bAmt
                      ? 'bg-emerald-100 text-emerald-9 border-primary'
                      : 'bg-slate-50 text-slate-800'
                  "
                  style="height: 38px; border-radius: 8px; font-size: 0.85rem"
                  @click="setBudgetPreset(bAmt)"
                />
              </div>
            </div>

            <!-- Big Scale Weighing Result Banner -->
            <div class="rounded-borders border-slate bg-emerald-50 q-pa-md q-mt-sm text-center">
              <div
                class="text-caption text-slate-600 text-weight-bold text-uppercase"
                style="letter-spacing: 0.05em; font-size: 0.68rem"
              >
                ⚖️ WEIGH ON SCALE
              </div>
              <div
                class="text-h3 text-weight-bolder text-primary num-tabular leading-tight q-my-xs"
              >
                {{ (parseFloat(addItemModal.quantity) || 0).toFixed(2) }}
                <span class="text-h6 text-weight-bold"
                  >{{ getRetailUnitLabel(addItemModal.product) }}s</span
                >
              </div>
              <div class="text-caption text-slate-600 font-tabular" style="font-size: 0.75rem">
                ₱{{ (parseFloat(addItemModal.budgetAmount) || 0).toFixed(2) }} ÷ ₱{{
                  currentUnitPrice.toFixed(2)
                }}
                = {{ (parseFloat(addItemModal.quantity) || 0).toFixed(2) }}
                {{ getRetailUnitLabel(addItemModal.product) }}s
              </div>
            </div>
          </div>

          <!-- 2. WEIGHT / QUANTITY MODE -->
          <div v-else class="q-mb-md">
            <div class="text-caption text-weight-bold text-slate-700 text-uppercase q-mb-xs">
              Quantity ({{
                addItemModal.unitType === 'SACK'
                  ? getBulkUnitLabel(addItemModal.product) + 's'
                  : getRetailUnitLabel(addItemModal.product) + 's'
              }})
            </div>
            <div class="row items-center q-gutter-x-sm">
              <q-btn
                round
                unelevated
                color="slate-200"
                text-color="slate-900"
                icon="remove"
                @click="stepModalQty(-1)"
              />
              <div class="col">
                <q-input
                  v-model.number="addItemModal.quantity"
                  type="number"
                  step="0.05"
                  min="0.01"
                  outlined
                  dense
                  input-class="text-center text-h6 text-weight-bold num-tabular"
                />
              </div>
              <q-btn
                round
                unelevated
                color="slate-200"
                text-color="slate-900"
                icon="add"
                @click="stepModalQty(1)"
              />
            </div>

            <!-- Quick Increment Buttons: Large 2 Columns × 2 Rows -->
            <div class="q-mt-sm">
              <div class="row q-col-gutter-sm">
                <div class="col-6" v-for="n in [1, 2, 5, 10]" :key="n">
                  <q-btn
                    unelevated
                    class="full-width quick-qty-btn"
                    :label="'+' + n"
                    @click="stepModalQty(n)"
                  />
                </div>
              </div>
            </div>

            <!-- Quick Budget Shortcuts in Weight Mode too! -->
            <div
              v-if="addItemModal.unitType === 'KILO'"
              class="row items-center justify-between q-mt-sm q-px-xs"
            >
              <span class="text-caption text-slate-500" style="font-size: 0.72rem"
                >Customer has a budget?</span
              >
              <div class="row q-gutter-x-xs">
                <q-btn
                  v-for="bAmt in [20, 50, 100, 200]"
                  :key="bAmt"
                  flat
                  dense
                  size="sm"
                  class="bg-emerald-50 text-primary text-weight-bold q-px-sm"
                  style="border-radius: 6px; font-size: 0.75rem"
                  :label="`₱${bAmt}`"
                  @click="setBudgetPreset(bAmt)"
                />
              </div>
            </div>
          </div>

          <!-- Subtotal Summary -->
          <div
            class="bg-slate-50 border-slate rounded-borders q-pa-sm row justify-between items-center"
          >
            <span class="text-slate-600 text-caption text-weight-bold">Subtotal:</span>
            <div class="text-right">
              <span class="text-h6 text-weight-bold text-slate-900 num-tabular"
                >₱{{ calculatedModalSubtotal.toFixed(2) }}</span
              >
              <span
                v-if="addItemModal.pricingMode === 'BUDGET' && addItemModal.unitType === 'KILO'"
                class="text-caption text-slate-500 q-ml-xs"
              >
                ({{ (parseFloat(addItemModal.quantity) || 0).toFixed(2) }}
                {{ getRetailUnitLabel(addItemModal.product) }})
              </span>
            </div>
          </div>
        </q-card-section>

        <q-card-actions align="between" class="q-px-md q-py-sm border-top-subtle">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            class="btn-agrivet-green q-px-md"
            :label="'Add to Order • ₱' + calculatedModalSubtotal.toFixed(2)"
            @click="confirmAddToCart"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Dedicated GCash (Cash In / Out) & Other Items Calculator Modal -->
    <q-dialog v-model="serviceModal.open">
      <q-card style="width: 480px; max-width: 95vw" class="rounded-borders-lg border-slate">
        <!-- Header with Type Selector -->
        <q-card-section class="q-pb-none">
          <div class="row items-center justify-between q-mb-sm">
            <div class="row items-center no-wrap">
              <div
                class="product-icon-squircle q-mr-sm"
                :class="
                  serviceModal.type === 'OTHER'
                    ? 'bg-purple-1 text-purple-9'
                    : 'bg-blue-1 text-blue-9'
                "
                style="width: 36px; height: 36px; border-radius: 10px"
              >
                <span>{{ serviceModal.type === 'OTHER' ? '🏷️' : '📱' }}</span>
              </div>
              <div class="text-subtitle1 text-weight-bolder text-slate-900">
                {{ serviceModal.type === 'OTHER' ? 'Custom / Other Item' : 'GCash Cash In & Out' }}
              </div>
            </div>
            <q-btn flat round dense icon="close" v-close-popup />
          </div>

          <!-- Mode Selector Tabs: [Cash In] [Cash Out] [Other Item] -->
          <q-btn-toggle
            v-model="serviceModal.type"
            spread
            no-caps
            dense
            rounded
            unelevated
            toggle-color="primary"
            color="slate-100"
            text-color="slate-7"
            class="border-slate text-weight-bold text-caption q-mb-md"
            :options="[
              { label: 'Cash In', value: 'GCASH_IN', icon: 'arrow_downward' },
              { label: 'Cash Out', value: 'GCASH_OUT', icon: 'arrow_upward' },
              { label: 'Other Item', value: 'OTHER', icon: 'shopping_bag' },
            ]"
          />
        </q-card-section>

        <q-card-section class="q-pt-none q-gutter-y-sm">
          <!-- A. If GCash (Cash In or Cash Out) -->
          <div v-if="serviceModal.type === 'GCASH_IN' || serviceModal.type === 'GCASH_OUT'">
            <!-- Service Info Banner -->
            <div
              class="q-pa-sm rounded-borders text-caption text-weight-medium q-mb-sm row items-center"
              :class="
                serviceModal.type === 'GCASH_IN'
                  ? 'bg-blue-50 text-blue-9'
                  : 'bg-teal-50 text-teal-9'
              "
            >
              <q-icon
                :name="serviceModal.type === 'GCASH_IN' ? 'south_east' : 'north_west'"
                size="18px"
                class="q-mr-xs"
              />
              <span>
                {{
                  serviceModal.type === 'GCASH_IN'
                    ? 'Cash In: Customer hands you physical cash; you send GCash + fee.'
                    : 'Cash Out: Customer transfers GCash to store; you dispense physical cash.'
                }}
              </span>
            </div>

            <!-- Reference / Customer Phone # (Optional) -->
            <q-input
              v-model="serviceModal.referenceNumber"
              outlined
              dense
              label="Customer Mobile / Reference No. (Optional)"
              placeholder="e.g. 0917-123-4567 or Ref #8921"
              class="q-mb-sm"
            >
              <template v-slot:prepend>
                <q-icon name="smartphone" color="slate-400" size="18px" />
              </template>
            </q-input>

            <!-- 1. Principal Amount Input -->
            <div class="q-mb-sm">
              <div class="text-caption text-weight-bold text-slate-700 q-mb-xs">
                Principal Amount (₱) *
              </div>
              <q-input
                v-model.number="serviceModal.amount"
                type="number"
                outlined
                dense
                placeholder="0.00"
                prefix="₱"
                class="text-weight-bold text-subtitle1"
                autofocus
                @update:model-value="autoSuggestFee"
              />
              <!-- Quick Amount Presets: Full-Width 6-Column Grid -->
              <div class="row q-col-gutter-xs q-mt-xs">
                <div v-for="amt in [200, 500, 1000, 2000, 3000, 5000]" :key="amt" class="col-2">
                  <q-btn
                    unelevated
                    no-caps
                    dense
                    :label="`₱${amt}`"
                    class="full-width text-weight-bold border-slate text-slate-800 bg-slate-50"
                    style="font-size: 0.76rem; height: 32px; border-radius: 8px"
                    @click="setServiceAmount(amt)"
                  />
                </div>
              </div>
            </div>

            <!-- 2. Charge / Patong Input -->
            <div class="q-mb-sm">
              <div class="row items-center justify-between q-mb-xs">
                <span class="text-caption text-weight-bold text-slate-700"
                  >Charge / Patong (Fee ₱) *</span
                >
                <span class="text-caption text-slate-400" style="font-size: 0.72rem"
                  >Store service fee / profit</span
                >
              </div>
              <q-input
                v-model.number="serviceModal.charge"
                type="number"
                outlined
                dense
                placeholder="0.00"
                prefix="₱"
                class="text-weight-bold text-subtitle1"
              />
              <!-- Quick Fee Presets: Full-Width 6-Column Grid -->
              <div class="row q-col-gutter-xs q-mt-xs">
                <div v-for="fee in [10, 15, 20, 25, 30, 50]" :key="fee" class="col-2">
                  <q-btn
                    unelevated
                    no-caps
                    dense
                    :label="`+₱${fee}`"
                    class="full-width text-weight-bold border-slate text-emerald-8 bg-emerald-50"
                    style="font-size: 0.76rem; height: 32px; border-radius: 8px"
                    @click="serviceModal.charge = fee"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- B. If Other / Custom Item -->
          <div v-else>
            <!-- Item Name / Description -->
            <div class="q-mb-sm">
              <div class="text-caption text-weight-bold text-slate-700 q-mb-xs">
                Item Description / Name *
              </div>
              <q-input
                v-model="serviceModal.description"
                outlined
                dense
                placeholder="e.g. Empty Sack, Egg Tray, Delivery Fee, Miscellaneous"
                autofocus
              >
                <template v-slot:prepend>
                  <q-icon name="edit_note" color="slate-400" size="20px" />
                </template>
              </q-input>
              <!-- Quick description chips -->
              <div class="row q-gutter-xs q-mt-xs">
                <q-btn
                  v-for="sug in [
                    'Empty Sack',
                    'Egg Tray',
                    'Delivery / Transport',
                    'Repair Service',
                    'Custom Merchandise',
                  ]"
                  :key="sug"
                  dense
                  outline
                  size="xs"
                  no-caps
                  :label="sug"
                  class="text-slate-700 bg-white"
                  @click="serviceModal.description = sug"
                />
              </div>
            </div>

            <!-- Base Amount / Price -->
            <div class="q-mb-sm">
              <div class="text-caption text-weight-bold text-slate-700 q-mb-xs">
                Base Amount / Price (₱) *
              </div>
              <q-input
                v-model.number="serviceModal.amount"
                type="number"
                outlined
                dense
                placeholder="0.00"
                prefix="₱"
                class="text-weight-bold text-subtitle1"
              />
            </div>

            <!-- Additional Charge / Patong (Optional) -->
            <div class="q-mb-sm">
              <div class="text-caption text-weight-bold text-slate-700 q-mb-xs">
                Additional Charge / Patong (₱, Optional)
              </div>
              <q-input
                v-model.number="serviceModal.charge"
                type="number"
                outlined
                dense
                placeholder="0.00"
                prefix="₱"
              />
            </div>
          </div>

          <!-- C. LIVE CALCULATION BOX (Amount + Charge = Total Sales!) -->
          <div class="bg-slate-50 border-slate rounded-borders q-pa-md q-mt-md">
            <div class="row justify-between items-center text-caption text-slate-500 q-mb-xs">
              <span>Amount:</span>
              <span class="text-weight-bold text-slate-800 num-tabular">
                ₱{{ (parseFloat(serviceModal.amount) || 0).toFixed(2) }}
              </span>
            </div>
            <div class="row justify-between items-center text-caption text-slate-500 q-mb-xs">
              <span>Charge / Patong:</span>
              <span class="text-weight-bold text-emerald-7 num-tabular">
                + ₱{{ (parseFloat(serviceModal.charge) || 0).toFixed(2) }}
              </span>
            </div>
            <q-separator class="q-my-xs" />
            <div class="row justify-between items-center q-pt-xs">
              <span class="text-subtitle2 text-weight-bolder text-slate-900">TOTAL LINE SALE:</span>
              <span class="text-h6 text-weight-bolder text-primary num-tabular">
                ₱{{
                  (
                    (parseFloat(serviceModal.amount) || 0) + (parseFloat(serviceModal.charge) || 0)
                  ).toLocaleString('en-US', {
                    minimumFractionDigits: 2,
                    maximumFractionDigits: 2,
                  })
                }}
              </span>
            </div>
          </div>
        </q-card-section>

        <!-- Actions -->
        <q-card-actions align="between" class="q-px-md q-pb-md border-top-subtle">
          <q-btn flat label="Cancel" color="slate-6" v-close-popup />
          <q-btn
            unelevated
            no-caps
            class="btn-agrivet-green q-px-lg text-weight-bold"
            :label="`Add to Order (₱${((parseFloat(serviceModal.amount) || 0) + (parseFloat(serviceModal.charge) || 0)).toFixed(2)})`"
            :disable="(parseFloat(serviceModal.amount) || 0) <= 0"
            @click="confirmAddServiceItem"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Customer Switch Dialog -->
    <q-dialog v-model="showCustomerPicker">
      <q-card style="width: 440px; max-width: 92vw">
        <q-card-section class="row items-center justify-between q-pb-none">
          <div class="text-subtitle1 text-weight-bold text-slate-900">Select Customer / Farm</div>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>
        <q-card-section class="q-pa-md">
          <!-- Add New Customer -->
          <q-btn
            unelevated
            class="btn-agrivet-green full-width q-mb-md"
            icon="person_add"
            label="+ Add New Customer"
            @click="openAddCustomerModal"
          />

          <!-- Existing customer dropdown -->
          <q-select
            v-model="selectedCustomer"
            :options="customerOptions"
            option-label="name"
            option-value="id"
            label="Search Registered Farm / Buyer"
            outlined
            dense
            use-input
            clearable
            input-debounce="0"
            class="q-mb-md"
            @filter="filterCustomers"
            @update:model-value="showCustomerPicker = false"
          >
            <template v-slot:option="scope">
              <q-item v-bind="scope.itemProps">
                <q-item-section>
                  <q-item-label class="text-weight-bold">{{ scope.opt.name }}</q-item-label>
                  <q-item-label caption v-if="scope.opt.contact_number"
                    >📞 {{ scope.opt.contact_number }}</q-item-label
                  >
                </q-item-section>
                <q-item-section side v-if="parseFloat(scope.opt.total_utang || 0) > 0">
                  <q-badge
                    color="negative"
                    :label="'₱' + parseFloat(scope.opt.total_utang).toFixed(2) + ' utang'"
                  />
                </q-item-section>
              </q-item>
            </template>
            <template v-slot:no-option>
              <q-item>
                <q-item-section class="text-grey text-caption">No customers found</q-item-section>
              </q-item>
            </template>
          </q-select>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Add New Customer Modal -->
    <q-dialog v-model="addCustomerModal.open">
      <q-card style="width: 420px; max-width: 92vw">
        <q-card-section class="row items-center justify-between q-pb-none">
          <div class="text-subtitle1 text-weight-bold text-slate-900">Add New Customer</div>
          <q-btn flat round dense icon="close" v-close-popup />
        </q-card-section>
        <q-card-section class="q-pa-md q-gutter-y-sm">
          <q-input
            v-model="addCustomerModal.name"
            label="Customer / Farm Name *"
            outlined
            dense
            autofocus
          />
          <q-input
            v-model="addCustomerModal.contact_number"
            label="Contact Number"
            outlined
            dense
            type="tel"
          />
          <q-input
            v-model="addCustomerModal.notes"
            label="Notes (optional)"
            outlined
            dense
            type="textarea"
            rows="2"
          />
        </q-card-section>
        <q-card-actions align="between" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            unelevated
            class="btn-agrivet-green q-px-lg"
            label="Save & Select"
            :loading="addCustomerModal.saving"
            :disable="!addCustomerModal.name.trim()"
            @click="saveNewCustomer"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- ===== CASH TENDERED / CASHIER MODAL (2-COLUMN SIDE-BY-SIDE) ===== -->
    <q-dialog v-model="cashModal.open" persistent>
      <q-card style="width: 760px; max-width: 96vw; border-radius: 16px; overflow: hidden">
        <!-- Header -->
        <q-card-section
          class="row items-center justify-between bg-slate-50 q-py-sm q-px-md border-bottom-subtle"
        >
          <div class="row items-center">
            <div
              class="shift-icon-wrap row items-center justify-center q-mr-sm"
              style="width: 32px; height: 32px; background-color: #e6f4ea; border-radius: 8px"
            >
              <q-icon name="payments" size="20px" color="primary" />
            </div>
            <div>
              <div class="text-subtitle1 text-weight-bolder text-slate-900 leading-none">
                Cash Payment & Change
              </div>
              <div class="text-caption text-slate-500" style="font-size: 0.7rem">
                Fast cash checkout with real-time change calculation
              </div>
            </div>
          </div>
          <q-btn flat round dense icon="close" color="grey-7" @click="cashModal.open = false" />
        </q-card-section>

        <!-- Body: 2 Columns Side-by-Side -->
        <q-card-section class="q-pa-md">
          <div class="row q-col-gutter-md items-stretch">
            <!-- LEFT COLUMN: Tendered Display + Presets + Numpad -->
            <div class="col-12 col-sm-6 column justify-between">
              <div>
                <!-- Amount Tendered Display -->
                <div class="q-mb-sm">
                  <div class="row items-center justify-between q-mb-xs">
                    <span
                      class="text-caption text-slate-600 text-uppercase text-weight-bold"
                      style="font-size: 0.68rem; letter-spacing: 0.04em"
                    >
                      Amount Tendered
                    </span>
                    <span
                      v-if="cashModal.rawValue"
                      class="text-caption text-primary text-weight-bold"
                      style="font-size: 0.72rem"
                    >
                      ₱{{
                        parseFloat(cashModal.rawValue || 0).toLocaleString('en-US', {
                          minimumFractionDigits: 2,
                          maximumFractionDigits: 2,
                        })
                      }}
                    </span>
                  </div>
                  <div
                    class="rounded-borders border-slate bg-slate-50 q-px-md q-py-xs text-right num-tabular text-h4 text-weight-bold text-slate-900"
                    style="min-height: 52px; line-height: 52px"
                  >
                    {{ cashModal.displayValue || '0' }}
                  </div>
                </div>

                <!-- Quick Preset Amounts -->
                <div class="row q-col-gutter-xs q-mb-sm">
                  <div class="col-3" v-for="amt in cashModal.presets" :key="amt">
                    <q-btn
                      unelevated
                      class="full-width bg-slate-100 text-slate-800 text-weight-bold"
                      style="height: 38px; font-size: 0.82rem; border-radius: 8px"
                      no-caps
                      @click="setCashPreset(amt)"
                    >
                      ₱{{ amt.toLocaleString() }}
                    </q-btn>
                  </div>
                </div>

                <!-- Numpad -->
                <div class="numpad-grid">
                  <q-btn
                    v-for="key in ['7', '8', '9', '4', '5', '6', '1', '2', '3', '000', '0', '⌫']"
                    :key="key"
                    unelevated
                    class="numpad-key bg-white border-slate text-slate-900 text-weight-bold"
                    :class="key === '⌫' ? 'text-negative' : ''"
                    no-caps
                    @click="numpadPress(key)"
                  >
                    {{ key }}
                  </q-btn>
                </div>
              </div>
            </div>

            <!-- RIGHT COLUMN (Second Picture): Total Due, Exact Amount, Change Due, Action Buttons -->
            <div class="col-12 col-sm-6 column justify-between">
              <div>
                <!-- Total Due Card -->
                <div class="rounded-borders border-slate bg-slate-50 q-pa-sm q-mb-sm text-center">
                  <div
                    class="text-caption text-slate-400 text-uppercase text-weight-bold"
                    style="font-size: 0.65rem; letter-spacing: 0.05em"
                  >
                    TOTAL DUE
                  </div>
                  <div class="text-h4 text-weight-bolder text-slate-900 num-tabular">
                    ₱{{
                      totalDueAmount.toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })
                    }}
                  </div>
                </div>

                <!-- Exact Amount shortcut button -->
                <q-btn
                  outline
                  color="primary"
                  label="Exact Amount"
                  icon="check_circle"
                  class="full-width q-mb-sm bg-white"
                  style="height: 42px; font-weight: 700; border-radius: 8px"
                  no-caps
                  @click="setCashExact"
                />

                <!-- Change Due Box -->
                <div
                  class="rounded-borders q-pa-md text-center border-slate"
                  :class="cashModal.changeDue >= 0 ? 'bg-emerald-50' : 'bg-red-50'"
                  style="
                    min-height: 104px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                  "
                >
                  <div
                    class="text-caption text-slate-500 text-uppercase text-weight-bold q-mb-xs"
                    style="font-size: 0.68rem; letter-spacing: 0.05em"
                  >
                    CHANGE DUE
                  </div>
                  <div
                    class="text-h3 text-weight-bolder num-tabular leading-tight"
                    :class="cashModal.changeDue >= 0 ? 'text-primary' : 'text-negative'"
                  >
                    ₱{{
                      Math.max(0, cashModal.changeDue).toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })
                    }}
                  </div>
                  <div
                    v-if="cashModal.changeDue < 0"
                    class="text-caption text-negative text-weight-bold q-mt-xs"
                  >
                    ₱{{
                      Math.abs(cashModal.changeDue).toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })
                    }}
                    short
                  </div>
                </div>
              </div>

              <!-- Bottom Actions Row inside Right Column -->
              <div class="q-pt-sm">
                <div class="row q-col-gutter-sm items-center">
                  <div class="col-4">
                    <q-btn
                      flat
                      label="Cancel"
                      color="grey-7"
                      class="full-width"
                      style="height: 48px; border-radius: 8px"
                      @click="cashModal.open = false"
                    />
                  </div>
                  <div class="col-8">
                    <q-btn
                      unelevated
                      class="btn-agrivet-green full-width"
                      icon="receipt_long"
                      label="Confirm & Print"
                      style="height: 48px; font-weight: 700; border-radius: 8px"
                      :disable="parseFloat(cashModal.rawValue || 0) < totalDueAmount"
                      :loading="cashModal.submitting"
                      @click="confirmCashPayment"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Official Receipt Modal (Side-by-Side 2-Column Layout) -->
    <q-dialog v-model="receiptDialog.open" persistent>
      <q-card style="width: 760px; max-width: 96vw; border-radius: 16px; overflow: hidden">
        <!-- Modal Top Bar -->
        <q-card-section
          class="row items-center justify-between bg-slate-50 q-py-sm q-px-md border-bottom-subtle no-print"
        >
          <div class="row items-center">
            <div
              class="shift-icon-wrap row items-center justify-center q-mr-sm"
              style="width: 32px; height: 32px; background-color: #e6f4ea; border-radius: 8px"
            >
              <q-icon name="receipt_long" size="20px" color="primary" />
            </div>
            <div>
              <div class="text-subtitle1 text-weight-bolder text-slate-900 leading-none">
                Official Receipt Preview
              </div>
              <div class="text-caption text-slate-500" style="font-size: 0.7rem">
                Order #TX-{{ receiptDialog.tx.id }}
              </div>
            </div>
          </div>
          <q-btn flat round dense icon="close" color="grey-7" v-close-popup />
        </q-card-section>

        <!-- Body: 2 Columns Side-by-Side -->
        <q-card-section class="q-pa-md">
          <div class="row q-col-gutter-md items-stretch">
            <!-- LEFT COLUMN: The Printable Receipt Slip -->
            <div class="col-12 col-sm-7">
              <div
                class="rounded-borders border-slate bg-slate-50 q-pa-sm"
                style="max-height: 65vh; overflow-y: auto"
              >
                <!-- The Clean Printable Slip (#pos-receipt-slip) -->
                <div
                  id="pos-receipt-slip"
                  class="receipt-paper-slip bg-white q-pa-md border-slate rounded-borders"
                >
                  <!-- Store Header with Logo -->
                  <div class="text-center q-mb-xs">
                    <img :src="logoUrl" alt="Nichole Agrivet Mascot" class="receipt-logo q-mb-xs" />
                    <div class="receipt-store-title text-slate-900 text-weight-bolder">
                      NICHOLE AGRIVET
                    </div>
                    <div class="receipt-store-subtitle text-slate-600 text-weight-medium">
                      Agricultural & Veterinary Supplies
                    </div>
                    <div
                      class="text-caption text-slate-500 font-tabular"
                      style="font-size: 0.72rem"
                    >
                      VillaReal, Samar
                    </div>
                  </div>

                  <div class="receipt-dashed-line"></div>

                  <!-- Receipt Meta Info -->
                  <div class="row justify-between text-caption q-mb-xs">
                    <span class="text-slate-500">Receipt No:</span>
                    <span class="text-weight-bold text-slate-900 num-tabular"
                      >#TX-{{ receiptDialog.tx.id }}</span
                    >
                  </div>
                  <div class="row justify-between text-caption q-mb-xs">
                    <span class="text-slate-500">Date & Time:</span>
                    <span class="text-weight-bold text-slate-900">{{
                      formatReceiptDate(receiptDialog.tx.created_at)
                    }}</span>
                  </div>
                  <div class="row justify-between text-caption q-mb-xs">
                    <span class="text-slate-500">Cashier:</span>
                    <span class="text-weight-bold text-slate-900">{{ userName }}</span>
                  </div>
                  <div class="row justify-between text-caption q-mb-xs">
                    <span class="text-slate-500">Customer:</span>
                    <span class="text-weight-bold text-slate-900">{{
                      receiptDialog.tx.customer_name || 'Walk-in Customer'
                    }}</span>
                  </div>
                  <div class="row justify-between text-caption q-mb-xs">
                    <span class="text-slate-500">Payment:</span>
                    <span class="text-weight-bold text-primary">{{
                      receiptDialog.tx.transaction_type
                    }}</span>
                  </div>

                  <div class="receipt-dashed-line"></div>

                  <!-- Itemized Table Header -->
                  <div
                    class="row text-caption text-weight-bolder text-slate-700 text-uppercase q-pb-xs"
                  >
                    <div class="col-7">Item Description</div>
                    <div class="col-2 text-center">Qty</div>
                    <div class="col-3 text-right">Amount</div>
                  </div>

                  <!-- Items Purchased List -->
                  <div class="q-gutter-y-xs">
                    <div
                      v-for="item in receiptDialog.items"
                      :key="item.id || item.product_name"
                      class="text-caption"
                    >
                      <div class="text-weight-bold text-slate-900 leading-tight">
                        {{ item.product_name }}
                      </div>
                      <div
                        v-if="item.notes || item.feeDetails"
                        class="text-caption text-primary font-medium"
                        style="font-size: 0.72rem"
                      >
                        {{ item.notes || item.feeDetails }}
                      </div>
                      <div
                        class="row justify-between text-slate-500 text-caption num-tabular"
                        style="font-size: 0.73rem"
                      >
                        <span
                          >{{ item.quantity }} {{ item.unit_type || 'pc' }} @ ₱{{
                            parseFloat(item.unit_price).toFixed(2)
                          }}</span
                        >
                        <span class="text-weight-bold text-slate-900"
                          >₱{{ parseFloat(item.subtotal).toFixed(2) }}</span
                        >
                      </div>
                    </div>
                  </div>

                  <div class="receipt-dashed-line"></div>

                  <!-- Financial Totals -->
                  <div class="row justify-between text-body2 q-mb-xs">
                    <span class="text-slate-600">Subtotal:</span>
                    <span class="text-weight-medium text-slate-900 num-tabular"
                      >₱{{ parseFloat(receiptDialog.tx.total_amount || 0).toFixed(2) }}</span
                    >
                  </div>
                  <div class="row justify-between items-center text-subtitle1 q-mb-xs">
                    <span class="text-weight-bolder text-slate-900 text-uppercase">TOTAL DUE:</span>
                    <span class="text-h6 text-weight-bolder text-slate-900 num-tabular"
                      >₱{{ parseFloat(receiptDialog.tx.total_amount || 0).toFixed(2) }}</span
                    >
                  </div>

                  <template v-if="receiptDialog.tx.transaction_type === 'CASH'">
                    <div class="row justify-between text-body2 q-mb-xs">
                      <span class="text-slate-600">Amount Tendered:</span>
                      <span class="text-weight-bold text-slate-900 num-tabular"
                        >₱{{ parseFloat(receiptDialog.tx.amount_paid || 0).toFixed(2) }}</span
                      >
                    </div>
                    <div
                      class="row justify-between text-subtitle1 q-mt-xs bg-slate-50 q-pa-xs rounded-borders"
                    >
                      <span class="text-weight-bolder text-slate-900">CHANGE DUE:</span>
                      <span class="text-weight-bolder text-primary num-tabular text-h6"
                        >₱{{ parseFloat(receiptDialog.tx.change_given || 0).toFixed(2) }}</span
                      >
                    </div>
                  </template>

                  <template v-else-if="receiptDialog.tx.transaction_type === 'CREDIT'">
                    <div class="row justify-between text-body2 q-mt-xs text-negative">
                      <span class="text-weight-bold">Added to Utang:</span>
                      <span class="text-weight-bolder num-tabular"
                        >₱{{ parseFloat(receiptDialog.tx.total_amount || 0).toFixed(2) }}</span
                      >
                    </div>
                  </template>

                  <template v-else-if="receiptDialog.tx.transaction_type === 'GCASH'">
                    <div class="row justify-between text-body2 q-mt-xs text-indigo-8">
                      <span class="text-weight-bold">Paid via GCash:</span>
                      <span class="text-weight-bolder num-tabular"
                        >₱{{ parseFloat(receiptDialog.tx.total_amount || 0).toFixed(2) }}</span
                      >
                    </div>
                  </template>

                  <div class="receipt-dashed-line"></div>

                  <!-- Footer Message -->
                  <div
                    class="text-center text-caption text-slate-500 q-pt-xs leading-tight"
                    style="font-size: 0.72rem"
                  >
                    <div class="text-weight-bold text-slate-700">
                      Thank you for trusting Nichole Agrivet!
                    </div>
                    <div>Quality Feeds • Quality Care for Your Animals</div>
                    <div class="text-slate-400 q-mt-xs" style="font-size: 0.65rem">
                      *** Official Sales Invoice ***
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- RIGHT COLUMN: Payment Success, Paper Size Toggle & Actions on the Side -->
            <div class="col-12 col-sm-5 column justify-between no-print">
              <div>
                <!-- Success Header -->
                <div class="rounded-borders border-slate bg-emerald-50 q-pa-md text-center q-mb-md">
                  <div
                    class="badge-mint q-mx-auto q-mb-xs"
                    style="
                      width: 44px;
                      height: 44px;
                      border-radius: 50%;
                      display: flex;
                      align-items: center;
                      justify-content: center;
                      background-color: #d1fae5;
                    "
                  >
                    <q-icon name="check" size="24px" color="primary" />
                  </div>
                  <div class="text-subtitle1 text-weight-bolder text-slate-900 leading-tight">
                    Payment Successful!
                  </div>
                  <div class="text-caption text-slate-500 q-mt-xs">
                    Order #TX-{{ receiptDialog.tx.id }}
                  </div>
                  <div class="text-h5 text-weight-bolder text-primary num-tabular q-mt-xs">
                    ₱{{
                      parseFloat(receiptDialog.tx.total_amount || 0).toLocaleString('en-US', {
                        minimumFractionDigits: 2,
                        maximumFractionDigits: 2,
                      })
                    }}
                  </div>
                </div>

                <!-- Paper Size Selector -->
                <div class="rounded-borders border-slate bg-slate-50 q-pa-sm q-mb-md">
                  <div
                    class="text-caption text-slate-600 text-weight-bold q-mb-xs"
                    style="font-size: 0.68rem; letter-spacing: 0.04em"
                  >
                    THERMAL PAPER SIZE
                  </div>
                  <q-btn-toggle
                    v-model="receiptPaperSize"
                    dense
                    rounded
                    unelevated
                    spread
                    toggle-color="primary"
                    color="white"
                    text-color="slate-7"
                    class="border-slate full-width"
                    size="sm"
                    @update:model-value="(val) => localStorage.setItem('receiptPaperSize', val)"
                    :options="[
                      { label: '80mm (Standard)', value: '80mm' },
                      { label: '58mm (Handheld)', value: '58mm' },
                    ]"
                  />
                </div>
              </div>

              <!-- Action Buttons on the Side -->
              <div class="q-gutter-y-sm q-pt-sm">
                <q-btn
                  unelevated
                  icon="print"
                  :label="'Print Receipt (' + receiptPaperSize + ')'"
                  class="btn-agrivet-green full-width"
                  style="height: 50px; font-weight: 700; border-radius: 8px; font-size: 0.95rem"
                  @click="printReceipt"
                />
                <q-btn
                  flat
                  label="Close & Next Sale"
                  color="grey-7"
                  class="full-width"
                  style="height: 42px; border-radius: 8px"
                  v-close-popup
                />
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Shift Z-Reading & Cash Balancing Modal -->
    <ShiftZReadingModal ref="zReadingModalRef" />

    <!-- Agrivet Quick Calculator Modal -->
    <QuickCalculatorModal ref="calculatorModalRef" />
  </q-page>
</template>

<script setup>
import { ref, onMounted, computed, inject } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
import logoUrl from 'src/images/Nichole Agrivet.png'
import TopHeaderControls from 'src/components/TopHeaderControls.vue'
import ShiftZReadingModal from 'src/components/ShiftZReadingModal.vue'
import QuickCalculatorModal from 'src/components/QuickCalculatorModal.vue'
import { playBeep, playChime, playWarning } from 'src/utils/audio'

const $q = useQuasar()
const toggleDrawer = inject('toggleDrawer', () => {})
const zReadingModalRef = ref(null)
const calculatorModalRef = ref(null)

function openShiftZReading() {
  if (zReadingModalRef.value) {
    zReadingModalRef.value.openModal()
  }
}

function openCalculator() {
  if (calculatorModalRef.value) {
    calculatorModalRef.value.openModal()
  }
}

function formatReceiptDate(dateStr) {
  if (!dateStr)
    return new Date().toLocaleString('en-PH', { dateStyle: 'medium', timeStyle: 'short' })
  const d = new Date(dateStr)
  return d.toLocaleString('en-PH', { dateStyle: 'medium', timeStyle: 'short' })
}

// State lists
const products = ref([])
const customers = ref([])
const categories = ref([])

// Filters
const searchQuery = ref('')
const selectedCategory = ref(null) // null means "All"
const todayShiftTotal = ref(0.0)

// Active Cart & Customer
const cart = ref([])
const selectedCustomer = ref(null)
const paymentMethod = ref('CASH')
const cashTendered = ref(null)

const userName = ref(localStorage.getItem('userName') || 'admin')

// Dialog states
const showCustomerPicker = ref(false)
const receiptDialog = ref({ open: false, tx: {}, items: [] })
const receiptPaperSize = ref(localStorage.getItem('receiptPaperSize') || '80mm')
const addItemModal = ref({
  open: false,
  product: null,
  unitType: 'KILO',
  quantity: 1,
  pricingMode: 'WEIGHT',
  budgetAmount: null,
})
const addCustomerModal = ref({
  open: false,
  name: '',
  contact_number: '',
  notes: '',
  saving: false,
})
const cashModal = ref({
  open: false,
  rawValue: '',
  displayValue: '',
  presets: [],
  changeDue: 0,
  submitting: false,
})

// GCash & Other Service Items Modal State
const serviceModal = ref({
  open: false,
  type: 'GCASH_IN', // 'GCASH_IN', 'GCASH_OUT', 'OTHER'
  amount: null,
  charge: null,
  description: '',
  referenceNumber: '',
  product: null,
})

function openServiceModal(type = 'GCASH_IN', product = null) {
  serviceModal.value = {
    open: true,
    type,
    amount: null,
    charge: null,
    description: '',
    referenceNumber: '',
    product:
      product ||
      (type === 'OTHER'
        ? products.value.find((p) => p.name.includes('Other') || p.name.includes('Custom')) ||
          products.value[0]
        : products.value.find((p) => p.name.includes('GCash')) || products.value[0]),
  }
}

function setServiceAmount(amt) {
  serviceModal.value.amount = amt
  autoSuggestFee(amt)
}

function autoSuggestFee(val) {
  if (serviceModal.value.type === 'OTHER') return
  const amt = parseFloat(val) || 0
  if (amt <= 0) return
  if (!serviceModal.value.charge || serviceModal.value.charge === 0) {
    if (amt <= 500) serviceModal.value.charge = 15
    else if (amt <= 1000) serviceModal.value.charge = 20
    else if (amt <= 2000) serviceModal.value.charge = 35
    else if (amt <= 3000) serviceModal.value.charge = 50
    else serviceModal.value.charge = Math.ceil(amt / 1000) * 15
  }
}

function confirmAddServiceItem() {
  const amt = parseFloat(serviceModal.value.amount) || 0
  const chg = parseFloat(serviceModal.value.charge) || 0
  if (amt <= 0) {
    $q.notify({
      color: 'warning',
      message: 'Please enter a valid amount greater than 0.',
      icon: 'warning',
      position: 'top',
    })
    return
  }

  const totalSale = amt + chg
  const type = serviceModal.value.type

  let customTitle = ''
  let feeLabel = ''
  let unitLabel = 'Transaction'

  if (type === 'GCASH_IN') {
    const ref = (serviceModal.value.referenceNumber || '').trim()
    customTitle = ref ? `GCash Cash In (${ref})` : 'GCash Cash In'
    feeLabel = `Amount: ₱${amt.toLocaleString('en-US', { minimumFractionDigits: 2 })} • Fee: ₱${chg.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
  } else if (type === 'GCASH_OUT') {
    const ref = (serviceModal.value.referenceNumber || '').trim()
    customTitle = ref ? `GCash Cash Out (${ref})` : 'GCash Cash Out'
    feeLabel = `Amount: ₱${amt.toLocaleString('en-US', { minimumFractionDigits: 2 })} • Fee: ₱${chg.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
  } else {
    const desc = (serviceModal.value.description || '').trim() || 'Custom Item'
    customTitle = desc
    feeLabel =
      chg > 0
        ? `Price: ₱${amt.toLocaleString('en-US', { minimumFractionDigits: 2 })} • Fee: ₱${chg.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
        : `Amount: ₱${amt.toLocaleString('en-US', { minimumFractionDigits: 2 })}`
    unitLabel = 'Item'
  }

  let targetProduct = serviceModal.value.product
  if (!targetProduct) {
    if (type === 'OTHER') {
      targetProduct =
        products.value.find((p) => p.name.includes('Other') || p.name.includes('Custom')) ||
        products.value[0]
    } else {
      targetProduct = products.value.find((p) => p.name.includes('GCash')) || products.value[0]
    }
  }

  cart.value.push({
    product: targetProduct,
    customName: customTitle,
    feeDetails: feeLabel,
    unitType: unitLabel,
    quantity: 1,
    price: totalSale,
    isServiceItem: true,
  })

  serviceModal.value.open = false

  $q.notify({
    color: 'primary',
    message: `Added ${customTitle} to ticket (₱${totalSale.toLocaleString('en-US', { minimumFractionDigits: 2 })})`,
    icon: 'add_shopping_cart',
    position: 'top',
    timeout: 1500,
  })
}

// Category mapping with emojis & counts
const categoryPillList = computed(() => {
  return categories.value.map((cat) => {
    const nameLower = cat.name.toLowerCase()
    let emoji = '📦'
    if (nameLower.includes('service') || nameLower.includes('gcash')) emoji = '📱'
    else if (
      nameLower.includes('feed') ||
      nameLower.includes('swine') ||
      nameLower.includes('pig') ||
      nameLower.includes('hog')
    )
      emoji = '🌾'
    else if (
      nameLower.includes('inject') ||
      nameLower.includes('vet') ||
      nameLower.includes('vaccin')
    )
      emoji = '💉'
    else if (nameLower.includes('antibiotic') || nameLower.includes('med')) emoji = '💊'
    else if (nameLower.includes('vit') || nameLower.includes('electrolyt')) emoji = '⚡'
    else if (
      nameLower.includes('disinfect') ||
      nameLower.includes('sanit') ||
      nameLower.includes('clean')
    )
      emoji = '🧴'
    else if (nameLower.includes('rice') || nameLower.includes('bugas')) emoji = '🍚'
    else if (nameLower.includes('pet') || nameLower.includes('dog') || nameLower.includes('cat'))
      emoji = '🐶'

    const count = products.value.filter((p) => p.category === cat.id).length
    return {
      id: cat.id,
      name: cat.name,
      emoji,
      count,
    }
  })
})

function getProductEmoji(product) {
  const cat = (product?.category_name || '').toLowerCase()
  const name = (product?.name || '').toLowerCase()
  if (name.includes('gcash') || cat.includes('gcash') || cat.includes('service')) return '📱'
  if (name.includes('other') || name.includes('custom')) return '🏷️'
  if (cat.includes('feed') || cat.includes('swine') || cat.includes('hog')) return '🌾'
  if (cat.includes('inject') || cat.includes('vaccin')) return '💉'
  if (cat.includes('antibiotic') || cat.includes('powder')) return '💊'
  if (cat.includes('vit') || cat.includes('electrolyt')) return '⚡'
  if (cat.includes('rice') || cat.includes('bugas')) return '🍚'
  if (cat.includes('pet') || cat.includes('dog')) return '🐶'
  return '🧴'
}

function getProductTagClass(product) {
  const cat = (product.category_name || '').toLowerCase()
  const name = (product.name || '').toLowerCase()
  if (name.includes('gcash') || cat.includes('service')) return 'badge-tag-blue'
  if (name.includes('other') || name.includes('custom')) return 'badge-tag-purple'
  if (cat.includes('inject') || name.includes('liquid') || name.includes('100ml'))
    return 'badge-tag-blue'
  if (cat.includes('vit') || name.includes('electro') || name.includes('1kg'))
    return 'badge-tag-purple'
  return 'badge-tag-amber'
}

function getBulkUnitLabel(product) {
  if (!product) return 'Sack'
  const name = product.unit_bulk_name
  if (!name || name === '50kg') return 'Sack'
  return name
}

function getRetailUnitLabel(product) {
  if (!product) return 'Kilo'
  return product.unit_retail_name || 'Kilo'
}

function getProductTagLabel(product) {
  if (!product) return 'Item'
  if (
    product.price_per_sack &&
    (product.unit_bulk_name === 'Sack' ||
      !product.unit_bulk_name ||
      product.unit_bulk_name === '50kg')
  ) {
    return 'Sack'
  }
  if (product.unit_bulk_name) return product.unit_bulk_name
  if (product.unit_retail_name && product.unit_retail_name !== 'Kilo')
    return product.unit_retail_name
  const name = (product.name || '').toLowerCase()
  if (name.includes('vit b12') || name.includes('anti-scour')) return '100ml'
  if (name.includes('vetracin')) return '100g'
  if (name.includes('electro-gen')) return '1kg'
  return product.unit_retail_name || 'Item'
}

function getCategoryBg(product) {
  const cat = (product?.category_name || '').toLowerCase()
  const name = (product?.name || '').toLowerCase()
  if (name.includes('gcash') || cat.includes('gcash') || cat.includes('service')) return '#E0F2FE'
  if (name.includes('other') || name.includes('custom')) return '#F3E8FF'
  if (cat.includes('feed') || name.includes('pellet') || name.includes('hog')) return '#FEF3C7'
  if (cat.includes('inject') || name.includes('dextran') || name.includes('scour')) return '#E0F2FE'
  if (cat.includes('anti') || name.includes('vetracin')) return '#FEF9C3'
  if (cat.includes('vit') || name.includes('electro')) return '#F3E8FF'
  if (cat.includes('rice')) return '#ECFDF5'
  return '#F1F5F9'
}

function getProductTotalBaseStock(product) {
  if (!product) return 0
  const ratio = parseFloat(product.units_per_bulk) || 50
  if (product.unit_bulk_name && product.price_per_sack) {
    return parseFloat(product.stock_sacks || 0) * ratio + parseFloat(product.stock_kilos || 0)
  }
  return parseFloat(product.stock_kilos || 0)
}

function getAvailableStockForUnit(product, unitType, excludeCartItem = null) {
  if (!product) return 0
  const ratio = parseFloat(product.units_per_bulk) || 50
  const totalBase = getProductTotalBaseStock(product)

  // Calculate base units already claimed in cart
  let claimedBase = 0
  for (const item of cart.value) {
    if (item.product.id === product.id && item !== excludeCartItem) {
      if (item.unitType === 'SACK') {
        claimedBase += item.quantity * ratio
      } else {
        claimedBase += item.quantity
      }
    }
  }

  const remainingBase = Math.max(0, totalBase - claimedBase)
  if (unitType === 'SACK') {
    return Math.floor(remainingBase / ratio)
  } else {
    return parseFloat(remainingBase.toFixed(2))
  }
}

function isProductOutOfStock(product) {
  if (!product) return true
  if (
    product.is_service ||
    (product.name && (product.name.includes('GCash') || product.name.includes('Other')))
  ) {
    return false
  }
  const totalBase = getProductTotalBaseStock(product)
  return totalBase <= 0
}

function isProductLowStock(product) {
  if (!product) return false
  if (
    product.is_service ||
    (product.name && (product.name.includes('GCash') || product.name.includes('Other')))
  ) {
    return false
  }
  const totalBase = getProductTotalBaseStock(product)
  if (totalBase <= 0) return false // When 0, it is Out of Stock, not Low!

  const threshold = parseFloat(product.low_stock_threshold || 5)
  if (product.unit_bulk_name && product.price_per_sack) {
    const ratio = parseFloat(product.units_per_bulk) || 50
    const totalBulk = totalBase / ratio
    return totalBulk <= threshold
  }
  return totalBase <= threshold
}

function handleProductCardClick(product) {
  if (
    product.is_service ||
    (product.name && (product.name.includes('GCash') || product.name.includes('Other')))
  ) {
    openServiceModal(product.name && product.name.includes('Other') ? 'OTHER' : 'GCASH_IN', product)
    return
  }
  if (isProductOutOfStock(product)) {
    $q.notify({
      message: `Out of Stock: "${product.name}" has 0 available units in inventory.`,
      color: 'negative',
      icon: 'remove_shopping_cart',
      position: 'top',
      timeout: 2200,
    })
    return
  }
  openAddProductModal(product)
}

function getStockDisplay(product) {
  if (!product) return { qty: 0, unit: 'items', fullText: '0 in stock', badgeText: 'Out of Stock' }
  if (product.is_service || (product.name && product.name.includes('GCash'))) {
    return {
      qty: 'Active',
      unit: 'Service',
      fullText: 'Cash In & Cash Out Service',
      badgeText: '📱 E-Money',
    }
  }
  if (product.is_service || (product.name && product.name.includes('Other'))) {
    return {
      qty: 'Custom',
      unit: 'Item',
      fullText: 'Custom Amount & Service',
      badgeText: '🏷️ Custom Sale',
    }
  }
  const sSacks = parseFloat(product.stock_sacks || 0)
  const sKilos = parseFloat(product.stock_kilos || 0)
  const bulkName = (product.unit_bulk_name || 'sack').toLowerCase()
  const retailName = (product.unit_retail_name || 'kilo').toLowerCase()

  if (product.unit_bulk_name && product.price_per_sack) {
    if (sSacks > 0 && sKilos > 0) {
      const sackUnit = sSacks === 1 ? bulkName : `${bulkName}s`
      const kiloUnit = sKilos === 1 ? retailName : `${retailName}s`
      return {
        qty: `${sSacks} ${sackUnit} & ${sKilos}`,
        unit: kiloUnit,
        fullText: `${sSacks} ${sackUnit} & ${sKilos} ${kiloUnit} in stock`,
        badgeText: `Only ${sSacks} ${sackUnit} & ${sKilos} ${kiloUnit} left`,
      }
    } else if (sSacks > 0) {
      const sackUnit = sSacks === 1 ? bulkName : `${bulkName}s`
      return {
        qty: sSacks,
        unit: sackUnit,
        fullText: `${sSacks} ${sackUnit} in stock`,
        badgeText: `Only ${sSacks} ${sackUnit} left`,
      }
    } else if (sKilos > 0) {
      const kiloUnit = sKilos === 1 ? retailName : `${retailName}s`
      return {
        qty: sKilos,
        unit: kiloUnit,
        fullText: `${sKilos} ${kiloUnit} in stock`,
        badgeText: `Only ${sKilos} ${kiloUnit} left`,
      }
    } else {
      return {
        qty: 0,
        unit: `${bulkName}s`,
        fullText: '0 in stock',
        badgeText: 'Out of Stock',
      }
    }
  }

  const rUnit = (product.unit_retail_name || 'pcs').toLowerCase()
  let unit = 'pcs'
  if (rUnit.includes('vial') || rUnit.includes('100ml')) unit = sKilos === 1 ? 'vial' : 'vials'
  else if (rUnit.includes('pack') || rUnit.includes('1kg')) unit = sKilos === 1 ? 'pack' : 'packs'
  else if (rUnit.includes('sack')) unit = sKilos === 1 ? 'sack' : 'sacks'
  else if (rUnit.includes('kilo')) unit = sKilos === 1 ? 'kilo' : 'kilos'
  else if (rUnit.includes('bottle')) unit = sKilos === 1 ? 'bottle' : 'bottles'
  else if (rUnit.includes('box')) unit = sKilos === 1 ? 'box' : 'boxes'
  else if (rUnit.includes('tablet')) unit = sKilos === 1 ? 'tablet' : 'tablets'
  else unit = sKilos === 1 ? 'pc' : 'pcs'

  return {
    qty: sKilos,
    unit,
    fullText: `${sKilos} ${unit} in stock`,
    badgeText: `Only ${sKilos} ${unit} left`,
  }
}

function quickAddToCart(product, event) {
  if (event) event.stopPropagation()
  if (
    product.is_service ||
    (product.name && (product.name.includes('GCash') || product.name.includes('Other')))
  ) {
    openServiceModal(product.name && product.name.includes('Other') ? 'OTHER' : 'GCASH_IN', product)
    return
  }
  if (isProductOutOfStock(product)) {
    playWarning()
    $q.notify({
      message: `Out of Stock: "${product.name}" has 0 available units.`,
      color: 'negative',
      icon: 'remove_shopping_cart',
      position: 'top',
      timeout: 2200,
    })
    return
  }

  const unitType = parseFloat(product.price_per_kilo || 0) > 0 ? 'KILO' : 'SACK'
  const price = parseFloat(product.price_per_kilo || product.price_per_sack || 0)
  const unitLabel =
    unitType === 'SACK' ? product.unit_bulk_name || 'sack' : product.unit_retail_name || 'kilo'

  const available = getAvailableStockForUnit(product, unitType)

  if (available < 1) {
    playWarning()
    $q.notify({
      message: `Out of Stock: "${product.name}" has no ${unitLabel}s available.`,
      color: 'negative',
      icon: 'block',
      position: 'top',
      timeout: 2000,
    })
    return
  }

  const existing = cart.value.find(
    (item) => item.product.id === product.id && item.unitType === unitType,
  )
  if (existing) {
    existing.quantity += 1
  } else {
    cart.value.push({
      product,
      unitType,
      quantity: 1,
      price,
    })
  }
  playBeep()
  $q.notify({
    message: `Added ${product.name} to order`,
    color: 'primary',
    icon: 'shopping_bag',
    position: 'top',
    timeout: 700,
  })
}

const filteredProducts = computed(() => {
  return products.value.filter((p) => {
    const matchSearch = p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchCat = selectedCategory.value === null || p.category === selectedCategory.value
    return matchSearch && matchCat && p.is_active
  })
})

// Financial Calculations (No discounts currently)
const subtotalAmount = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.quantity * item.price, 0)
})

const totalDueAmount = computed(() => {
  return subtotalAmount.value
})

// ===== CASH TENDERED MODAL FUNCTIONS =====
function openCashTenderedModal() {
  if (cart.value.length === 0) return
  const total = totalDueAmount.value
  // Build smart presets: next round, next 500, next 1000, + total itself
  const nextRound = Math.ceil(total / 100) * 100
  const next500 = Math.ceil(total / 500) * 500
  const next1000 = Math.ceil(total / 1000) * 1000
  const presets = [...new Set([total, nextRound, next500, next1000].filter((v) => v > 0))]
    .sort((a, b) => a - b)
    .slice(0, 4)

  cashModal.value = {
    open: true,
    rawValue: '',
    displayValue: '',
    presets,
    changeDue: -total,
    submitting: false,
  }
}

function updateCashModalChange() {
  const tendered = parseFloat(cashModal.value.rawValue) || 0
  cashModal.value.changeDue = tendered - totalDueAmount.value
}

function numpadPress(key) {
  if (key === '⌫') {
    cashModal.value.rawValue = cashModal.value.rawValue.slice(0, -1)
  } else if (key === '000') {
    cashModal.value.rawValue += '000'
  } else {
    cashModal.value.rawValue += key
  }
  // Format display with commas
  const num = parseFloat(cashModal.value.rawValue) || 0
  cashModal.value.displayValue = num > 0 ? num.toLocaleString('en-US') : ''
  updateCashModalChange()
}

function setCashPreset(amt) {
  cashModal.value.rawValue = String(amt)
  cashModal.value.displayValue = amt.toLocaleString('en-US')
  updateCashModalChange()
}

function setCashExact() {
  const exact = totalDueAmount.value
  cashModal.value.rawValue = String(exact)
  cashModal.value.displayValue = exact.toLocaleString('en-US', { minimumFractionDigits: 2 })
  cashModal.value.changeDue = 0
}

async function confirmCashPayment() {
  const tendered = parseFloat(cashModal.value.rawValue) || 0
  if (tendered < totalDueAmount.value) return
  cashTendered.value = tendered
  cashModal.value.submitting = true
  await submitTransaction()
  cashModal.value.open = false
  cashModal.value.submitting = false
}

// Steppers in Cart
function increaseCartQty(item) {
  if (
    item.isServiceItem ||
    item.product?.is_service ||
    (item.product?.name &&
      (item.product.name.includes('GCash') || item.product.name.includes('Other')))
  ) {
    item.quantity = parseFloat((item.quantity + 1).toFixed(2))
    playBeep()
    return
  }
  const availableStock = getAvailableStockForUnit(item.product, item.unitType, item)
  const unitLabel =
    item.unitType === 'SACK'
      ? item.product.unit_bulk_name || 'sack'
      : item.product.unit_retail_name || 'kilo'
  if (item.quantity + 1 > availableStock) {
    playWarning()
    $q.notify({
      color: 'warning',
      message: `Stock limit reached: only ${availableStock} ${unitLabel}(s) available.`,
      icon: 'warning',
      position: 'top',
      timeout: 1500,
    })
    return
  }
  item.quantity = parseFloat((item.quantity + 1).toFixed(2))
  playBeep()
}

function decreaseCartQty(item, idx) {
  if (item.quantity <= 1) {
    cart.value.splice(idx, 1)
  } else {
    item.quantity = parseFloat((item.quantity - 1).toFixed(2))
  }
  playBeep()
}

function clearCart() {
  if (cart.value.length > 0) playWarning()
  cart.value = []
  cashTendered.value = null
}

// Add Item Modal
const hasKiloPrice = computed(() => {
  return (
    addItemModal.value.product && parseFloat(addItemModal.value.product.price_per_kilo || 0) > 0
  )
})

const hasSackPrice = computed(() => {
  return (
    addItemModal.value.product && parseFloat(addItemModal.value.product.price_per_sack || 0) > 0
  )
})

const currentUnitPrice = computed(() => {
  if (!addItemModal.value.product) return 0
  if (addItemModal.value.unitType === 'SACK') {
    return parseFloat(addItemModal.value.product.price_per_sack || 0)
  }
  return parseFloat(addItemModal.value.product.price_per_kilo || 0)
})

const calculatedModalSubtotal = computed(() => {
  const qty = parseFloat(addItemModal.value.quantity) || 0
  return qty * currentUnitPrice.value
})

function setUnitType(type) {
  addItemModal.value.unitType = type
  if (type === 'SACK') {
    addItemModal.value.pricingMode = 'WEIGHT'
    addItemModal.value.quantity = Math.max(1, Math.round(addItemModal.value.quantity || 1))
  }
}

function onBudgetAmountChange(val) {
  const budget = parseFloat(val) || 0
  const price = currentUnitPrice.value
  if (budget > 0 && price > 0) {
    const rawKg = budget / price
    const roundedKg = parseFloat(rawKg.toFixed(2))
    addItemModal.value.quantity = roundedKg > 0 ? roundedKg : 0.01
  }
}

function setBudgetPreset(bAmt) {
  addItemModal.value.pricingMode = 'BUDGET'
  addItemModal.value.budgetAmount = bAmt
  onBudgetAmountChange(bAmt)
  playBeep()
}

function onPricingModeSwitch(mode) {
  if (mode === 'BUDGET') {
    if (!addItemModal.value.budgetAmount) {
      setBudgetPreset(50)
    } else {
      onBudgetAmountChange(addItemModal.value.budgetAmount)
    }
  }
}

function openAddProductModal(product) {
  addItemModal.value.product = product
  // Default to KILO if kilo price exists, otherwise SACK
  const defaultUnit = parseFloat(product.price_per_kilo || 0) > 0 ? 'KILO' : 'SACK'
  addItemModal.value.unitType = defaultUnit
  addItemModal.value.pricingMode = 'WEIGHT'
  addItemModal.value.budgetAmount = null
  addItemModal.value.quantity = 1
  addItemModal.value.open = true
}

function stepModalQty(delta) {
  const cur = parseFloat(addItemModal.value.quantity) || 0
  addItemModal.value.quantity = Math.max(0.01, parseFloat((cur + delta).toFixed(2)))
  playBeep()
}

function confirmAddToCart() {
  const product = addItemModal.value.product
  const unitType = addItemModal.value.unitType
  const quantity = parseFloat(addItemModal.value.quantity) || 1
  const price = currentUnitPrice.value
  if (!product || quantity <= 0) return

  const existing = cart.value.find((i) => i.product.id === product.id && i.unitType === unitType)
  const availableStock = getAvailableStockForUnit(product, unitType, existing)
  const unitLabel =
    unitType === 'SACK' ? product.unit_bulk_name || 'sack' : product.unit_retail_name || 'kilo'

  const totalWanted = (existing ? existing.quantity : 0) + quantity

  if (totalWanted > availableStock) {
    playWarning()
    $q.notify({
      color: 'negative',
      message: `Cannot add ${quantity}: only ${availableStock} ${unitLabel}(s) available in stock.`,
      icon: 'warning',
      position: 'top',
      timeout: 2500,
    })
    return
  }

  const feeDetails =
    addItemModal.value.pricingMode === 'BUDGET' && addItemModal.value.budgetAmount
      ? `₱${addItemModal.value.budgetAmount} budget (${quantity} ${unitLabel})`
      : ''

  if (existing) {
    existing.quantity = parseFloat((existing.quantity + quantity).toFixed(2))
  } else {
    cart.value.push({ product, unitType, quantity, price, feeDetails })
  }

  addItemModal.value.open = false
  playBeep()

  $q.notify({
    color: 'primary',
    message: `Added ${quantity} ${unitLabel} ${product.name} to ticket`,
    icon: 'add_shopping_cart',
    timeout: 800,
  })
}

// Checkout Submit
async function submitTransaction() {
  if (cart.value.length === 0) {
    $q.notify({
      color: 'warning',
      message: 'Cart is empty. Add items to checkout.',
      icon: 'shopping_cart',
    })
    return
  }

  // Credit requires customer ledger
  if (paymentMethod.value === 'CREDIT' && !selectedCustomer.value) {
    $q.notify({
      color: 'negative',
      message: 'Please select a customer ledger before checking out on Credit/Utang.',
      icon: 'person_off',
    })
    showCustomerPicker.value = true
    return
  }

  // Final stock depletion verification across unified pool (skip services / GCash / custom items)
  const productCartUsage = {}
  for (const item of cart.value) {
    if (item.isServiceItem || item.product?.is_service) continue
    const pId = item.product.id
    const ratio = parseFloat(item.product.units_per_bulk) || 50
    const itemBaseQty = item.unitType === 'SACK' ? item.quantity * ratio : item.quantity
    productCartUsage[pId] = (productCartUsage[pId] || 0) + itemBaseQty
  }

  for (const item of cart.value) {
    if (item.isServiceItem || item.product?.is_service) continue
    const totalBase = getProductTotalBaseStock(item.product)
    const neededBase = productCartUsage[item.product.id] || 0
    if (neededBase > totalBase) {
      const isBulk = item.unitType === 'SACK'
      const unitName = isBulk
        ? item.product.unit_bulk_name || 'sack'
        : item.product.unit_retail_name || 'kilo'
      const availableUnits = isBulk
        ? Math.floor(totalBase / (parseFloat(item.product.units_per_bulk) || 50))
        : totalBase
      $q.notify({
        color: 'negative',
        message: `Insufficient stock for "${item.product.name}". Total available in pool: ${availableUnits} ${unitName}(s).`,
        icon: 'warning',
        timeout: 4000,
      })
      return
    }
  }

  try {
    let amountPaid = 0
    let changeGiven = 0

    if (paymentMethod.value === 'CASH') {
      const tendered =
        cashTendered.value !== null && cashTendered.value !== undefined
          ? parseFloat(cashTendered.value)
          : totalDueAmount.value
      amountPaid = Math.max(tendered, totalDueAmount.value)
      changeGiven = Math.max(0, tendered - totalDueAmount.value)
    } else if (paymentMethod.value === 'GCASH') {
      amountPaid = totalDueAmount.value
      changeGiven = 0
    } else if (paymentMethod.value === 'CREDIT') {
      // Full credit/utang: amount paid today is 0, so customer utang increases by total_amount!
      amountPaid = 0.0
      changeGiven = 0.0
    }

    const payload = {
      transaction_type: paymentMethod.value,
      customer: selectedCustomer.value?.id || null,
      total_amount: totalDueAmount.value,
      amount_paid: amountPaid,
      change_given: changeGiven,
      items: cart.value.map((i) => ({
        product: i.product.id,
        unit_type: i.unitType,
        quantity: i.quantity,
        unit_price: i.price,
        subtotal: i.quantity * i.price,
        notes: i.feeDetails || '',
      })),
    }

    const cartSnapshot = cart.value.map((i) => ({
      product_name: i.customName || i.product.name,
      quantity: i.quantity,
      unit_price: i.price,
      subtotal: i.quantity * i.price,
      unit_type: i.isServiceItem
        ? 'Item'
        : i.unitType === 'SACK'
          ? i.product.unit_bulk_name || 'Sack'
          : i.product.unit_retail_name || 'Kilo',
      feeDetails: i.feeDetails || '',
      notes: i.feeDetails || '',
    }))

    const res = await api.post('transactions/', payload)
    receiptDialog.value.tx = res.data
    receiptDialog.value.items = cartSnapshot
    receiptDialog.value.open = true
    playChime()

    clearCart()
    fetchData()
  } catch (err) {
    console.error(err)
    $q.notify({ color: 'negative', message: 'Failed to process checkout.' })
  }
}

function printReceipt() {
  const slipElement = document.getElementById('pos-receipt-slip')
  if (!slipElement) {
    window.print()
    return
  }

  const is58 = receiptPaperSize.value === '58mm'
  const pageSize = is58 ? '58mm auto' : '80mm auto'
  const pageMargin = is58 ? '2mm 1mm' : '4mm 2mm'
  const slipWidth = is58 ? '210px' : '320px'
  const fontSize = is58 ? '9.5px' : '11px'
  const logoHeight = is58 ? '38px' : '48px'
  const titleSize = is58 ? '13px' : '15px'
  const subTotalSize = is58 ? '12px' : '14px'

  // Create an isolated printable iframe so ONLY the clean receipt is printed
  const existingIframe = document.getElementById('receipt-print-frame')
  if (existingIframe) existingIframe.remove()

  const iframe = document.createElement('iframe')
  iframe.id = 'receipt-print-frame'
  iframe.style.position = 'fixed'
  iframe.style.right = '0'
  iframe.style.bottom = '0'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = '0'
  document.body.appendChild(iframe)

  const doc = iframe.contentWindow.document
  doc.open()
  doc.write(`
    <!DOCTYPE html>
    <html>
      <head>
        <base href="${window.location.origin}/">
        <title>Receipt #TX-${receiptDialog.value.tx?.id || ''} - Nichole Agrivet</title>
        <style>
          @page {
            size: ${pageSize};
            margin: ${pageMargin};
          }
          * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
          }
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            margin: 0;
            padding: ${is58 ? '2px' : '4px'};
            color: #0f172a;
            background: #ffffff;
            font-size: ${fontSize};
            line-height: 1.35;
          }
          .receipt-paper-slip {
            width: 100%;
            max-width: ${slipWidth};
            margin: 0 auto;
            background: #ffffff;
            padding: ${is58 ? '4px 2px' : '6px 8px'};
            border: ${is58 ? 'none' : '1px solid #e2e8f0'};
            border-radius: 6px;
          }
          .text-center { text-align: center; }
          .text-right { text-align: right; }
          .receipt-logo {
            height: ${logoHeight};
            width: auto;
            object-fit: contain;
            margin: 0 auto 3px;
            display: block;
          }
          .receipt-store-title {
            font-size: ${titleSize};
            font-weight: 800;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            color: #0f172a;
            margin-bottom: 2px;
          }
          .receipt-store-subtitle {
            font-size: ${is58 ? '8.5px' : '10px'};
            color: #475569;
            font-weight: 500;
            margin-bottom: 2px;
          }
          .receipt-dashed-line {
            border-top: 1px dashed #cbd5e1;
            margin: ${is58 ? '5px 0' : '7px 0'};
          }
          .row {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            margin-bottom: 2px;
          }
          .justify-between { justify-content: space-between; }
          .items-center { align-items: center; }
          .col-7 { width: 58%; }
          .col-2 { width: 17%; text-align: center; }
          .col-3 { width: 25%; text-align: right; }
          .num-tabular, .font-tabular {
            font-variant-numeric: tabular-nums;
            font-family: inherit;
          }
          .text-caption { font-size: ${is58 ? '8.5px' : '10px'}; }
          .text-body2 { font-size: ${is58 ? '9.5px' : '11px'}; }
          .text-subtitle1 { font-size: ${is58 ? '10px' : '12px'}; }
          .text-h6 { font-size: ${subTotalSize}; font-weight: 800; }
          
          /* Colors exactly matching screen */
          .text-slate-900 { color: #0f172a !important; }
          .text-slate-700 { color: #334155 !important; }
          .text-slate-600 { color: #475569 !important; }
          .text-slate-500 { color: #64748b !important; }
          .text-slate-400 { color: #94a3b8 !important; }
          .text-primary { color: #0d6832 !important; }
          .text-negative { color: #e11d48 !important; }
          .text-indigo-8 { color: #3730a3 !important; }
          
          /* Typography */
          .text-weight-bold { font-weight: 700 !important; }
          .text-weight-bolder { font-weight: 800 !important; }
          .text-weight-medium { font-weight: 500 !important; }
          .text-uppercase { text-transform: uppercase; }
          .leading-tight { line-height: 1.25; }
          
          /* Change Due Box */
          .bg-slate-50 {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            padding: ${is58 ? '3px 4px' : '4px 6px'};
          }
          .rounded-borders { border-radius: 4px; }
          .q-mb-xs { margin-bottom: 2px; }
          .q-mt-xs { margin-top: 2px; }
          .q-pt-xs { padding-top: 2px; }
          .q-pb-xs { padding-bottom: 2px; }
          .q-pa-xs { padding: ${is58 ? '3px 4px' : '4px 6px'}; }
          .q-gutter-y-xs > * + * { margin-top: 2.5px; }
        </style>
      </head>
      <body>
        <div class="receipt-paper-slip">
          ${slipElement.innerHTML}
        </div>
      </body>
    </html>
  `)
  doc.close()

  const triggerPrint = () => {
    try {
      iframe.contentWindow.focus()
      iframe.contentWindow.print()
    } catch (e) {
      console.error('Print error:', e)
    } finally {
      setTimeout(() => {
        iframe.remove()
      }, 2000)
    }
  }

  // Ensure mascot logo image is loaded before opening print preview dialog
  const img = doc.querySelector('img')
  if (img) {
    if (img.complete && img.naturalHeight !== 0) {
      setTimeout(triggerPrint, 120)
    } else {
      img.onload = () => setTimeout(triggerPrint, 120)
      img.onerror = () => setTimeout(triggerPrint, 120)
      setTimeout(triggerPrint, 800)
    }
  } else {
    setTimeout(triggerPrint, 150)
  }
}

async function shareReceiptViaBluetooth() {
  const tx = receiptDialog.value.tx
  if (!tx) return
  const is58 = receiptPaperSize.value === '58mm'
  const divider = is58
    ? '--------------------------------'
    : '------------------------------------------'

  let receiptText = `================================\n`
  receiptText += `        NICHOLE AGRIVET        \n`
  receiptText += `Agricultural & Veterinary Supplies\n`
  receiptText += `       VillaReal, Samar         \n`
  receiptText += `${divider}\n`
  receiptText += `Receipt No: #TX-${tx.id}\n`
  receiptText += `Date: ${formatReceiptDate(tx.created_at)}\n`
  receiptText += `Cashier: ${userName.value}\n`
  receiptText += `Customer: ${tx.customer_name || selectedCustomer.value?.name || 'Walk-in Customer'}\n`
  receiptText += `Payment: ${tx.transaction_type}\n`
  receiptText += `${divider}\n`
  receiptText += `ITEM                QTY    PRICE   TOTAL\n`
  receiptText += `${divider}\n`

  const items = receiptDialog.value.items || []
  items.forEach((i) => {
    const name = (i.product_name || '').slice(0, 18).padEnd(18, ' ')
    const qty = String(i.quantity).padStart(3, ' ')
    const pr = parseFloat(i.unit_price).toFixed(0).padStart(6, ' ')
    const sub = parseFloat(i.subtotal).toFixed(0).padStart(7, ' ')
    receiptText += `${name} ${qty} ${pr} ${sub}\n`
  })

  receiptText += `${divider}\n`
  receiptText += `TOTAL AMOUNT: PHP ${parseFloat(tx.total_amount).toFixed(2)}\n`
  receiptText += `AMOUNT PAID:  PHP ${parseFloat(tx.amount_paid).toFixed(2)}\n`
  receiptText += `CHANGE:       PHP ${parseFloat(tx.change_given || 0).toFixed(2)}\n`
  receiptText += `================================\n`
  receiptText += ` Thank you for shopping with us! \n`
  receiptText += `   Daghang Salamat & God Bless!  \n`

  if (navigator.share) {
    try {
      await navigator.share({
        title: `Nichole Agrivet Receipt #TX-${tx.id}`,
        text: receiptText,
      })
      playBeep()
      $q.notify({
        color: 'positive',
        message: 'Receipt shared to Bluetooth/Printer app',
        icon: 'share',
      })
    } catch (e) {
      if (e.name !== 'AbortError') {
        copyReceiptToClipboard(receiptText)
      }
    }
  } else {
    copyReceiptToClipboard(receiptText)
  }
}

function copyReceiptToClipboard(text) {
  if (navigator.clipboard?.writeText) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        playBeep()
        $q.notify({
          color: 'positive',
          message: 'Receipt text copied to clipboard! Paste into your Bluetooth printer app.',
          icon: 'content_paste',
          timeout: 3000,
        })
      })
      .catch(() => {})
  }
}

// Fetch Initial Data
async function fetchData() {
  try {
    const [pRes, cRes, catRes, shiftRes] = await Promise.all([
      api.get('products/'),
      api.get('customers/'),
      api.get('categories/'),
      api.get('transactions/daily-summary/'),
    ])
    products.value = pRes.data
    customers.value = cRes.data
    customerOptions.value = cRes.data
    categories.value = catRes.data
    todayShiftTotal.value = parseFloat(
      shiftRes.data.total_shift_sales || shiftRes.data.total_cash_revenue || 0.0,
    )
  } catch (err) {
    console.error(err)
  }
}

const customerOptions = ref([])

function filterCustomers(val, update) {
  update(() => {
    if (val === '') {
      customerOptions.value = customers.value
    } else {
      const needle = val.toLowerCase()
      customerOptions.value = customers.value.filter(
        (c) =>
          c.name.toLowerCase().includes(needle) ||
          (c.contact_number || '').toLowerCase().includes(needle),
      )
    }
  })
}

// Guard: Credit is only allowed for registered customers
function selectCreditPayment() {
  if (!selectedCustomer.value) {
    $q.notify({
      color: 'warning',
      message:
        'Walk-in customers cannot do Credit. Please select or add a registered customer first.',
      icon: 'person_off',
      position: 'top',
      timeout: 3500,
    })
    showCustomerPicker.value = true
    return
  }
  paymentMethod.value = 'CREDIT'
}

function openAddCustomerModal() {
  addCustomerModal.value = { open: true, name: '', contact_number: '', notes: '', saving: false }
}

async function saveNewCustomer() {
  if (!addCustomerModal.value.name.trim()) return
  addCustomerModal.value.saving = true
  try {
    const res = await api.post('customers/', {
      name: addCustomerModal.value.name.trim(),
      contact_number: addCustomerModal.value.contact_number.trim(),
      notes: addCustomerModal.value.notes.trim(),
    })
    // Add to local list and select immediately
    customers.value.push(res.data)
    customerOptions.value = customers.value
    selectedCustomer.value = res.data
    // If this was triggered from Credit selection, apply it now
    paymentMethod.value = 'CREDIT'
    addCustomerModal.value.open = false
    showCustomerPicker.value = false
    $q.notify({
      color: 'positive',
      message: `Customer "${res.data.name}" created and selected!`,
      icon: 'check_circle',
      position: 'top',
      timeout: 2000,
    })
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to save customer. Check your input and try again.',
      icon: 'error',
      position: 'top',
    })
  } finally {
    addCustomerModal.value.saving = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.pos-screen {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.numpad-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.numpad-key {
  height: 46px;
  font-size: 1.15rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  cursor: pointer;
  transition: background 0.1s;
  &:active {
    background-color: #f1f5f9 !important;
  }
}

.bg-emerald-50 {
  background-color: #ecfdf5;
}
.bg-red-50 {
  background-color: #fef2f2;
}

.brand-mascot-raw {
  height: 46px;
  width: auto;
  object-fit: contain;
  border: none !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  background: transparent !important;
}

.shift-counter-pill {
  border-radius: 12px;
  height: 44px;
  border: 1px solid #e2e8f0;
  padding: 0 14px 0 8px;
  display: inline-flex;
  align-items: center;
  transition: all 0.15s ease;
  user-select: none;
}
.shift-counter-pill:hover {
  background-color: #f8fafc;
  border-color: #cbd5e1;
}

.shift-icon-wrap {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background-color: #e6f4ea;
  flex-shrink: 0;
}

.shift-label {
  font-size: 0.62rem;
  letter-spacing: 0.05em;
  color: #64748b;
  line-height: 1;
}

.shift-amount {
  font-size: 0.95rem;
  line-height: 1.15;
  color: #0f172a;
  margin-top: 1px;
}

.user-profile-pill {
  border-radius: 12px;
  height: 44px;
  border: 1px solid #e5e7eb;
}

:deep(.tablet-sku-search.q-field--outlined .q-field__control) {
  border-radius: 9999px !important;
  height: 44px;
  border: 2px solid #0d6832 !important;
  background-color: #ffffff !important;
  box-shadow: 0 1px 4px rgba(13, 104, 50, 0.12) !important;
}
:deep(.tablet-sku-search.q-field--outlined .q-field__control::before),
:deep(.tablet-sku-search.q-field--outlined .q-field__control::after) {
  border: none !important;
}
:deep(.tablet-sku-search.q-field--focused .q-field__control) {
  border: 2.5px solid #0d6832 !important;
  box-shadow: 0 0 0 3px rgba(13, 104, 50, 0.2) !important;
}

.receipt-paper-slip {
  border: 1px solid #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  max-width: 380px;
  margin: 0 auto;
}

.receipt-logo {
  height: 48px;
  width: auto;
  object-fit: contain;
  display: block;
  margin: 0 auto 4px auto;
}

.receipt-store-title {
  font-size: 1.15rem;
  letter-spacing: 0.04em;
  color: #0f172a;
}

.receipt-store-subtitle {
  font-size: 0.75rem;
  color: #475569;
}

.receipt-dashed-line {
  border-top: 1px dashed #cbd5e1;
  margin: 8px 0;
}

@media print {
  @page {
    size: 80mm auto;
    margin: 4mm;
  }
  body * {
    visibility: hidden !important;
  }
  #pos-receipt-slip,
  #pos-receipt-slip * {
    visibility: visible !important;
  }
  #pos-receipt-slip {
    position: fixed !important;
    left: 50% !important;
    top: 0 !important;
    transform: translateX(-50%) !important;
    width: 320px !important;
    max-width: 100% !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
  }
  .no-print,
  .q-dialog__backdrop,
  .q-card-actions {
    display: none !important;
    visibility: hidden !important;
  }
}

.categories-scroll-wrapper {
  overflow-x: auto;
  white-space: nowrap;
}

.pos-product-card {
  border-radius: 16px;
  border: 1px solid #e5e7eb;
  transition: all 0.15s ease;
}
.pos-product-card:hover {
  transform: translateY(-2px);
  border-color: #0d6832 !important;
  box-shadow: 0 8px 24px -4px rgba(13, 104, 50, 0.12) !important;
}
.pos-product-low-stock {
  border: 1.5px solid #fca5a5 !important;
}
.pos-product-out-of-stock {
  border: 1px dashed #cbd5e1 !important;
  background-color: #fafbfc !important;
  opacity: 0.72;
}
.pos-product-out-of-stock:hover {
  transform: none !important;
  border-color: #94a3b8 !important;
  box-shadow: none !important;
}

.mint-plus-btn-disabled {
  background-color: #f1f5f9 !important;
  color: #94a3b8 !important;
}
.mint-plus-btn-disabled:hover {
  background-color: #f1f5f9 !important;
  transform: none !important;
}

.product-icon-squircle {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mint-plus-btn {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background-color: #e6f4ea;
  color: #0d6832;
  transition: all 0.1s ease;
}
.mint-plus-btn:hover {
  background-color: #d1fae5;
  transform: scale(1.08);
}

.pos-main-row {
  width: 100%;
  max-width: 100%;
  margin-left: 0;
  margin-right: 0;
}

.pos-products-catalog {
  min-width: 0; /* Critical: allows flexbox child to shrink without pushing siblings */
  flex: 1 1 0%;
}

.pos-checkout-column {
  width: 345px;
  min-width: 320px;
  max-width: 360px;
  flex-shrink: 0;
}

.pos-checkout-panel {
  border-radius: 18px;
  border: 1px solid #e5e7eb;
  position: sticky;
  top: 12px;
  display: flex !important;
  flex-direction: column !important;
  flex-wrap: nowrap !important;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 820px) {
  .pos-main-row {
    flex-wrap: wrap !important;
  }
  .pos-checkout-column {
    width: 100% !important;
    max-width: 100% !important;
  }
}

.customer-farm-card {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 14px;
}

.farm-icon-squircle {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background-color: #e6f4ea;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
}

.cart-items-scroll {
  max-height: clamp(140px, 28vh, 280px);
  overflow-y: auto;
}

.border-slate {
  border: 1px solid #e5e7eb;
}
.border-top-subtle {
  border-top: 1px solid #f1f5f9;
}
.border-bottom-subtle {
  border-bottom: 1px solid #f1f5f9;
}

.quick-qty-btn {
  height: 48px;
  font-size: 1.15rem !important;
  font-weight: 800 !important;
  border: 1.5px solid #cbd5e1 !important;
  border-radius: 12px !important;
  background-color: #f8fafc !important;
  color: #1e293b !important;
  letter-spacing: 0.02em;
  transition: all 0.15s ease;
}
.quick-qty-btn:hover {
  background-color: #f0fdf4 !important;
  border-color: #0d6832 !important;
  color: #0d6832 !important;
  transform: translateY(-1px);
}
.quick-qty-btn:active {
  transform: translateY(0);
}

.header-hamburger-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  transition: all 0.15s ease;
  &:hover {
    background-color: #f1f5f9;
    border-color: #cbd5e1;
  }
}
</style>
