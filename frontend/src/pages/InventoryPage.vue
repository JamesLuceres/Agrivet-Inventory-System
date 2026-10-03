<template>
  <q-page class="q-pa-md">
    <!-- Header -->
    <div class="row items-center q-mb-lg justify-between">
      <div class="row items-center">
        <q-btn
          flat
          round
          dense
          icon="arrow_back"
          size="lg"
          color="blue-10"
          class="q-mr-md"
          @click="$router.push('/')"
        >
          <q-tooltip>Back to Dashboard</q-tooltip>
        </q-btn>
        <q-icon name="inventory_2" size="lg" color="blue-10" class="q-mr-sm" />
        <h1 class="text-h4 text-weight-bold text-blue-10 q-my-none">Available Items & Stocks</h1>
      </div>
      <div>
        <q-btn color="primary" icon="add" label="Add New Product" @click="openAddDialog" />
      </div>
    </div>

    <!-- Filters & Table Card -->
    <q-card flat bordered class="bg-white shadow-1">
      <!-- Search and Filter Header -->
      <q-card-section class="row q-col-gutter-sm items-center q-pb-md">
        <div class="col-12 col-sm-6 col-md-8">
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
        <div class="col-12 col-sm-6 col-md-4">
          <q-select
            v-model="selectedCategory"
            :options="categoryOptions"
            label="Filter by Category"
            outlined
            dense
            emit-value
            map-options
          />
        </div>
      </q-card-section>

      <q-separator />

      <!-- Data Table -->
      <q-table
        :rows="filteredProducts"
        :columns="columns"
        row-key="id"
        flat
        bordered
        separator="cell"
        class="inventory-data-table"
        :rows-per-page-options="[10, 25, 50]"
        no-data-label="No items in inventory."
      >
        <!-- Extra Bold Header Cells -->
        <template v-slot:header-cell="props">
          <q-th :props="props" class="table-header-bold">
            <span class="text-weight-bolder text-dark" style="font-weight: 800; font-size: 0.93rem">
              {{ props.col.label }}
            </span>
          </q-th>
        </template>

        <!-- Category name -->
        <template v-slot:body-cell-category_name="props">
          <q-td :props="props">
            <q-badge color="indigo-1" text-color="indigo-10" class="text-weight-bold">
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>

        <!-- Units badge -->
        <template v-slot:body-cell-units="props">
          <q-td :props="props">
            <q-chip dense outline color="slate-7" class="text-weight-medium">
              <span v-if="props.row.unit_bulk_name && props.row.price_per_sack">
                {{ props.row.unit_bulk_name }} & {{ props.row.unit_retail_name || 'Item' }}
              </span>
              <span v-else> Single {{ props.row.unit_retail_name || 'Piece' }} </span>
            </q-chip>
          </q-td>
        </template>

        <!-- Retail / Single Unit & Price -->
        <template v-slot:body-cell-retail_info="props">
          <q-td :props="props">
            <div v-if="props.row.price_per_kilo">
              <div class="text-weight-bold text-emerald-7 num-tabular">
                ₱{{ parseFloat(props.row.price_per_kilo).toFixed(2) }} /
                {{ props.row.unit_retail_name || 'Item' }}
              </div>

              <!-- Product with Bulk Unit (e.g. Sack & Kilo) -->
              <div v-if="props.row.unit_bulk_name && props.row.price_per_sack" class="text-caption">
                <!-- When customer bought kilos, display the remaining kilos and total -->
                <div v-if="parseFloat(props.row.stock_kilos || 0) > 0" class="text-slate-800">
                  <span class="text-weight-bold"
                    >{{ parseFloat(props.row.stock_kilos) }}
                    {{ props.row.unit_retail_name || 'Kilos' }}</span
                  >
                  <div class="text-slate-500 font-medium" style="font-size: 0.74rem">
                    Total:
                    {{
                      (
                        parseFloat(props.row.stock_sacks || 0) *
                          parseFloat(props.row.units_per_bulk || 50) +
                        parseFloat(props.row.stock_kilos || 0)
                      ).toLocaleString()
                    }}
                    {{ props.row.unit_retail_name || 'Kilos' }}
                  </div>
                </div>
                <!-- When whole sacks only (e.g. 2 sacks = 100 kilos) -->
                <div v-else class="text-slate-800">
                  <span class="text-weight-bold"
                    >{{
                      (
                        parseFloat(props.row.stock_sacks || 0) *
                        parseFloat(props.row.units_per_bulk || 50)
                      ).toLocaleString()
                    }}
                    {{ props.row.unit_retail_name || 'Kilos' }}</span
                  >
                </div>

                <q-badge class="badge-out-of-stock q-mt-xs" v-if="isOutOfStock(props.row, 'kilos')">
                  OUT OF STOCK
                </q-badge>
                <q-badge class="badge-low-stock q-mt-xs" v-else-if="isLowStock(props.row, 'kilos')">
                  LOW
                </q-badge>
              </div>

              <!-- Single Unit Product -->
              <div
                v-else
                class="text-caption"
                :class="
                  isOutOfStock(props.row, 'kilos')
                    ? 'text-slate-400'
                    : isLowStock(props.row, 'kilos')
                      ? 'text-negative text-weight-bold'
                      : 'text-slate-600'
                "
              >
                Stock: {{ parseFloat(props.row.stock_kilos || 0) }}
                {{ props.row.unit_retail_name || 'Items' }}
                <q-badge class="badge-out-of-stock q-ml-xs" v-if="isOutOfStock(props.row, 'kilos')">
                  OUT OF STOCK
                </q-badge>
                <q-badge class="badge-low-stock q-ml-xs" v-else-if="isLowStock(props.row, 'kilos')">
                  LOW
                </q-badge>
              </div>
            </div>
            <div v-else class="text-slate-400">-</div>
          </q-td>
        </template>

        <!-- Bulk Unit & Price -->
        <template v-slot:body-cell-bulk_info="props">
          <q-td :props="props">
            <div v-if="props.row.price_per_sack && props.row.unit_bulk_name">
              <div class="text-weight-bold text-indigo-7 num-tabular">
                ₱{{ parseFloat(props.row.price_per_sack).toFixed(2) }} /
                {{ props.row.unit_bulk_name }}
              </div>
              <div
                class="text-caption"
                :class="
                  isOutOfStock(props.row, 'sacks')
                    ? 'text-slate-400'
                    : isLowStock(props.row, 'sacks')
                      ? 'text-negative text-weight-bold'
                      : 'text-slate-700'
                "
              >
                Stock: {{ parseFloat(props.row.stock_sacks || 0) }}
                {{ pluralize(props.row.unit_bulk_name) }}
                <q-badge class="badge-out-of-stock q-ml-xs" v-if="isOutOfStock(props.row, 'sacks')">
                  OUT OF STOCK
                </q-badge>
                <q-badge class="badge-low-stock q-ml-xs" v-else-if="isLowStock(props.row, 'sacks')">
                  LOW
                </q-badge>
              </div>
              <div class="text-caption text-slate-400" style="font-size: 0.72rem">
                (1 {{ props.row.unit_bulk_name }} = {{ props.row.units_per_bulk || 50 }}
                {{ props.row.unit_retail_name || 'kilos' }})
              </div>
            </div>
            <div v-else class="text-slate-400">-</div>
          </q-td>
        </template>


        <!-- Actions -->
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" align="center" class="q-gutter-xs">
            <q-btn flat round dense color="primary" icon="edit" @click="openEditDialog(props.row)">
              <q-tooltip>Edit Stock & Details</q-tooltip>
            </q-btn>
            <q-btn
              flat
              round
              dense
              color="negative"
              icon="delete_outline"
              @click="confirmDeleteProduct(props.row)"
            >
              <q-tooltip>Delete Product</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Product Form Dialog (Add / Edit) -->
    <q-dialog v-model="productDialog.open" persistent>
      <q-card style="width: 540px; max-width: 95vw">
        <q-card-section class="bg-indigo-10 text-white q-py-md">
          <div class="text-h6 text-weight-bold">
            {{ productDialog.editMode ? 'Edit Product Details' : 'Add New Product' }}
          </div>
        </q-card-section>

        <q-card-section class="q-py-md row q-col-gutter-sm">
          <!-- Name -->
          <div class="col-12">
            <q-input
              v-model="productForm.name"
              label="Product Name"
              outlined
              dense
              :rules="[(val) => !!val || 'Name is required']"
            />
          </div>

          <!-- Category -->
          <div class="col-12 col-sm-6">
            <q-select
              v-model="productForm.category"
              :options="formCategoryOptions"
              label="Select Category"
              outlined
              dense
              emit-value
              map-options
              use-input
              input-debounce="0"
              hide-selected
              fill-input
              :display-value="
                productForm.category
                  ? formCategoryOptions.find((c) => c.value === productForm.category)?.label || ''
                  : ''
              "
              :rules="[(val) => !!val || 'Category is required']"
              @new-value="createCategoryInline"
              @filter="filterCategoryOptions"
            >
              <template v-slot:no-option="scope">
                <q-item
                  v-if="scope.inputValue"
                  clickable
                  @click="createCategoryInline(scope.inputValue)"
                >
                  <q-item-section>
                    <q-item-label class="text-positive">
                      <q-icon name="add_circle" class="q-mr-xs" />
                      Create category "{{ scope.inputValue }}"
                    </q-item-label>
                  </q-item-section>
                </q-item>
                <q-item v-else>
                  <q-item-section class="text-grey-6"
                    >No categories yet. Type to create one.</q-item-section
                  >
                </q-item>
              </template>
            </q-select>
          </div>

          <!-- Measurement Preset / Unit Type Mode -->
          <div class="col-12 col-sm-6">
            <q-select
              v-model="unitPresetMode"
              :options="unitPresetOptions"
              label="Measurement Type"
              outlined
              dense
              emit-value
              map-options
              @update:model-value="onUnitPresetChange"
            />
          </div>

          <!-- Custom Unit Labels (Visible if CUSTOM mode selected) -->
          <template v-if="unitPresetMode === 'CUSTOM'">
            <div class="col-6">
              <q-input
                v-model="productForm.unit_retail_name"
                label="Retail Unit Name (e.g. Bottle, Piece, Kilo)"
                outlined
                dense
              />
            </div>
            <div class="col-6">
              <q-input
                v-model="productForm.unit_bulk_name"
                label="Bulk Unit Name (e.g. Case, Box, Sack)"
                outlined
                dense
                clearable
              />
            </div>
          </template>

          <!-- Conversion Ratio / Units Per Bulk -->
          <div class="col-12" v-if="productForm.unit_bulk_name">
            <div class="bg-indigo-50 border-slate rounded-borders q-pa-sm">
              <div class="row items-center q-col-gutter-sm">
                <div class="col-12 col-sm-6">
                  <q-input
                    v-model.number="productForm.units_per_bulk"
                    type="number"
                    min="1"
                    step="0.1"
                    :label="
                      '1 ' +
                      productForm.unit_bulk_name +
                      ' = how many ' +
                      (productForm.unit_retail_name || 'units') +
                      '?'
                    "
                    outlined
                    dense
                    bg-color="white"
                    :hint="'e.g. 50 ' + (productForm.unit_retail_name || 'kilos') + ' per sack'"
                  />
                </div>
                <div class="col-12 col-sm-6 text-caption text-indigo-10">
                  <div class="text-weight-bold">⚡ Unified Inventory Pool:</div>
                  <div>
                    1 {{ productForm.unit_bulk_name }} = {{ productForm.units_per_bulk || 50 }}
                    {{ productForm.unit_retail_name || 'Kilos' }}
                  </div>
                  <div class="text-positive text-weight-bolder">
                    Total Available:
                    {{
                      (
                        parseFloat(productForm.stock_sacks || 0) *
                          parseFloat(productForm.units_per_bulk || 50) +
                        parseFloat(productForm.stock_kilos || 0)
                      ).toFixed(1)
                    }}
                    {{ productForm.unit_retail_name || 'Kilos' }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <q-separator class="col-12 q-my-xs" />

          <!-- Dynamic Selling Pricing Inputs -->
          <!-- Retail / Single Unit Price -->
          <div :class="productForm.unit_bulk_name ? 'col-6' : 'col-12'">
            <q-input
              v-model.number="productForm.price_per_kilo"
              type="number"
              step="0.01"
              :label="
                'Selling Price per ' + (productForm.unit_retail_name || 'Piece / Item') + ' (₱)'
              "
              outlined
              dense
              prefix="₱"
            />
          </div>

          <!-- Bulk Price (Only if bulk unit exists) -->
          <div class="col-6" v-if="productForm.unit_bulk_name">
            <q-input
              v-model.number="productForm.price_per_sack"
              type="number"
              step="0.01"
              :label="'Selling Price per ' + productForm.unit_bulk_name + ' (₱)'"
              outlined
              dense
              prefix="₱"
            />
          </div>

          <!-- Supplier Cost Section (For Profit Margin Tracking) -->
          <div class="col-12 q-pt-xs">
            <div class="text-caption text-weight-bold text-slate-500 text-uppercase">
              Supplier Wholesale Cost (For Profit Tracking)
            </div>
          </div>

          <!-- Retail Cost -->
          <div :class="productForm.unit_bulk_name ? 'col-6' : 'col-12'">
            <q-input
              v-model.number="productForm.cost_per_kilo"
              type="number"
              step="0.01"
              :label="
                'Wholesale Cost per ' + (productForm.unit_retail_name || 'Piece / Item') + ' (₱)'
              "
              outlined
              dense
              prefix="₱"
            />
          </div>

          <!-- Bulk Cost -->
          <div class="col-6" v-if="productForm.unit_bulk_name">
            <q-input
              v-model.number="productForm.cost_per_sack"
              type="number"
              step="0.01"
              :label="'Wholesale Cost per ' + productForm.unit_bulk_name + ' (₱)'"
              outlined
              dense
              prefix="₱"
            />
          </div>

          <!-- Dynamic Stock Input -->
          <!-- Bulk Stock (When product has bulk units like Sacks / Boxes) -->
          <div class="col-12" v-if="productForm.unit_bulk_name">
            <q-input
              v-model.number="productForm.stock_sacks"
              type="number"
              min="0"
              step="1"
              :label="'Stock ' + productForm.unit_bulk_name + 's Count'"
              outlined
              dense
              :hint="
                'e.g. ' +
                (productForm.stock_sacks || 0) +
                ' ' +
                productForm.unit_bulk_name +
                's = ' +
                (productForm.stock_sacks || 0) * (productForm.units_per_bulk || 50) +
                ' ' +
                (productForm.unit_retail_name || 'kilos')
              "
            />
          </div>

          <!-- Retail Stock (Only for Single-Unit products without bulk units) -->
          <div class="col-12" v-else>
            <q-input
              v-model.number="productForm.stock_kilos"
              type="number"
              min="0"
              step="1"
              :label="'Stock ' + (productForm.unit_retail_name || 'Pieces') + ' Count'"
              outlined
              dense
            />
          </div>

          <!-- Live Stock Calculation Summary -->
          <div class="col-12" v-if="productForm.unit_bulk_name">
            <div class="bg-emerald-50 border-slate rounded-borders q-pa-sm text-caption">
              <div class="row items-center justify-between text-weight-bold">
                <span class="text-slate-800">📦 Total Available Stock:</span>
                <span class="text-positive text-subtitle2 num-tabular">
                  {{ productForm.stock_sacks || 0 }} {{ productForm.unit_bulk_name }}s =
                  {{
                    (
                      parseFloat(productForm.stock_sacks || 0) *
                      parseFloat(productForm.units_per_bulk || 50)
                    ).toFixed(0)
                  }}
                  {{ productForm.unit_retail_name || 'Kilos' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Low Stock Threshold -->
          <div class="col-12">
            <q-input
              v-model.number="productForm.low_stock_threshold"
              type="number"
              label="Low Stock Warning Limit"
              outlined
              dense
            />
          </div>

          <!-- Active Switch (Only on Edit) -->
          <div class="col-12 q-pt-xs" v-if="productDialog.editMode">
            <q-toggle v-model="productForm.is_active" label="Product is Active" color="primary" />
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            label="Save Product"
            color="primary"
            @click="saveProduct"
            :disable="!productForm.name || !productForm.category"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Product Added Success Dialog Popup -->
    <q-dialog v-model="successDialog.open">
      <q-card
        style="width: 440px; max-width: 90vw"
        class="rounded-borders-lg border-slate overflow-hidden"
      >
        <!-- Success Banner Header (Clean Forest Green) -->
        <q-card-section
          class="text-white text-center q-py-md"
          style="background-color: #0d6832 !important"
        >
          <q-icon name="check_circle" size="44px" class="q-mb-xs" />
          <div class="text-h6 text-weight-bold tracking-tight">Product Added Successfully!</div>
          <div class="text-caption text-emerald-100">Item has been logged into inventory</div>
        </q-card-section>

        <!-- Summary Info Box -->
        <q-card-section class="q-pa-md" v-if="successDialog.product">
          <div class="bg-slate-50 border-slate rounded-borders q-pa-md">
            <div class="row items-center justify-between q-mb-xs">
              <div class="text-subtitle1 text-weight-bold text-slate-900">
                {{ successDialog.product.name }}
              </div>
              <q-badge color="indigo-1" text-color="indigo-10" class="text-weight-bold">
                {{ successDialog.product.category_name }}
              </q-badge>
            </div>

            <q-separator class="q-my-sm" />

            <!-- Prices & Stocks Summary -->
            <div class="text-caption text-slate-600 column q-gutter-xs">
              <div
                class="row justify-between items-center"
                v-if="successDialog.product.price_per_kilo"
              >
                <span>{{ successDialog.product.unit_retail_name || 'Retail' }} Price:</span>
                <span class="text-weight-bold text-emerald-7 num-tabular">
                  ₱{{ parseFloat(successDialog.product.price_per_kilo).toFixed(2) }} /
                  {{ successDialog.product.unit_retail_name || 'item' }}
                </span>
              </div>
              <div
                class="row justify-between items-center"
                v-if="successDialog.product.price_per_kilo"
              >
                <span>Initial Stock:</span>
                <span class="text-weight-bold text-slate-900 num-tabular">
                  {{ parseFloat(successDialog.product.stock_kilos || 0) }}
                  {{ successDialog.product.unit_retail_name || 'items' }}
                </span>
              </div>

              <div
                class="row justify-between items-center q-mt-xs"
                v-if="successDialog.product.price_per_sack && successDialog.product.unit_bulk_name"
              >
                <span>{{ successDialog.product.unit_bulk_name }} Price:</span>
                <span class="text-weight-bold text-indigo-7 num-tabular">
                  ₱{{ parseFloat(successDialog.product.price_per_sack).toFixed(2) }} /
                  {{ successDialog.product.unit_bulk_name }}
                </span>
              </div>
              <div
                class="row justify-between items-center"
                v-if="successDialog.product.price_per_sack && successDialog.product.unit_bulk_name"
              >
                <span>Bulk Stock:</span>
                <span class="text-weight-bold text-slate-900 num-tabular">
                  {{ parseFloat(successDialog.product.stock_sacks || 0) }}
                  {{ successDialog.product.unit_bulk_name }}s
                </span>
              </div>
              <div
                class="row justify-between items-center text-positive text-weight-bold"
                v-if="successDialog.product.price_per_sack && successDialog.product.unit_bulk_name"
              >
                <span>Total Unified Stock:</span>
                <span class="num-tabular">
                  {{
                    (
                      parseFloat(successDialog.product.stock_sacks || 0) *
                        parseFloat(successDialog.product.units_per_bulk || 50) +
                      parseFloat(successDialog.product.stock_kilos || 0)
                    ).toFixed(1)
                  }}
                  {{ successDialog.product.unit_retail_name || 'units' }}
                </span>
              </div>
            </div>
          </div>
        </q-card-section>

        <!-- Actions -->
        <q-card-actions align="between" class="q-px-md q-pb-md">
          <q-btn
            outline
            color="primary"
            icon="add"
            label="Add Another Product"
            @click="handleAddAnotherProduct"
          />
          <q-btn color="positive" label="Done / View List" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <!-- Confirm Delete Product Dialog Popup -->
    <q-dialog v-model="deleteConfirmDialog.open" persistent>
      <q-card
        style="width: 440px; max-width: 90vw"
        class="rounded-borders-lg border-slate overflow-hidden"
      >
        <q-card-section
          class="text-white q-py-md row items-center"
          style="background-color: #e11d48 !important"
        >
          <q-icon name="warning" size="28px" class="q-mr-sm" />
          <div class="text-h6 text-weight-bold">Confirm Product Deletion</div>
        </q-card-section>

        <q-card-section
          class="q-pa-md text-slate-700 text-body1"
          v-if="deleteConfirmDialog.product"
        >
          Are you sure you want to delete
          <span class="text-weight-bold text-slate-900"
            >"{{ deleteConfirmDialog.product.name }}"</span
          >?
          <div class="text-caption text-rose-6 q-mt-sm text-weight-bold">
            ⚠️ This action will permanently remove the item from inventory.
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn
            color="negative"
            label="Delete Product"
            icon="delete_forever"
            @click="executeDeleteProduct"
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

const $q = useQuasar()

// State lists
const products = ref([])
const categories = ref([])

// Filters
const searchQuery = ref('')
const selectedCategory = ref(null)

// Dialog states
const productDialog = ref({
  open: false,
  editMode: false,
  productId: null,
})

const successDialog = ref({
  open: false,
  product: null,
})

const deleteConfirmDialog = ref({
  open: false,
  product: null,
})

const unitPresetMode = ref('FEEDS')

const unitPresetOptions = [
  {
    label: '🌾 Feeds & Grains (Sack & Kilo - 50 kg/sack)',
    value: 'FEEDS',
    bulk: 'Sack',
    retail: 'Kilo',
    ratio: 50,
  },
  {
    label: '🍾 Drinks & Beverages (Case & Bottle - 24/case)',
    value: 'DRINKS',
    bulk: 'Case',
    retail: 'Bottle',
    ratio: 24,
  },
  {
    label: '📦 Boxes & Pieces (Box & Piece - 12/box)',
    value: 'BOX_PIECE',
    bulk: 'Box',
    retail: 'Piece',
    ratio: 12,
  },
  {
    label: '🏷️ Essentials & Items (Single Piece / Qty)',
    value: 'SINGLE',
    bulk: null,
    retail: 'Piece',
    ratio: 1,
  },
  { label: '⚙️ Custom Measurement Units', value: 'CUSTOM', bulk: null, retail: 'Piece', ratio: 50 },
]

const productForm = ref({
  name: '',
  category: null,
  unit_bulk_name: 'Sack',
  unit_retail_name: 'Kilo',
  units_per_bulk: 50.0,
  price_per_sack: null,
  price_per_kilo: null,
  cost_per_sack: null,
  cost_per_kilo: null,
  stock_sacks: 0.0,
  stock_kilos: 0.0,
  low_stock_threshold: 5,
  is_active: true,
})

function onUnitPresetChange(value) {
  const preset = unitPresetOptions.find((p) => p.value === value)
  if (preset && value !== 'CUSTOM') {
    productForm.value.unit_bulk_name = preset.bulk
    productForm.value.unit_retail_name = preset.retail
    productForm.value.units_per_bulk = preset.ratio || 50
    if (!preset.bulk) {
      productForm.value.price_per_sack = null
      productForm.value.stock_sacks = 0.0
      productForm.value.cost_per_sack = null
    }
  }
}

// Mapped selections
const categoryOptions = computed(() => {
  const list = categories.value.map((cat) => ({ label: cat.name, value: cat.id }))
  return [{ label: 'All Categories', value: null }, ...list]
})

const formCategoryOptions = computed(() => {
  return categories.value.map((cat) => ({ label: cat.name, value: cat.id }))
})

// Filter category options for search
function filterCategoryOptions(val, update) {
  update(() => {
    if (!val) {
      // no filtering needed, formCategoryOptions computed handles it
    }
  })
}

// Create a new category inline from the product form
async function createCategoryInline(val, done) {
  const name = typeof val === 'string' ? val.trim() : val
  if (!name) return
  try {
    const res = await api.post('categories/', { name })
    categories.value.push(res.data)
    const newOpt = { label: res.data.name, value: res.data.id }
    productForm.value.category = res.data.id
    if (done) done(newOpt, 'add-unique')
    $q.notify({ color: 'positive', message: `Category "${name}" created!`, icon: 'check_circle' })
  } catch {
    $q.notify({ color: 'negative', message: 'Failed to create category.', icon: 'error' })
  }
}

// Pluralize unit names correctly (Box→Boxes, Piece→Pieces, Sack→Sacks, etc.)
function pluralize(unit) {
  if (!unit) return ''
  const u = unit.trim()
  const lower = u.toLowerCase()
  // Words ending in x, ch, sh, s, z → add 'es'
  if (/(?:x|ch|sh|s|z)$/.test(lower)) return u + 'es'
  // Words ending in consonant + y → replace y with ies
  if (/[^aeiou]y$/.test(lower)) return u.slice(0, -1) + 'ies'
  // Default → add 's'
  return u + 's'
}

// Filtered products list
const filteredProducts = computed(() => {
  return products.value.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory =
      selectedCategory.value === null || product.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const columns = [
  {
    name: 'name',
    label: 'Product Name',
    field: 'name',
    align: 'left',
    sortable: true,
    headerClasses: 'table-header-bold text-weight-bolder text-dark',
  },
  {
    name: 'category_name',
    label: 'Category',
    field: 'category_name',
    align: 'left',
    sortable: true,
    headerClasses: 'table-header-bold text-weight-bolder text-dark',
  },
  {
    name: 'units',
    label: 'Unit Types',
    field: 'unit_retail_name',
    align: 'left',
    headerClasses: 'table-header-bold text-weight-bolder text-dark',
  },
  {
    name: 'retail_info',
    label: 'Retail / Loose Stock',
    field: 'price_per_kilo',
    align: 'left',
    sortable: true,
    headerClasses: 'table-header-bold text-weight-bolder text-dark',
  },
  {
    name: 'bulk_info',
    label: 'Bulk Stock',
    field: 'price_per_sack',
    align: 'left',
    sortable: true,
    headerClasses: 'table-header-bold text-weight-bolder text-dark',
  },
  {
    name: 'actions',
    label: 'Actions',
    field: 'id',
    align: 'center',
    headerClasses: 'table-header-bold text-weight-bolder text-dark',
  },
]

// API Requests
async function fetchData() {
  try {
    const prodRes = await api.get('products/', { params: { _t: Date.now() } })
    products.value = prodRes.data

    const catRes = await api.get('categories/', { params: { _t: Date.now() } })
    categories.value = catRes.data
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to fetch inventory stock records.',
      icon: 'error',
    })
  }
}

// Out of Stock and Low Stock logic helpers (Unified stock pool)
function isOutOfStock(row, type) {
  if (!row) return true
  const ratio = parseFloat(row.units_per_bulk || 50)
  const totalBase = parseFloat(row.stock_sacks || 0) * ratio + parseFloat(row.stock_kilos || 0)

  if (type === 'sacks') {
    return parseFloat(row.stock_sacks || 0) <= 0
  } else {
    if (row.unit_bulk_name && row.price_per_sack) {
      return totalBase <= 0
    }
    return parseFloat(row.stock_kilos || 0) <= 0
  }
}

function isLowStock(row, type) {
  if (!row) return false
  const threshold = parseFloat(row.low_stock_threshold || 5)
  const ratio = parseFloat(row.units_per_bulk || 50)
  const totalBase = parseFloat(row.stock_sacks || 0) * ratio + parseFloat(row.stock_kilos || 0)

  if (type === 'sacks') {
    const sacks = parseFloat(row.stock_sacks || 0)
    return sacks > 0 && sacks < threshold
  } else {
    // If bulk product, check if the entire unified pool is below the warning limit but greater than 0
    if (row.unit_bulk_name && row.price_per_sack) {
      return totalBase > 0 && totalBase < threshold
    }
    const kilos = parseFloat(row.stock_kilos || 0)
    return kilos > 0 && kilos < threshold
  }
}

// Dialog management
function openAddDialog() {
  productDialog.value.editMode = false
  productDialog.value.productId = null
  unitPresetMode.value = 'FEEDS'

  // Reset form to defaults
  productForm.value = {
    name: '',
    category: null,
    unit_bulk_name: 'Sack',
    unit_retail_name: 'Kilo',
    units_per_bulk: 50.0,
    price_per_sack: null,
    price_per_kilo: null,
    cost_per_sack: null,
    cost_per_kilo: null,
    stock_sacks: 0.0,
    stock_kilos: 0.0,
    low_stock_threshold: 5,
    is_active: true,
  }

  productDialog.value.open = true
}

function handleAddAnotherProduct() {
  successDialog.value.open = false
  openAddDialog()
}

function openEditDialog(row) {
  productDialog.value.editMode = true
  productDialog.value.productId = row.id

  // Infer preset mode or set to custom
  const bulk = row.unit_bulk_name
  const retail = row.unit_retail_name
  if (!bulk && (retail === 'Piece' || retail === 'Qty' || retail === 'Item')) {
    unitPresetMode.value = 'SINGLE'
  } else if (bulk === 'Case' && retail === 'Bottle') {
    unitPresetMode.value = 'DRINKS'
  } else if (bulk === 'Box' && retail === 'Piece') {
    unitPresetMode.value = 'BOX_PIECE'
  } else if (bulk === 'Sack' && retail === 'Kilo') {
    unitPresetMode.value = 'FEEDS'
  } else {
    unitPresetMode.value = 'CUSTOM'
  }

  // Clone selected product details to form
  productForm.value = {
    name: row.name,
    category: row.category,
    unit_bulk_name: row.unit_bulk_name || null,
    unit_retail_name: row.unit_retail_name || 'Piece',
    units_per_bulk: row.units_per_bulk ? parseFloat(row.units_per_bulk) : 50.0,
    price_per_sack: row.price_per_sack ? parseFloat(row.price_per_sack) : null,
    price_per_kilo: row.price_per_kilo ? parseFloat(row.price_per_kilo) : null,
    cost_per_sack: row.cost_per_sack ? parseFloat(row.cost_per_sack) : null,
    cost_per_kilo: row.cost_per_kilo ? parseFloat(row.cost_per_kilo) : null,
    stock_sacks: parseFloat(row.stock_sacks || 0),
    stock_kilos: parseFloat(row.stock_kilos || 0),
    low_stock_threshold: row.low_stock_threshold,
    is_active: row.is_active,
  }

  productDialog.value.open = true
}

async function saveProduct() {
  try {
    const payload = {
      name: productForm.value.name,
      category: productForm.value.category,
      unit_bulk_name: productForm.value.unit_bulk_name || null,
      unit_retail_name: productForm.value.unit_retail_name || 'Piece',
      units_per_bulk: productForm.value.unit_bulk_name
        ? parseFloat(productForm.value.units_per_bulk) || 50.0
        : null,
      price_per_sack:
        productForm.value.price_per_sack === '' ? null : productForm.value.price_per_sack,
      price_per_kilo:
        productForm.value.price_per_kilo === '' ? null : productForm.value.price_per_kilo,
      cost_per_sack:
        productForm.value.cost_per_sack === '' ? null : productForm.value.cost_per_sack,
      cost_per_kilo:
        productForm.value.cost_per_kilo === '' ? null : productForm.value.cost_per_kilo,
      stock_sacks: productForm.value.unit_bulk_name
        ? productForm.value.stock_sacks === ''
          ? 0.0
          : (productForm.value.stock_sacks ?? 0.0)
        : 0.0,
      stock_kilos: productForm.value.unit_bulk_name
        ? productDialog.value.editMode
          ? (productForm.value.stock_kilos ?? 0.0)
          : 0.0
        : productForm.value.stock_kilos === ''
          ? 0.0
          : (productForm.value.stock_kilos ?? 0.0),
      low_stock_threshold:
        productForm.value.low_stock_threshold === ''
          ? 5
          : (productForm.value.low_stock_threshold ?? 5),
      is_active: productForm.value.is_active,
    }

    if (productDialog.value.editMode) {
      const res = await api.put(`products/${productDialog.value.productId}/`, payload)
      $q.notify({
        color: 'positive',
        message: 'Product updated successfully!',
        icon: 'check',
      })
      const index = products.value.findIndex((p) => p.id === productDialog.value.productId)
      if (index > -1) {
        products.value[index] = res.data
      }
      productDialog.value.open = false
    } else {
      const res = await api.post('products/', payload)
      products.value.push(res.data)
      productDialog.value.open = false

      // Trigger Success Popup Dialog
      successDialog.value = {
        open: true,
        product: res.data,
      }
    }

    fetchData()
  } catch (err) {
    console.error(err)
    $q.notify({
      color: 'negative',
      message: 'Failed to save product records.',
      icon: 'error',
    })
  }
}

function confirmDeleteProduct(product) {
  deleteConfirmDialog.value = {
    open: true,
    product: product,
  }
}

async function executeDeleteProduct() {
  const product = deleteConfirmDialog.value.product
  if (!product) return

  try {
    await api.delete(`products/${product.id}/`)
    $q.notify({
      color: 'positive',
      message: `Product "${product.name}" deleted successfully!`,
      icon: 'delete_forever',
    })
    const index = products.value.findIndex((p) => p.id === product.id)
    if (index > -1) {
      products.value.splice(index, 1)
    }
    deleteConfirmDialog.value.open = false
  } catch (err) {
    console.error(err)
    deleteConfirmDialog.value.open = false
    $q.notify({
      color: 'negative',
      message: `Cannot delete "${product.name}" because it has recorded sales history. You can edit its status to Inactive instead.`,
      icon: 'warning',
      timeout: 5000,
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
.bg-red-1 {
  background-color: #ffebee !important;
}
.text-red {
  color: #c62828 !important;
}
.bg-indigo-10 {
  background-color: #1a237e !important;
}
.rounded-borders {
  border-radius: 4px;
}
:deep(.table-header-bold),
:deep(.q-table th) {
  font-weight: 800 !important;
  font-size: 0.93rem !important;
  color: #0f172a !important;
  letter-spacing: 0.01em;
}

:deep(.inventory-data-table th:last-child),
:deep(.inventory-data-table td:last-child) {
  position: sticky;
  right: 0;
  background-color: #ffffff !important;
  z-index: 2;
  box-shadow: -2px 0 6px rgba(0, 0, 0, 0.05);
}
</style>
