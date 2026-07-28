from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.models import Category, Brand, Supplier, Product, Customer, Employee, Sale, SaleItem, Trip, TripItem, PurchaseOrder, PurchaseItem, Expense, AuditLog
import json
from decimal import Decimal
from datetime import datetime, date
import barcode
from barcode.writer import ImageWriter
import qrcode
from io import BytesIO
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Helper function to serialize model objects into dictionaries
def serialize_obj(obj):
    if isinstance(obj, (Decimal, float)):
        return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj

def serialize_model(model_obj):
    if not model_obj:
        return None
    data = {}
    for field in model_obj._meta.fields:
        val = getattr(model_obj, field.name)
        if isinstance(val, (Decimal, float)):
            data[field.name] = float(val)
        elif isinstance(val, (datetime, date)):
            data[field.name] = val.isoformat()
        elif hasattr(val, 'pk'):
            data[field.name] = val.pk
        else:
            data[field.name] = val
    return data

def get_current_state():
    state = {
        "categories": [serialize_model(c) for c in Category.objects.all()],
        "brands": [serialize_model(b) for b in Brand.objects.all()],
        "suppliers": [serialize_model(s) for s in Supplier.objects.all()],
        "customers": [serialize_model(c) for c in Customer.objects.all()],
        "employees": [serialize_model(e) for e in Employee.objects.all()],
        "expenses": [serialize_model(e) for e in Expense.objects.all()],
        "audit_logs": [serialize_model(a) for a in AuditLog.objects.order_by('-timestamp')[:50]],
    }
    
    # Products
    products = []
    for p in Product.objects.all():
        p_data = serialize_model(p)
        p_data["category_name"] = p.category.name if p.category else ""
        p_data["brand_name"] = p.brand.name if p.brand else ""
        p_data["supplier_name"] = p.supplier.name if p.supplier else ""
        products.append(p_data)
    state["products"] = products

    # Sales
    sales = []
    for s in Sale.objects.order_by('-date'):
        s_data = serialize_model(s)
        s_data["customer_id"] = s.customer.id if s.customer else None
        s_data["customer_name"] = s.customer.name if s.customer else "Walk-in"
        s_data["salesman_name"] = s.salesman.name if s.salesman else "N/A"
        s_data["items"] = [
            {
                "product_sku": item.product.sku,
                "product_name": item.product.name,
                "qty": item.qty,
                "price": float(item.price),
                "total": float(item.total)
            }
            for item in s.items.all()
        ]
        sales.append(s_data)
    state["sales"] = sales

    # Trips
    trips = []
    for t in Trip.objects.order_by('-date'):
        t_data = serialize_model(t)
        t_data["driver_name"] = t.driver.name if t.driver else "N/A"
        t_data["helper_name"] = t.helper.name if t.helper else "N/A"
        t_data["items"] = [
            {
                "product_sku": item.product.sku,
                "product_name": item.product.name,
                "qty_loaded": item.qty_loaded,
                "qty_sold": item.qty_sold,
                "qty_returned": item.qty_returned
            }
            for item in t.items.all()
        ]
        trips.append(t_data)
    state["trips"] = trips

    # Purchase Orders
    pos = []
    for po in PurchaseOrder.objects.order_by('-date'):
        po_data = serialize_model(po)
        po_data["supplier_name"] = po.supplier.name if po.supplier else "N/A"
        po_data["items"] = [
            {
                "product_sku": item.product.sku,
                "product_name": item.product.name,
                "qty": item.qty,
                "cost": float(item.cost),
                "total": float(item.total)
            }
            for item in po.items.all()
        ]
        pos.append(po_data)
    state["purchase_orders"] = pos

    return state

@login_required(login_url='login')
def index(request):
    emp = getattr(request.user, 'employee', None)
    if not request.user.is_superuser and (not emp or emp.role != 'Admin'):
        cust = getattr(request.user, 'customer_profile', None)
        if cust:
            return redirect('customer_portal')
        return HttpResponse("Access Denied: Admin privileges required.", status=403)
    return render(request, 'index.html')

def store(request):
    if request.user.is_authenticated:
        cust = getattr(request.user, 'customer_profile', None)
        if cust:
            return redirect('customer_portal')
    return render(request, 'store.html')

def login_view(request):
    if request.user.is_authenticated:
        cust = getattr(request.user, 'customer_profile', None)
        if cust:
            return redirect('customer_portal')
        return redirect('admin_portal')
    
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            cust = getattr(user, 'customer_profile', None)
            if cust:
                return redirect('customer_portal')
            return redirect('admin_portal')
        else:
            error_message = "Invalid username or password."
            
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def customer_portal(request):
    cust = getattr(request.user, 'customer_profile', None)
    if not cust:
        if request.user.is_superuser:
            return redirect('admin_portal')
        return HttpResponse("You are not registered as a customer in the system.", status=403)
        
    return render(request, 'customer_portal.html', {'customer': cust})

def signup_view(request):
    if request.user.is_authenticated:
        cust = getattr(request.user, 'customer_profile', None)
        if cust:
            return redirect('customer_portal')
        return redirect('admin_portal')
        
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        if password != confirm_password:
            error_message = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error_message = "Username is already taken."
        else:
            try:
                user = User.objects.create_user(username=username, password=password, email=email)
                customer = Customer.objects.create(
                    user=user,
                    name=name,
                    contact=contact,
                    email=email,
                    address=address,
                    credit_limit=10000.00,
                    credit_balance=0.00,
                    reward_points=0
                )
                login(request, user)
                return redirect('customer_portal')
            except Exception as e:
                error_message = "Error creating account: " + str(e)
                
    return render(request, 'signup.html', {'error_message': error_message})

@csrf_exempt
def api_state(request):
    if request.method == 'GET':
        return JsonResponse(get_current_state())
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get("action")
            
            # Action Handlers
            if action == "create_sale":
                # Create sale record
                invoice_no = data.get("invoice_no")
                cust_id = data.get("customer_id")
                emp_id = data.get("salesman_id")
                route = data.get("route")
                subtotal = Decimal(str(data.get("subtotal", 0)))
                tax = Decimal(str(data.get("tax", 0)))
                total = Decimal(str(data.get("total", 0)))
                method = data.get("method", "Cash")
                status = data.get("status", "Posted")
                
                customer = Customer.objects.filter(id=cust_id).first() if cust_id else None
                salesman = Employee.objects.filter(id=emp_id).first() if emp_id else None
                
                sale = Sale.objects.create(
                    invoice_no=invoice_no,
                    customer=customer,
                    salesman=salesman,
                    route=route,
                    subtotal=subtotal,
                    tax=tax,
                    total=total,
                    method=method,
                    status=status
                )
                
                # Handle customer accounts credit & loyalty points
                if customer:
                    if method == "Credit":
                        customer.credit_balance += total
                    customer.save()
                
                # Create sale items and deduct inventory stock
                items = data.get("items", [])
                for item in items:
                    prod = Product.objects.filter(sku=item.get("product_sku")).first()
                    if prod:
                        qty = int(item.get("qty", 1))
                        price = Decimal(str(item.get("price", 0)))
                        item_total = Decimal(str(item.get("total", 0)))
                        
                        SaleItem.objects.create(
                            sale=sale,
                            product=prod,
                            qty=qty,
                            price=price,
                            total=item_total
                        )
                        
                        # Deduct inventory stock if POS / direct sale
                        if status == "Posted":
                            prod.stock_quantity -= qty
                            prod.save()
                
                AuditLog.objects.create(
                    user=request.user.username if request.user.is_authenticated else "system",
                    action="Create Sale",
                    module="Sales",
                    details=f"Created Invoice {invoice_no} worth PHP {total:.2f}. Method: {method}. Status: {status}."
                )

            elif action == "approve_sale":
                invoice_no = data.get("invoice_no")
                sale = Sale.objects.filter(invoice_no=invoice_no).first()
                if sale and sale.status == "Draft":
                    for item in sale.items.all():
                        if item.product and item.product.stock_quantity < item.qty:
                            return JsonResponse({"success": False, "error": f"Insufficient stock for {item.product.name}."})
                    
                    for item in sale.items.all():
                        if item.product:
                            item.product.stock_quantity -= item.qty
                            item.product.save()
                    
                    sale.status = "Posted"
                    sale.save()
                    
                    if sale.customer:
                        if sale.method == "Credit":
                            sale.customer.credit_balance += sale.total
                        sale.customer.save()
                        
                    AuditLog.objects.create(
                        user=request.user.username if request.user.is_authenticated else "system",
                        action="Approve Draft Order",
                        module="Sales",
                        details=f"Approved and posted draft order {sale.invoice_no} for {sale.customer.name if sale.customer else 'Walk-in'}."
                    )
                    return JsonResponse({"success": True})
                return JsonResponse({"success": False, "error": "Sale not found or not in Draft status."})

            elif action == "create_trip":
                # Create trip
                truck_id = data.get("truck_id")
                driver_id = data.get("driver_id")
                helper_id = data.get("helper_id")
                route = data.get("route")
                trip_date = data.get("date", date.today().isoformat())
                
                driver = Employee.objects.filter(id=driver_id).first()
                helper = Employee.objects.filter(id=helper_id).first()
                
                trip = Trip.objects.create(
                    date=datetime.strptime(trip_date, "%Y-%m-%d").date(),
                    truck_id=truck_id,
                    driver=driver,
                    helper=helper,
                    route=route,
                    status="Pending"
                )
                
                # Add loaded products
                items = data.get("items", [])
                for item in items:
                    prod = Product.objects.filter(sku=item.get("product_sku")).first()
                    if prod:
                        qty_loaded = int(item.get("qty_loaded", 0))
                        TripItem.objects.create(
                            trip=trip,
                            product=prod,
                            qty_loaded=qty_loaded
                        )
                        
                        # Deduct load from warehouse stock immediately on dispatch/load
                        prod.stock_quantity -= qty_loaded
                        prod.save()

                AuditLog.objects.create(
                    user=request.user.username if request.user.is_authenticated else "system",
                    action="Create Dispatch Trip",
                    module="Logistics",
                    details=f"Created trip #{trip.id} to route '{route}' using {truck_id}."
                )

            elif action == "dispatch_trip":
                trip_id = data.get("trip_id")
                trip = Trip.objects.filter(id=trip_id).first()
                if trip:
                    trip.status = "Dispatched"
                    trip.save()
                    AuditLog.objects.create(
                        user=request.user.username if request.user.is_authenticated else "system",
                        action="Dispatch Trip",
                        module="Logistics",
                        details=f"Dispatched trip #{trip.id} to route '{trip.route}'."
                    )

            elif action == "deliver_trip":
                trip_id = data.get("trip_id")
                trip = Trip.objects.filter(id=trip_id).first()
                if trip:
                    trip.status = "Delivered"
                    trip.save()
                    AuditLog.objects.create(
                        user=request.user.username if request.user.is_authenticated else "system",
                        action="Deliver Trip",
                        module="Logistics",
                        details=f"Driver marked trip #{trip.id} as Delivered."
                    )

            elif action == "reconcile_trip":
                trip_id = data.get("trip_id")
                cash_collected = Decimal(str(data.get("cash_collected", 0)))
                cash_predicted = Decimal(str(data.get("cash_predicted", 0)))
                shortage = Decimal(str(data.get("shortage", 0)))
                logs = data.get("logs", "")
                
                trip = Trip.objects.filter(id=trip_id).first()
                if trip:
                    trip.status = "Completed"
                    trip.cash_collected = cash_collected
                    trip.cash_predicted = cash_predicted
                    trip.shortage = shortage
                    trip.logs = logs
                    trip.save()
                    
                    # Update Trip Items and returns to stock
                    items = data.get("items", [])
                    for item in items:
                        prod = Product.objects.filter(sku=item.get("product_sku")).first()
                        trip_item = TripItem.objects.filter(trip=trip, product=prod).first()
                        if trip_item:
                            qty_sold = int(item.get("qty_sold", 0))
                            qty_returned = int(item.get("qty_returned", 0))
                            
                            trip_item.qty_sold = qty_sold
                            trip_item.qty_returned = qty_returned
                            trip_item.save()
                            
                            # Add returned goods back to warehouse stock
                            if prod:
                                prod.stock_quantity += qty_returned
                                prod.save()
                    
                    # Add bonuses to payroll running incentives
                    if trip.driver:
                        trip.driver.incentives += Decimal("100.00")
                        trip.driver.save()
                    if trip.helper:
                        trip.helper.incentives += Decimal("50.00")
                        trip.helper.save()
                    
                    # Also log the driver trip completed as sale salesman commission if they did direct sales
                    # Let's say a salesman is tied to this trip route, let's look for them
                    salesmen = Employee.objects.filter(role="Salesman")
                    for sm in salesmen:
                        # Find sales created today for this route
                        sales = Sale.objects.filter(route=trip.route, date__date=date.today())
                        route_sales_total = sum(s.total for s in sales)
                        # Add 2% commission to salesman's payroll incentives
                        sm.incentives += route_sales_total * Decimal("0.02")
                        sm.save()

                    AuditLog.objects.create(
                        user=request.user.username if request.user.is_authenticated else "system",
                        action="Reconcile Trip",
                        module="Logistics",
                        details=f"Reconciled trip #{trip.id}. Predicted Cash: {cash_predicted:.2f}, Collected: {cash_collected:.2f}, Shortage: {shortage:.2f}."
                    )

            elif action == "post_payment":
                cust_id = data.get("customer_id")
                amount = Decimal(str(data.get("amount", 0)))
                method = data.get("method", "Cash")
                ref = data.get("reference", "")
                
                customer = Customer.objects.filter(id=cust_id).first()
                if customer:
                    customer.credit_balance -= amount
                    customer.save()
                    
                    AuditLog.objects.create(
                        user=request.user.username if request.user.is_authenticated else "system",
                        action="Post Customer Payment",
                        module="Cashier",
                        details=f"Received PHP {amount:.2f} from {customer.name} via {method}. Ref: {ref}."
                    )

            elif action == "create_po":
                po_no = data.get("po_no")
                supplier_id = data.get("supplier_id")
                total = Decimal(str(data.get("total", 0)))
                
                supplier = Supplier.objects.filter(id=supplier_id).first()
                if supplier:
                    po = PurchaseOrder.objects.create(
                        po_no=po_no,
                        supplier=supplier,
                        total=total,
                        status="Submitted"
                    )
                    
                    items = data.get("items", [])
                    for item in items:
                        prod = Product.objects.filter(sku=item.get("product_sku")).first()
                        if prod:
                            qty = int(item.get("qty", 1))
                            cost = Decimal(str(item.get("cost", 0)))
                            item_total = Decimal(str(item.get("total", 0)))
                            
                            PurchaseItem.objects.create(
                                purchase_order=po,
                                product=prod,
                                qty=qty,
                                cost=cost,
                                total=item_total
                            )
                    
                    # Add to supplier's outstanding balance
                    supplier.outstanding_balance += total
                    supplier.save()

                    AuditLog.objects.create(
                        user=request.user.username if request.user.is_authenticated else "system",
                        action="Create Purchase Order",
                        module="Purchase Orders",
                        details=f"Created PO {po_no} for {supplier.name} totaling PHP {total:.2f}."
                    )

            elif action == "receive_po":
                po_no = data.get("po_no")
                po = PurchaseOrder.objects.filter(po_no=po_no).first()
                if po and po.status != "Received":
                    po.status = "Received"
                    po.save()
                    
                    # Load items and add stock to warehouse
                    for item in po.items.all():
                        prod = item.product
                        prod.stock_quantity += item.qty
                        prod.save()
                        
                    AuditLog.objects.create(
                        user=request.user.username if request.user.is_authenticated else "system",
                        action="Receive Purchase Order",
                        module="Purchase Orders",
                        details=f"Received PO {po.po_no}. Added products to inventory."
                    )

            elif action == "run_payroll":
                # Resets incentives and posts expenses
                total_payroll = Decimal("0.00")
                employees = Employee.objects.filter(status="Active")
                payroll_date = date.today().isoformat()
                
                for emp in employees:
                    total_salary = emp.base_salary + emp.overtime + emp.incentives - emp.deductions
                    total_payroll += total_salary
                    
                    # Log as a payroll expense
                    Expense.objects.create(
                        category="Payroll / Salaries",
                        amount=total_salary,
                        description=f"Monthly payout for {emp.name} ({emp.role}). Base: {emp.base_salary}, Inc: {emp.incentives}.",
                        date=date.today()
                    )
                    
                    # Reset dynamic monthly incentives
                    emp.incentives = Decimal("0.00")
                    emp.overtime = Decimal("0.00")
                    emp.deductions = Decimal("0.00")
                    emp.save()
                
                AuditLog.objects.create(
                    user=request.user.username if request.user.is_authenticated else "system",
                    action="Release Salaries",
                    module="Payroll",
                    details=f"Processed payroll release for all employees. Total: PHP {total_payroll:.2f} recorded in expenses."
                )

            elif action == "create_expense":
                cat = data.get("category")
                amt = Decimal(str(data.get("amount", 0)))
                desc = data.get("description", "")
                exp_date = data.get("date", date.today().isoformat())
                
                Expense.objects.create(
                    category=cat,
                    amount=amt,
                    description=desc,
                    date=datetime.strptime(exp_date, "%Y-%m-%d").date()
                )
                
                AuditLog.objects.create(
                    user=request.user.username if request.user.is_authenticated else "system",
                    action="Create Expense",
                    module="Accounting",
                    details=f"Recorded expense under '{cat}' worth PHP {amt:.2f}."
                )

            elif action == "create_product":
                sku = data.get("sku")
                name = data.get("name")
                cost_price = Decimal(str(data.get("cost_price", 0)))
                wholesale_price = Decimal(str(data.get("wholesale_price", 0)))
                retail_price = Decimal(str(data.get("retail_price", 0)))
                min_stock = int(data.get("min_stock", 5))
                max_stock = int(data.get("max_stock", 100))
                barcode_str = data.get("barcode", "")
                
                brand_id = data.get("brand_id")
                cat_id = data.get("category_id")
                supplier_id = data.get("supplier_id")
                
                brand = Brand.objects.filter(id=brand_id).first() if brand_id else None
                cat = Category.objects.filter(id=cat_id).first() if cat_id else None
                supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id else None
                
                Product.objects.create(
                    sku=sku,
                    name=name,
                    brand=brand,
                    category=cat,
                    cost_price=cost_price,
                    wholesale_price=wholesale_price,
                    retail_price=retail_price,
                    stock_quantity=0,
                    min_stock=min_stock,
                    max_stock=max_stock,
                    barcode=barcode_str,
                    supplier=supplier
                )
                
                AuditLog.objects.create(
                    user=request.user.username if request.user.is_authenticated else "system",
                    action="Add Product",
                    module="Products",
                    details=f"Added new product {name} ({sku}) to catalog."
                )

            return JsonResponse({"success": True, "state": get_current_state()})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)

def generate_barcode(request, sku):
    prod = Product.objects.filter(sku=sku).first()
    barcode_data = prod.barcode if (prod and prod.barcode) else sku
    
    try:
        # Standard EAN13 or Code128 barcode
        CODE128 = barcode.get_barcode_class('code128')
        code128 = CODE128(barcode_data, writer=ImageWriter())
        
        buffer = BytesIO()
        code128.write(buffer)
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    except Exception as e:
        # Return fallback blank image or string error
        return HttpResponse(f"Error generating barcode: {str(e)}", status=500)

def generate_qrcode(request, sku):
    # Dynamic QR code that points to checkout catalog or item description
    qr_data = f"https://sarisari-erp.ph/product/{sku}"
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")

def export_excel(request):
    # Generates Excel sheets for Sales and Inventory reports
    report_type = request.GET.get('type', 'sales')
    wb = Workbook()
    ws = wb.active
    
    if report_type == 'inventory':
        ws.title = "Inventory Balance Report"
        ws.append(["SKU", "Product Name", "Category", "Brand", "Cost Price (PHP)", "Wholesale Price (PHP)", "Retail Price (PHP)", "Current Stock", "Min Stock", "Status"])
        for p in Product.objects.all():
            status = "Ok"
            if p.stock_quantity <= p.min_stock:
                status = "Critical Low Stock"
            elif p.stock_quantity == 0:
                status = "Out of Stock"
            ws.append([p.sku, p.name, p.category.name if p.category else "", p.brand.name if p.brand else "", float(p.cost_price), float(p.wholesale_price), float(p.retail_price), p.stock_quantity, p.min_stock, status])
    else:
        ws.title = "Sales Report"
        ws.append(["Invoice No", "Date", "Customer", "Route", "Subtotal (PHP)", "Tax (PHP)", "Total (PHP)", "Payment Method", "Status"])
        for s in Sale.objects.order_by('-date'):
            ws.append([s.invoice_no, s.date.strftime("%Y-%m-%d %H:%M"), s.customer.name if s.customer else "Walk-in", s.route or "Store POS", float(s.subtotal), float(s.tax), float(s.total), s.method, s.status])
            
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d%H%M')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb.save(response)
    return response

def export_pdf(request):
    # PDF generation for sales receipts or reports using ReportLab
    report_type = request.GET.get('type', 'sales')
    invoice_no = request.GET.get('invoice_no')
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=15
    )
    normal_style = styles['Normal']
    
    if invoice_no:
        # Exporting specific Invoice
        sale = Sale.objects.filter(invoice_no=invoice_no).first()
        if not sale:
            return HttpResponse("Invoice not found", status=404)
        
        story.append(Paragraph(f"SHERYL SARI-SARI STORE & ERP SYSTEM", title_style))
        story.append(Paragraph(f"Official Sales Invoice / Receipt", styles['Heading2']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Invoice No: <b>{sale.invoice_no}</b>", normal_style))
        story.append(Paragraph(f"Date: {sale.date.strftime('%Y-%m-%d %H:%M')}", normal_style))
        story.append(Paragraph(f"Customer: {sale.customer.name if sale.customer else 'Walk-in'}", normal_style))
        story.append(Paragraph(f"Sales Route: {sale.route or 'POS Direct Checkout'}", normal_style))
        story.append(Spacer(1, 15))
        
        # Item Table
        data = [["Product SKU", "Product Name", "Qty", "Price (PHP)", "Total (PHP)"]]
        for item in sale.items.all():
            data.append([item.product.sku, item.product.name, str(item.qty), f"{item.price:.2f}", f"{item.total:.2f}"])
            
        data.append(["", "", "", "Subtotal:", f"{sale.subtotal:.2f}"])
        data.append(["", "", "", "Tax (12%):", f"{sale.tax:.2f}"])
        data.append(["", "", "", "Grand Total:", f"{sale.total:.2f}"])
        
        table = Table(data, colWidths=[100, 220, 40, 90, 90])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2563EB')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 6),
            ('GRID', (0,0), (-1,-4), 0.5, colors.grey),
            ('FONTNAME', (3,-3), (-1,-1), 'Helvetica-Bold'),
            ('LINEABOVE', (3,-3), (-1,-3), 1, colors.black),
            ('FONTSIZE', (0,1), (-1,-1), 9),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"Payment Method: <b>{sale.method}</b> | Status: <b>{sale.status}</b>", normal_style))
        story.append(Spacer(1, 40))
        story.append(Paragraph("Thank you for your patronage! Reconciled & Powered by Django ERP", normal_style))
        
    else:
        # General Sales Summary
        story.append(Paragraph(f"Sales Summary Statement Report", title_style))
        story.append(Paragraph(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
        story.append(Spacer(1, 15))
        
        data = [["Invoice No", "Date", "Customer", "Route", "Total (PHP)", "Method", "Status"]]
        for s in Sale.objects.order_by('-date')[:30]:
            data.append([
                s.invoice_no,
                s.date.strftime("%Y-%m-%d"),
                s.customer.name[:18] if s.customer else "Walk-in",
                s.route[:15] if s.route else "POS",
                f"{s.total:.2f}",
                s.method,
                s.status
            ])
            
        table = Table(data, colWidths=[90, 80, 110, 100, 70, 50, 60])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ]))
        story.append(table)

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(content_type="application/pdf")
    filename = f"report_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    response.write(pdf)
    return response
