from django.contrib import admin
from core.models import (
    Category, Brand, Supplier, Product, Customer, 
    Employee, Sale, SaleItem, Trip, TripItem, 
    PurchaseOrder, PurchaseItem, Expense, AuditLog
)

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'brand', 'cost_price', 'wholesale_price', 'retail_price', 'stock_quantity', 'min_stock')
    search_fields = ('sku', 'name', 'barcode')
    list_filter = ('category', 'brand', 'supplier')
    ordering = ('name',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'date', 'customer', 'salesman', 'total', 'method', 'status')
    search_fields = ('invoice_no', 'customer__name', 'route')
    list_filter = ('method', 'status', 'date')
    inlines = [SaleItemInline]

class TripItemInline(admin.TabularInline):
    model = TripItem
    extra = 0

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'truck_id', 'driver', 'helper', 'route', 'status', 'cash_collected')
    list_filter = ('status', 'date', 'truck_id')
    search_fields = ('route', 'driver__name', 'helper__name')
    inlines = [TripItemInline]

class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_no', 'date', 'supplier', 'total', 'status')
    list_filter = ('status', 'date')
    search_fields = ('po_no', 'supplier__name')
    inlines = [PurchaseItemInline]

# Basic registration for other models
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(Expense)
admin.site.register(AuditLog)

