import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_erp.settings')
django.setup()

from core.models import Category, Brand, Supplier, Product, Customer, Employee, Sale, SaleItem, Trip, TripItem, PurchaseOrder, PurchaseItem, Expense, AuditLog
from datetime import datetime, date, timedelta

print("Seeding database...")

# Clear existing data
Category.objects.all().delete()
Brand.objects.all().delete()
Supplier.objects.all().delete()
Product.objects.all().delete()
Customer.objects.all().delete()
Employee.objects.all().delete()
Sale.objects.all().delete()
Trip.objects.all().delete()
PurchaseOrder.objects.all().delete()
Expense.objects.all().delete()
AuditLog.objects.all().delete()

# 1. Categories
beverages = Category.objects.create(name="Beverages", description="Soft drinks, beers, energy drinks, and water")
snacks = Category.objects.create(name="Snacks", description="Chips, biscuits, candies, and crackers")
groceries = Category.objects.create(name="Groceries", description="Canned goods, noodles, sauces, condiments")
household = Category.objects.create(name="Household", description="Soaps, detergents, toiletries, and cleaners")
tobacco = Category.objects.create(name="Tobacco & Liquor", description="Cigarettes, hard liquor, and spirits")

# 2. Brands
coca_cola_brand = Brand.objects.create(name="Coca-Cola Company")
smb_brand = Brand.objects.create(name="San Miguel Brewery")
pepsi_brand = Brand.objects.create(name="PepsiCo")
monde_brand = Brand.objects.create(name="Monde Nissin")
unilever_brand = Brand.objects.create(name="Unilever")
pmftc_brand = Brand.objects.create(name="PMFTC Inc.")

# 3. Suppliers
coke_bottlers = Supplier.objects.create(
    name="Coca-Cola Beverages PH",
    company_name="Coca-Cola Bottlers Philippines Inc.",
    phone="02-8866-2653",
    email="orders@coca-cola.com.ph",
    address="Manila Gateway, Taguig, Metro Manila",
    tin="000-111-222-000",
    outstanding_balance=45000.00
)
smb_distributor = Supplier.objects.create(
    name="San Miguel Brewery Inc.",
    company_name="San Miguel Corporation",
    phone="02-8632-3000",
    email="distributors@smb.sanmiguel.com.ph",
    address="Ortigas Center, Pasig City",
    tin="111-222-333-000",
    outstanding_balance=125000.00
)
monde_dist = Supplier.objects.create(
    name="Monde Nissin Corp",
    company_name="Monde Nissin Corporation",
    phone="02-8588-9100",
    email="sales@mondenissin.com",
    address="Sta. Rosa, Laguna",
    tin="222-333-444-000",
    outstanding_balance=0.00
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
        "supplier": smb_distributor,
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
        "stock_quantity": 8, # Low Stock!
        "min_stock": 15,
        "max_stock": 150,
        "barcode": "4800011223302",
        "supplier": smb_distributor,
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
        "supplier": monde_dist,
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
        "barcode": "4800033445501",
        "supplier": monde_dist,
        "expiration_date": date.today() + timedelta(days=730),
        "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=600&q=80"
    },
]

for p_item in products_data:
    Product.objects.create(**p_item)

# 5. Customers
Customer.objects.create(
    name="Aling Nena's Sari-Sari Store",
    contact="09123456789",
    email="nena@gmail.com",
    address="Cagsalaosao, Calbayog City",
    credit_limit=15000.00,
    credit_balance=3400.00,
    reward_points=120
)
Customer.objects.create(
    name="Mang Tomas Minimart",
    contact="09876543210",
    email="tomas@minimart.ph",
    address="Rawis, Calbayog City",
    credit_limit=30000.00,
    credit_balance=0.00,
    reward_points=450
)
Customer.objects.create(
    name="Tita Baby's Wholesale Outlet",
    contact="09223334444",
    email="baby@outlook.com",
    address="Oquendo, Calbayog City",
    credit_limit=10000.00,
    credit_balance=850.00,
    reward_points=75
)

# 6. Employees
salesman = Employee.objects.create(name="Juan Dela Cruz", role="Salesman", phone="09331112222", base_salary=15000.00, status="Active")
driver = Employee.objects.create(name="Pedro Penduko", role="Driver", phone="09332223333", base_salary=12000.00, status="Active")
helper = Employee.objects.create(name="Cardo Dalisay", role="Helper", phone="09333334444", base_salary=10000.00, status="Active")
admin = Employee.objects.create(name="Sheryl Vasquez", role="Admin", phone="09175558888", base_salary=30000.00, status="Active")

# 7. Audit Trail
AuditLog.objects.create(user="system", action="Database Seeding", module="System Setup", details="Successfully populated system tables with initial demonstration records.")

# 8. Create a sample past trip and invoice to show statistics
trip = Trip.objects.create(
    date=date.today() - timedelta(days=1),
    truck_id="TRUCK-A (ELF-4W)",
    driver=driver,
    helper=helper,
    route="Route 1 - Cagsalaosao City Center",
    status="Completed",
    cash_predicted=2800.00,
    cash_collected=2800.00,
    shortage=0.00,
    logs="Trip reconciled automatically. Helper bonus (50) and Driver bonus (100) added."
)
coke = Product.objects.get(sku="COKE-1.5L")
TripItem.objects.create(trip=trip, product=coke, qty_loaded=10, qty_sold=8, qty_returned=2)

sale = Sale.objects.create(
    invoice_no="INV-2026-0001",
    customer=Customer.objects.get(name="Aling Nena's Sari-Sari Store"),
    salesman=salesman,
    route="Route 1 - Cagsalaosao City Center",
    subtotal=4960.00,
    tax=595.20,
    total=5555.20,
    method="Credit",
    status="Posted"
)
SaleItem.objects.create(sale=sale, product=coke, qty=8, price=620.00, total=4960.00)

print("Database seeding completed successfully!")
