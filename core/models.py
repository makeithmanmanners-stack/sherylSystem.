from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=150)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tin = models.CharField(max_length=20, blank=True, null=True, verbose_name="TIN")
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Product(models.Model):
    sku = models.CharField(max_length=50, primary_key=True, verbose_name="SKU")
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wholesale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_quantity = models.IntegerField(default=0)
    min_stock = models.IntegerField(default=5)
    max_stock = models.IntegerField(default=100)
    barcode = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.TextField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    expiration_date = models.DateField(blank=True, null=True)
    image_url = models.ImageField(upload_to='products/', blank=True, null=True, max_length=500, verbose_name="Attach files")

    def __str__(self):
        return f"{self.name} ({self.sku})"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_profile')
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    reward_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee')
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Cashier', 'Cashier'),
        ('Salesman', 'Salesman'),
        ('Driver', 'Driver'),
        ('Helper', 'Helper'),
    ]
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    overtime = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    incentives = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.name} ({self.role})"

class Sale(models.Model):
    invoice_no = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    salesman = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    route = models.CharField(max_length=100, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    method = models.CharField(max_length=50, default='Cash')  # Cash, Credit, GCash, Maya, Bank
    status = models.CharField(max_length=20, default='Posted') # Draft, Posted, Voided

    def __str__(self):
        return self.invoice_no

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.sale.invoice_no} - {self.product.name} ({self.qty})"

class Trip(models.Model):
    date = models.DateField()
    truck_id = models.CharField(max_length=50)
    driver = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='driver_trips')
    helper = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='helper_trips')
    route = models.CharField(max_length=100)
    status = models.CharField(max_length=50, default='Pending') # Pending, Dispatched, Completed
    cash_collected = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    cash_predicted = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    shortage = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    logs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Trip {self.id} - {self.route} ({self.date})"

class TripItem(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty_loaded = models.IntegerField(default=0)
    qty_sold = models.IntegerField(default=0)
    qty_returned = models.IntegerField(default=0)

    def __str__(self):
        return f"Trip {self.trip.id} - {self.product.name}"

class PurchaseOrder(models.Model):
    po_no = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    status = models.CharField(max_length=50, default='Submitted') # Submitted, Approved, Received

    def __str__(self):
        return self.po_no

class PurchaseItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.purchase_order.po_no} - {self.product.name}"

class Expense(models.Model):
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.date})"

class AuditLog(models.Model):
    user = models.CharField(max_length=150, default='system')
    action = models.CharField(max_length=100)
    module = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.module} - {self.action} ({self.timestamp})"
