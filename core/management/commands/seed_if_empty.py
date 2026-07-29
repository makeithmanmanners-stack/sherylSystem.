from django.core.management.base import BaseCommand
from core.models import Category, Brand, Supplier, Product, Customer, Employee, Sale, SaleItem, Trip, TripItem, PurchaseOrder, Expense, AuditLog
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seeds database with default products and records if empty.'

    def handle(self, *args, **options):
        if Product.objects.count() > 0:
            self.stdout.write(self.style.SUCCESS(f"Database already contains {Product.objects.count()} products. Skipping initial seed."))
            return

        self.stdout.write("Database has 0 products. Seeding default inventory catalog...")

        # 1. Categories
        beverages, _ = Category.objects.get_or_create(name="Beverages", defaults={"description": "Soft drinks, beers, energy drinks, and water"})
        snacks, _ = Category.objects.get_or_create(name="Snacks", defaults={"description": "Chips, biscuits, candies, and crackers"})
        groceries, _ = Category.objects.get_or_create(name="Groceries", defaults={"description": "Canned goods, noodles, sauces, condiments"})
        household, _ = Category.objects.get_or_create(name="Household", defaults={"description": "Soaps, detergents, toiletries, and cleaners"})
        tobacco, _ = Category.objects.get_or_create(name="Tobacco & Liquor", defaults={"description": "Cigarettes, hard liquor, and spirits"})

        # 2. Brands
        coca_cola_brand, _ = Brand.objects.get_or_create(name="Coca-Cola Company")
        smb_brand, _ = Brand.objects.get_or_create(name="San Miguel Brewery")
        monde_brand, _ = Brand.objects.get_or_create(name="Monde Nissin")
        unilever_brand, _ = Brand.objects.get_or_create(name="Unilever")

        # 3. Suppliers
        coke_bottlers, _ = Supplier.objects.get_or_create(
            name="Coca-Cola Beverages PH",
            defaults={
                "company_name": "Coca-Cola Bottlers Philippines Inc.",
                "phone": "02-8866-2653",
                "email": "orders@coca-cola.com.ph",
                "address": "Manila Gateway, Taguig, Metro Manila",
                "tin": "000-111-222-000",
                "outstanding_balance": 45000.00
            }
        )
        smb_supplier, _ = Supplier.objects.get_or_create(
            name="San Miguel Brewery Inc.",
            defaults={
                "company_name": "San Miguel Corporation",
                "phone": "02-8632-3000",
                "email": "sales@smb.sanmiguel.com.ph",
                "address": "Ortigas Center, Pasig City",
                "tin": "111-222-333-000",
                "outstanding_balance": 125000.00
            }
        )
        monde_supplier, _ = Supplier.objects.get_or_create(
            name="Monde Nissin Corp",
            defaults={
                "company_name": "Monde Nissin Corporation",
                "phone": "02-8588-9100",
                "email": "sales@mondenissin.com",
                "address": "Sta. Rosa, Laguna",
                "tin": "222-333-444-000",
                "outstanding_balance": 0.00
            }
        )

        # 4. Products
        products_data = [
            {
                "sku": "COKE-1.5L",
                "name": "Coca-Cola Original 1.5L (Case of 12)",
                "brand": coca_cola_brand,
                "category": beverages,
                "cost_price": 550.00,
                "wholesale_price": 620.00,
                "retail_price": 660.00,
                "stock_quantity": 45,
                "min_stock": 10,
                "max_stock": 150,
                "barcode": "4800001001502",
                "supplier": coke_bottlers,
                "expiration_date": date.today() + timedelta(days=180),
                "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=600&q=80"
            },
            {
                "sku": "SPRITE-1.5L",
                "name": "Sprite Lemon-Lime 1.5L (Case of 12)",
                "brand": coca_cola_brand,
                "category": beverages,
                "cost_price": 540.00,
                "wholesale_price": 610.00,
                "retail_price": 650.00,
                "stock_quantity": 25,
                "min_stock": 10,
                "max_stock": 100,
                "barcode": "4800001001503",
                "supplier": coke_bottlers,
                "expiration_date": date.today() + timedelta(days=180),
                "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=600&q=80"
            },
            {
                "sku": "REDHORSE-1L",
                "name": "Red Horse Beer Extra Strong 1L (Case of 12)",
                "brand": smb_brand,
                "category": beverages,
                "cost_price": 1150.00,
                "wholesale_price": 1280.00,
                "retail_price": 1350.00,
                "stock_quantity": 60,
                "min_stock": 15,
                "max_stock": 200,
                "barcode": "4800011223301",
                "supplier": smb_supplier,
                "expiration_date": date.today() + timedelta(days=365),
                "image_url": "https://images.unsplash.com/photo-1566633806327-68e152aaf26d?auto=format&fit=crop&w=600&q=80"
            },
            {
                "sku": "PILSER-320",
                "name": "San Miguel Pale Pilsen 320ml (Case of 24)",
                "brand": smb_brand,
                "category": beverages,
                "cost_price": 980.00,
                "wholesale_price": 1080.00,
                "retail_price": 1150.00,
                "stock_quantity": 8,
                "min_stock": 15,
                "max_stock": 150,
                "barcode": "4800011223302",
                "supplier": smb_supplier,
                "expiration_date": date.today() + timedelta(days=365),
                "image_url": "https://images.unsplash.com/photo-1600788886242-5c96aabe3757?auto=format&fit=crop&w=600&q=80"
            },
            {
                "sku": "LUCKYME-PC",
                "name": "Lucky Me Pancit Canton Original 80g (Box of 72)",
                "brand": monde_brand,
                "category": groceries,
                "cost_price": 620.00,
                "wholesale_price": 680.00,
                "retail_price": 720.00,
                "stock_quantity": 35,
                "min_stock": 8,
                "max_stock": 80,
                "barcode": "4800022334401",
                "supplier": monde_supplier,
                "expiration_date": date.today() + timedelta(days=120),
                "image_url": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=600&q=80"
            },
            {
                "sku": "SAFEGUARD-W",
                "name": "Safeguard White Soap 130g (Pack of 36)",
                "brand": unilever_brand,
                "category": household,
                "cost_price": 1350.00,
                "wholesale_price": 1450.00,
                "retail_price": 1520.00,
                "stock_quantity": 18,
                "min_stock": 5,
                "max_stock": 50,
                "barcode": "480033445501",
                "supplier": monde_supplier,
                "expiration_date": date.today() + timedelta(days=730),
                "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=600&q=80"
            }
        ]

        for p_data in products_data:
            Product.objects.get_or_create(sku=p_data["sku"], defaults=p_data)

        # 5. Default Customers
        Customer.objects.get_or_create(
            name="Aling Nena's Sari-Sari Store",
            defaults={
                "contact": "09123456789",
                "email": "nena@gmail.com",
                "address": "Cagsalaosao, Calbayog City",
                "credit_limit": 15000.00,
                "credit_balance": 3400.00,
                "reward_points": 120
            }
        )

        # 6. Default Employees
        Employee.objects.get_or_create(name="Sheyde Vasquez", defaults={"role": "Admin", "phone": "09175558888", "base_salary": 30000.00, "status": "Active"})

        AuditLog.objects.create(user="system", action="Auto-Seed DB", module="System Setup", details="Seeded database with default product catalog.")
        self.stdout.write(self.style.SUCCESS("Database seeded successfully with default catalog."))
