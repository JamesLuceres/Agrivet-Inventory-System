<template>
  <q-page class="q-pa-lg">
    <!-- Header -->
    <div class="row items-center q-mb-lg justify-between">
      <div class="row items-center">
        <q-btn flat round dense icon="arrow_back" size="lg" color="blue-10" class="q-mr-md" @click="$router.push('/')">
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
        :rows-per-page-options="[10, 25, 50]"
        no-data-label="No items in inventory."
      >
        <!-- Category name -->
        <template v-slot:body-cell-category_name="props">
          <q-td :props="props">
            <q-badge color="indigo-1" text-color="indigo-10" class="text-weight-bold">
              {{ props.value }}
            </q-badge>
          </q-td>
        </template>

        <!-- Stock Sacks -->
        <template v-slot:body-cell-stock_sacks="props">
          <q-td :props="props" :class="isLowStock(props.row, 'sacks') ? 'bg-red-1 text-red text-weight-bold' : ''">
            {{ parseFloat(props.value) }}
            <q-badge color="red" text-color="white" class="q-ml-xs text-caption" v-if="isLowStock(props.row, 'sacks')">
              LOW
            </q-badge>
          </q-td>
        </template>

        <!-- Stock Kilos -->
        <template v-slot:body-cell-stock_kilos="props">
          <q-td :props="props" :class="isLowStock(props.row, 'kilos') ? 'bg-red-1 text-red text-weight-bold' : ''">
            {{ parseFloat(props.value) }}
            <q-badge color="red" text-color="white" class="q-ml-xs text-caption" v-if="isLowStock(props.row, 'kilos')">
              LOW
            </q-badge>
          </q-td>
        </template>

        <!-- Sack Price -->
        <template v-slot:body-cell-price_per_sack="props">
          <q-td :props="props" class="text-green-10 text-weight-bold">
            {{ props.value ? `₱${parseFloat(props.value).toFixed(2)}` : '-' }}
          </q-td>
        </template>

        <!-- Kilo Price -->
        <template v-slot:body-cell-price_per_kilo="props">
          <q-td :props="props" class="text-green-10 text-weight-bold">
            {{ props.value ? `₱${parseFloat(props.value).toFixed(2)}` : '-' }}
          </q-td>
        </template>

        <!-- Status -->
        <template v-slot:body-cell-is_active="props">
          <q-td :props="props" align="center">
            <q-badge :color="props.value ? 'positive' : 'negative'" text-color="white" class="text-weight-bold">
              {{ props.value ? 'Active' : 'Inactive' }}
            </q-badge>
          </q-td>
        </template>

        <!-- Actions -->
        <template v-slot:body-cell-actions="props">
          <q-td :props="props" align="center">
            <q-btn
              flat
              round
              dense
              color="primary"
              icon="edit"
              @click="openEditDialog(props.row)"
            >
              <q-tooltip>Edit Stock & Details</q-tooltip>
            </q-btn>
          </q-td>
        </template>
      </q-table>
    </q-card>

    <!-- Product Form Dialog (Add / Edit) -->
    <q-dialog v-model="productDialog.open" persistent>
      <q-card style="width: 500px; max-width: 90vw;">
        <q-card-section class="bg-indigo-10 text-white q-py-md">
          <div class="text-h6 text-weight-bold">{{ productDialog.editMode ? 'Edit Product details' : 'Add New Product' }}</div>
        </q-card-section>

        <q-card-section class="q-py-md row q-col-gutter-sm">
          <!-- Name -->
          <div class="col-12">
            <q-input v-model="productForm.name" label="Product Name" outlined dense :rules="[val => !!val || 'Name is required']" />
          </div>
          <!-- Category -->
          <div class="col-12">
            <q-select
              v-model="productForm.category"
              :options="formCategoryOptions"
              label="Select Category"
              outlined
              dense
              emit-value
              map-options
              :rules="[val => !!val || 'Category is required']"
            />
          </div>
          
          <!-- Prices -->
          <div class="col-6">
            <q-input v-model.number="productForm.price_per_sack" type="number" step="0.01" label="Price per Sack (₱)" outlined dense prefix="₱" />
          </div>
          <div class="col-6">
            <q-input v-model.number="productForm.price_per_kilo" type="number" step="0.01" label="Price per Kilo (₱)" outlined dense prefix="₱" />
          </div>

          <!-- Stock Levels -->
          <div class="col-6">
            <q-input v-model.number="productForm.stock_sacks" type="number" step="0.1" label="Stock Sacks" outlined dense />
          </div>
          <div class="col-6">
            <q-input v-model.number="productForm.stock_kilos" type="number" step="0.1" label="Stock Kilos" outlined dense />
          </div>

          <!-- Low Stock Threshold -->
          <div class="col-12">
            <q-input v-model.number="productForm.low_stock_threshold" type="number" label="Low Stock Warning Threshold (sacks/kilos limit)" outlined dense />
          </div>

          <!-- Active Switch (Only on Edit) -->
          <div class="col-12 q-pt-sm" v-if="productDialog.editMode">
            <q-toggle v-model="productForm.is_active" label="Product is Active" color="primary" />
          </div>
        </q-card-section>

        <q-card-actions align="right" class="q-px-md q-pb-md">
          <q-btn flat label="Cancel" color="grey-7" v-close-popup />
          <q-btn label="Save Product" color="primary" @click="saveProduct" :disable="!productForm.name || !productForm.category" />
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
  productId: null
})

const productForm = ref({
  name: '',
  category: null,
  price_per_sack: null,
  price_per_kilo: null,
  stock_sacks: 0.0,
  stock_kilos: 0.0,
  low_stock_threshold: 5,
  is_active: true
})

// Mapped selections
const categoryOptions = computed(() => {
  const list = categories.value.map(cat => ({ label: cat.name, value: cat.id }))
  return [{ label: 'All Categories', value: null }, ...list]
})

const formCategoryOptions = computed(() => {
  return categories.value.map(cat => ({ label: cat.name, value: cat.id }))
})

// Filtered products list
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesCategory = selectedCategory.value === null || product.category === selectedCategory.value
    return matchesSearch && matchesCategory
  })
})

const columns = [
  { name: 'name', label: 'Product Name', field: 'name', align: 'left', sortable: true },
  { name: 'category_name', label: 'Category', field: 'category_name', align: 'left', sortable: true },
  { name: 'stock_sacks', label: 'Sack Stock', field: 'stock_sacks', align: 'right', sortable: true },
  { name: 'stock_kilos', label: 'Kilo Stock', field: 'stock_kilos', align: 'right', sortable: true },
  { name: 'price_per_sack', label: 'Sack Price', field: 'price_per_sack', align: 'right', sortable: true },
  { name: 'price_per_kilo', label: 'Kilo Price', field: 'price_per_kilo', align: 'right', sortable: true },
  { name: 'is_active', label: 'Status', field: 'is_active', align: 'center', sortable: true },
  { name: 'actions', label: 'Actions', field: 'id', align: 'center' }
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
      icon: 'error'
    })
  }
}

// Low Stock logic helper
function isLowStock(row, type) {
  const threshold = parseInt(row.low_stock_threshold || 5)
  if (type === 'sacks') {
    return parseFloat(row.stock_sacks) < threshold
  } else {
    return parseFloat(row.stock_kilos) < threshold
  }
}

// Dialog management
function openAddDialog() {
  productDialog.value.editMode = false
  productDialog.value.productId = null
  
  // Reset form to defaults
  productForm.value = {
    name: '',
    category: null,
    price_per_sack: null,
    price_per_kilo: null,
    stock_sacks: 0.0,
    stock_kilos: 0.0,
    low_stock_threshold: 5,
    is_active: true
  }
  
  productDialog.value.open = true
}

function openEditDialog(row) {
  productDialog.value.editMode = true
  productDialog.value.productId = row.id
  
  // Clone selected product details to form
  productForm.value = {
    name: row.name,
    category: row.category,
    price_per_sack: row.price_per_sack ? parseFloat(row.price_per_sack) : null,
    price_per_kilo: row.price_per_kilo ? parseFloat(row.price_per_kilo) : null,
    stock_sacks: parseFloat(row.stock_sacks),
    stock_kilos: parseFloat(row.stock_kilos),
    low_stock_threshold: row.low_stock_threshold,
    is_active: row.is_active
  }
  
  productDialog.value.open = true
}

async function saveProduct() {
  try {
    const payload = {
      name: productForm.value.name,
      category: productForm.value.category,
      price_per_sack: productForm.value.price_per_sack === '' ? null : productForm.value.price_per_sack,
      price_per_kilo: productForm.value.price_per_kilo === '' ? null : productForm.value.price_per_kilo,
      stock_sacks: productForm.value.stock_sacks === '' ? 0.0 : (productForm.value.stock_sacks ?? 0.0),
      stock_kilos: productForm.value.stock_kilos === '' ? 0.0 : (productForm.value.stock_kilos ?? 0.0),
      low_stock_threshold: productForm.value.low_stock_threshold === '' ? 5 : (productForm.value.low_stock_threshold ?? 5),
      is_active: productForm.value.is_active
    }

    if (productDialog.value.editMode) {
      const res = await api.put(`products/${productDialog.value.productId}/`, payload)
      $q.notify({
        color: 'positive',
        message: 'Product updated successfully!',
        icon: 'check'
      })
      // Update local state instantly to avoid delay/caching
      const index = products.value.findIndex(p => p.id === productDialog.value.productId)
      if (index > -1) {
        products.value[index] = res.data
      }
    } else {
      const res = await api.post('products/', payload)
      $q.notify({
        color: 'positive',
        message: 'Product added successfully!',
        icon: 'check'
      })
      // Insert in local state instantly
      products.value.push(res.data)
    }

    productDialog.value.open = false
    fetchData()
  } catch {
    $q.notify({
      color: 'negative',
      message: 'Failed to save product records.',
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
</style>
