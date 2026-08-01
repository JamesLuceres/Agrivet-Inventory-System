from django.core.management.base import BaseCommand
from store.models import Category, Product, Customer

class Command(BaseCommand):
    help = "Seeds database with initial sample data for Category, Product, and Customer models"

    def handle(self, *args, **kwargs):
        # Prevent double seeding
        if Category.objects.exists() or Product.objects.exists() or Customer.objects.exists():
            self.stdout.write(self.style.WARNING("Database already contains data. Seeding skipped."))
            return

        self.stdout.write("Seeding sample data...")

        # 1. Create Categories
        feeds = Category.objects.create(
            name="Feeds", 
            description="Animal livestock feeds for pigs, chickens, etc."
        )
        pet_food = Category.objects.create(
            name="Pet Food", 
            description="Food items for household pets."
        )
        rice = Category.objects.create(
            name="Rice (Bugas)", 
            description="Various varieties of rice sold by sack or kilo."
        )
        essentials = Category.objects.create(
            name="Essentials", 
            description="Veterinary medicines, tools, and basic store items."
        )

        self.stdout.write(self.style.SUCCESS("Created Categories: Feeds, Pet Food, Rice (Bugas), Essentials"))

        # 2. Create Products
        Product.objects.create(
            name="Piglet Starter (Sack/Kilo)",
            category=feeds,
            price_per_sack=1500.00,
            price_per_kilo=35.00,
            stock_sacks=10.00,
            stock_kilos=15.00,
            low_stock_threshold=5,
            is_active=True
        )

        Product.objects.create(
            name="Grown Pig Hog Feed",
            category=feeds,
            price_per_sack=1200.00,
            price_per_kilo=28.00,
            stock_sacks=8.00,
            stock_kilos=0.00,
            low_stock_threshold=5,
            is_active=True
        )

        Product.objects.create(
            name="Adult Dog Food",
            category=pet_food,
            price_per_sack=1800.00,
            price_per_kilo=95.00,
            stock_sacks=4.00,  # Below threshold
            stock_kilos=2.00,
            low_stock_threshold=5,
            is_active=True
        )

        Product.objects.create(
            name="Super Premium Dinorado Rice",
            category=rice,
            price_per_sack=2600.00,
            price_per_kilo=55.00,
            stock_sacks=20.00,
            stock_kilos=50.00,
            low_stock_threshold=8,
            is_active=True
        )

        self.stdout.write(self.style.SUCCESS("Created Products: Piglet Starter, Grown Pig Hog Feed, Adult Dog Food, Super Premium Dinorado Rice"))

        # 3. Create Customers
        Customer.objects.create(
            name="Mang Juan",
            contact_number="09171234567",
            total_utang=1500.00,
            notes="Regular feeds buyer. Pays credit balances bi-weekly."
        )

        Customer.objects.create(
            name="Aling Nena",
            contact_number="09187654321",
            total_utang=500.00,
            notes="Owns a small sari-sari store. Buys dog food."
        )

        self.stdout.write(self.style.SUCCESS("Created Customers: Mang Juan, Aling Nena"))
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
