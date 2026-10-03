from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from store.models import Category, Product, Customer, Transaction, TransactionItem


class AgrivetStoreQATestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # 1. Setup Categories
        self.cat_feeds = Category.objects.create(name="Feeds")
        self.cat_services = Category.objects.create(name="Services & Others")

        # 2. Setup Physical Feed Product (Sack = 50 kg)
        # Total initial stock: 2 Sacks and 0 loose kilos = 100 kg
        self.feed_product = Product.objects.create(
            name="B-Meg Hog Starter Pellet",
            category=self.cat_feeds,
            price_per_kilo=Decimal("35.00"),
            price_per_sack=Decimal("1680.00"),
            stock_sacks=Decimal("2.00"),
            stock_kilos=Decimal("0.00"),
            low_stock_threshold=5,
            unit_bulk_name="sack",
            unit_retail_name="kilo",
            units_per_bulk=Decimal("50.00"),
            is_service=False,
            is_active=True,
        )

        # 3. Setup Service Product (GCash)
        self.gcash_product = Product.objects.create(
            name="GCash (Cash In / Cash Out)",
            category=self.cat_services,
            price_per_kilo=Decimal("0.00"),
            stock_sacks=Decimal("0.00"),
            stock_kilos=Decimal("999999.00"),
            unit_bulk_name="service",
            unit_retail_name="txn",
            units_per_bulk=Decimal("1.00"),
            is_service=True,
            is_active=True,
        )

        # 4. Setup Customer
        self.customer = Customer.objects.create(
            name="Mang Juan Dela Cruz",
            contact_number="0918-123-4567",
            total_utang=Decimal("0.00"),
        )

    def test_product_unified_stock_depletion_sack(self):
        """Test buying 1 Sack (50kg) depletes physical inventory by 1 sack."""
        payload = {
            "transaction_type": "CASH",
            "total_amount": "1680.00",
            "amount_paid": "2000.00",
            "change_given": "320.00",
            "items": [
                {
                    "product": self.feed_product.id,
                    "unit_type": "SACK",
                    "quantity": "1.00",
                    "unit_price": "1680.00",
                    "subtotal": "1680.00",
                }
            ],
        }
        res = self.client.post("/api/transactions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.feed_product.refresh_from_db()
        self.assertEqual(self.feed_product.stock_sacks, Decimal("1.00"))
        self.assertEqual(self.feed_product.stock_kilos, Decimal("0.00"))

    def test_product_unified_stock_depletion_retail_kilo(self):
        """Test buying 5 Kilos from 2 sacks (100kg total) leaves 1 sack and 45 kilos (95kg)."""
        payload = {
            "transaction_type": "CASH",
            "total_amount": "175.00",
            "amount_paid": "200.00",
            "change_given": "25.00",
            "items": [
                {
                    "product": self.feed_product.id,
                    "unit_type": "KILO",
                    "quantity": "5.00",
                    "unit_price": "35.00",
                    "subtotal": "175.00",
                }
            ],
        }
        res = self.client.post("/api/transactions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.feed_product.refresh_from_db()
        # 100 kg - 5 kg = 95 kg -> 1 sack (50kg) + 45 kilos
        self.assertEqual(self.feed_product.stock_sacks, Decimal("1.00"))
        self.assertEqual(self.feed_product.stock_kilos, Decimal("45.00"))

    def test_service_gcash_transaction_does_not_deplete_stock(self):
        """Test GCash Cash In/Out does not decrement inventory."""
        initial_gcash_stock = self.gcash_product.stock_kilos
        payload = {
            "transaction_type": "CASH",
            "total_amount": "1020.00",
            "amount_paid": "1020.00",
            "change_given": "0.00",
            "items": [
                {
                    "product": self.gcash_product.id,
                    "unit_type": "ITEM",
                    "quantity": "1.00",
                    "unit_price": "1020.00",
                    "subtotal": "1020.00",
                    "notes": "Amount: ₱1,000.00 • Fee: ₱20.00",
                }
            ],
        }
        res = self.client.post("/api/transactions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.gcash_product.refresh_from_db()
        self.assertEqual(self.gcash_product.stock_kilos, initial_gcash_stock)

        # Verify notes are saved
        item = TransactionItem.objects.filter(transaction_id=res.data["id"]).first()
        self.assertIsNotNone(item)
        self.assertIn("Fee: ₱20.00", item.notes)

    def test_credit_transaction_increases_customer_debt(self):
        """Test Credit transaction increases customer's total_utang."""
        self.assertEqual(self.customer.total_utang, Decimal("0.00"))
        payload = {
            "transaction_type": "CREDIT",
            "customer": self.customer.id,
            "total_amount": "500.00",
            "amount_paid": "0.00",
            "change_given": "0.00",
            "items": [
                {
                    "product": self.feed_product.id,
                    "unit_type": "KILO",
                    "quantity": "10.00",
                    "unit_price": "50.00",
                    "subtotal": "500.00",
                }
            ],
        }
        res = self.client.post("/api/transactions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_utang, Decimal("500.00"))

    def test_customer_debt_repayment_via_debt_payment_tx(self):
        """Test paying off credit reduces debt."""
        self.customer.total_utang = Decimal("500.00")
        self.customer.save()

        # Patch customer total_utang
        patch_res = self.client.patch(
            f"/api/customers/{self.customer.id}/",
            {"total_utang": "300.00"},
            format="json",
        )
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)

        # Record payment transaction
        tx_res = self.client.post(
            "/api/transactions/",
            {
                "transaction_type": "DEBT_PAYMENT",
                "customer": self.customer.id,
                "total_amount": "200.00",
                "amount_paid": "200.00",
                "change_given": "0.00",
                "items": [],
            },
            format="json",
        )
        self.assertEqual(tx_res.status_code, status.HTTP_201_CREATED)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_utang, Decimal("300.00"))

    def test_low_stock_alert_endpoint(self):
        """Test low stock endpoint filters products below threshold."""
        # Set stock to 0 sacks, 2 kilos (threshold is 5)
        self.feed_product.stock_sacks = Decimal("0.00")
        self.feed_product.stock_kilos = Decimal("2.00")
        self.feed_product.save()

        res = self.client.get("/api/products/low-stock/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        low_ids = [p["id"] for p in res.data]
        self.assertIn(self.feed_product.id, low_ids)
        # Service product should not be in low stock
        self.assertNotIn(self.gcash_product.id, low_ids)

    def test_daily_and_monthly_summary_endpoints(self):
        """Test summary endpoints return valid HTTP 200 with totals."""
        res_daily = self.client.get("/api/transactions/daily-summary/")
        self.assertEqual(res_daily.status_code, status.HTTP_200_OK)
        self.assertIn("total_shift_sales", res_daily.data)
        self.assertIn("total_physical_cash", res_daily.data)

        res_monthly = self.client.get("/api/transactions/monthly-summary/")
        self.assertEqual(res_monthly.status_code, status.HTTP_200_OK)
        self.assertIn("total_revenue", res_monthly.data)

    def test_delete_transaction_restores_stock_and_credit(self):
        """Test deleting a sale restores inventory stock and reverses customer debt."""
        # 1. Create a credit sale of 1 sack (50kg)
        initial_sacks = self.feed_product.stock_sacks  # 2.00
        payload = {
            "transaction_type": "CREDIT",
            "customer": self.customer.id,
            "total_amount": "1680.00",
            "amount_paid": "0.00",
            "change_given": "0.00",
            "items": [
                {
                    "product": self.feed_product.id,
                    "unit_type": "SACK",
                    "quantity": "1.00",
                    "unit_price": "1680.00",
                    "subtotal": "1680.00",
                }
            ],
        }
        res = self.client.post("/api/transactions/", payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        tx_id = res.data["id"]

        # Verify stock decreased and debt increased
        self.feed_product.refresh_from_db()
        self.customer.refresh_from_db()
        self.assertEqual(self.feed_product.stock_sacks, initial_sacks - Decimal("1.00"))
        self.assertEqual(self.customer.total_utang, Decimal("1680.00"))

        # 2. Delete / void the transaction
        del_res = self.client.delete(f"/api/transactions/{tx_id}/")
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)

        # 3. Verify stock is restored back to 2 sacks and customer debt is reversed back to 0
        self.feed_product.refresh_from_db()
        self.customer.refresh_from_db()
        self.assertEqual(self.feed_product.stock_sacks, initial_sacks)
        self.assertEqual(self.customer.total_utang, Decimal("0.00"))
        self.assertFalse(Transaction.objects.filter(id=tx_id).exists())
