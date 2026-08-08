from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from core.models import Category, Brand, Supplier, Product, Customer, Employee, Sale, SaleItem, Trip, TripItem, PurchaseOrder, PurchaseItem, Expense, AuditLog, Subscription
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
        if val is None:
            data[field.name] = None
        elif isinstance(val, bool):
            data[field.name] = val
        elif isinstance(val, int):
            data[field.name] = val
        elif isinstance(val, (Decimal, float)):
            data[field.name] = float(val)
        elif isinstance(val, (datetime, date)):
            data[field.name] = val.isoformat()
        elif bool(val) and hasattr(val, 'url'):
            try:
                name_str = str(getattr(val, 'name', '') or '')
                if name_str.startswith('http://') or name_str.startswith('https://'):
                    data[field.name] = name_str
                else:
                    data[field.name] = val.url
            except Exception:
                data[field.name] = None
        elif hasattr(val, 'pk'):
            data[field.name] = val.pk if val else None
        else:
            data[field.name] = str(val)
    return data

def log_audit(request, action, module, details):
    user_obj = request.user if (request and hasattr(request, 'user') and request.user.is_authenticated) else None
    username_str = user_obj.username if user_obj else "system"
    AuditLog.objects.create(
        account_user=user_obj,
        user=username_str,
        action=action,
        module=module,
        details=details
    )

def store_context(request):
    store_name = "SHEYDE SARI-SARI STORE"
    user_plan = "Guest"
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
        cust = getattr(user, 'customer_profile', None)
        if cust and cust.name:
            store_name = cust.name
        else:
            sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()
            if sub and sub.name:
                store_name = sub.name
            else:
                emp = getattr(user, 'employee', None)
                if emp and emp.name:
                    store_name = emp.name

        is_admin = user.is_superuser or user.is_staff or (getattr(user, 'employee', None) and user.employee.role == 'Admin')
        if is_admin:
            user_plan = "Admin"
        else:
            sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()
            if sub:
                plan = sub.plan_name.lower()
                if 'vip' in plan or '799' in plan:
                    user_plan = 'VIP'
                elif 'standard' in plan or '549' in plan:
                    user_plan = 'Standard'
                else:
                    user_plan = 'Starter'
    return {
        'store_name': store_name,
        'user_plan': user_plan
    }

def get_current_state(request=None):
    u = User.objects.filter(username__iexact='Khertadmin').first()
    if not u:
        try:
            u = User.objects.create_superuser(username='Khertadmin', email='Khertadmin', password='Sheydekertdeo051804')
        except Exception as e:
            print("Auto create superadmin error:", e)
    else:
        u.is_staff = True
        u.is_superuser = True
        u.is_active = True
        u.save()

    if u:
        Employee.objects.get_or_create(user=u, defaults={'name': 'Khert Admin', 'role': 'Admin', 'status': 'Active'})
        # Ensure Khertadmin has NO customer profile linked to prevent customer portal redirects
        Customer.objects.filter(user=u).update(user=None)

    if Product.objects.count() == 0:
        from django.core.management import call_command
        try:
            call_command('seed_if_empty')
        except Exception as e:
            print("Auto-seed error: ", e)

    user_plan = "Admin"
    store_name = "SHEYDE SARI-SARI STORE"
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
        cust = getattr(user, 'customer_profile', None)
        if cust and cust.name:
            store_name = cust.name
        else:
            sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()
            if sub and sub.name:
                store_name = sub.name
            else:
                emp = getattr(user, 'employee', None)
                if emp and emp.name:
                    store_name = emp.name

        is_admin = user.is_superuser or user.is_staff or (getattr(user, 'employee', None) and user.employee.role == 'Admin') or (user.username and user.username.lower() == 'khertadmin')
        if not is_admin:
            sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()
            if sub:
                plan = sub.plan_name.lower()
                if 'vip' in plan or '799' in plan:
                    user_plan = 'VIP'
                elif 'standard' in plan or '549' in plan:
                    user_plan = 'Standard'
                else:
                    user_plan = 'Starter'
            else:
                user_plan = 'Starter'

    curr_user = request.user if (request and hasattr(request, 'user') and request.user.is_authenticated) else None
    is_super = curr_user and (curr_user.is_superuser or curr_user.username.lower() == 'khertadmin')

    if curr_user and not is_super:
        cat_qs = Category.objects.filter(Q(user=curr_user) | Q(user__isnull=True))
        brand_qs = Brand.objects.filter(Q(user=curr_user) | Q(user__isnull=True))
        supp_qs = Supplier.objects.filter(Q(user=curr_user) | Q(user__isnull=True))
        cust_qs = Customer.objects.filter(Q(user=curr_user) | Q(user__isnull=True))
        emp_qs = Employee.objects.filter(Q(user=curr_user) | Q(user__isnull=True))
        prod_qs = Product.objects.filter(user=curr_user)
        sale_qs = Sale.objects.filter(user=curr_user).order_by('-date')
        trip_qs = Trip.objects.filter(user=curr_user).order_by('-date')
        po_qs = PurchaseOrder.objects.filter(user=curr_user).order_by('-date')
        exp_qs = Expense.objects.filter(user=curr_user).order_by('-date')
        audit_qs = AuditLog.objects.filter(Q(account_user=curr_user) | Q(user=curr_user.username)).order_by('-timestamp')[:50]
    else:
        cat_qs = Category.objects.all()
        brand_qs = Brand.objects.all()
        supp_qs = Supplier.objects.all()
        cust_qs = Customer.objects.all()
        emp_qs = Employee.objects.all()
        prod_qs = Product.objects.all()
        sale_qs = Sale.objects.order_by('-date')
        trip_qs = Trip.objects.order_by('-date')
        po_qs = PurchaseOrder.objects.order_by('-date')
        exp_qs = Expense.objects.order_by('-date')
        audit_qs = AuditLog.objects.order_by('-timestamp')[:50]

    state = {
        "user_plan": user_plan,
        "store_name": store_name,
        "categories": [serialize_model(c) for c in cat_qs],
        "brands": [serialize_model(b) for b in brand_qs],
        "suppliers": [serialize_model(s) for s in supp_qs],
        "customers": [serialize_model(c) for c in cust_qs],
        "employees": [serialize_model(e) for e in emp_qs],
        "expenses": [serialize_model(e) for e in exp_qs],
        "subscriptions": [serialize_model(s) for s in Subscription.objects.order_by('-created_at')],
        "audit_logs": [serialize_model(a) for a in audit_qs],
    }
    
    # Products
    products = []
    for p in prod_qs:
        p_data = serialize_model(p)
        p_data["category_id"] = p.category.id if p.category else None
        p_data["category_name"] = p.category.name if p.category else ""
        p_data["brand_id"] = p.brand.id if p.brand else None
        p_data["brand_name"] = p.brand.name if p.brand else ""
        p_data["supplier_id"] = p.supplier.id if p.supplier else None
        p_data["supplier_name"] = p.supplier.name if p.supplier else ""
        products.append(p_data)
    state["products"] = products

    # Sales
    sales = []
    for s in sale_qs:
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
    for t in trip_qs:
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
    for po in po_qs:
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
    state["purchase_orders"] = pos

    return state

@login_required(login_url='login')
def index(request):
    user = request.user
    emp = getattr(user, 'employee', None)
    is_admin = user.is_superuser or user.is_staff or (emp and emp.role == 'Admin') or (user.username and user.username.lower() == 'khertadmin')
    sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()

    if not is_admin and not sub:
        return HttpResponse("Access Denied: Active approved subscription required to access Admin Panel.", status=403)
    return render(request, 'index.html')

@login_required(login_url='login')
def store(request):
    user = request.user
    emp = getattr(user, 'employee', None)
    is_admin = user.is_superuser or user.is_staff or (emp and emp.role == 'Admin') or (user.username and user.username.lower() == 'khertadmin')
    if not is_admin:
        sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()
        if not sub:
            return HttpResponse("Access Denied: Active approved subscription required to access Storefront.", status=403)
    return render(request, 'store.html')

def login_view(request):
    if request.user.is_authenticated:
        user = request.user
        emp = getattr(user, 'employee', None)
        is_admin = user.is_superuser or user.is_staff or (emp and emp.role == 'Admin') or (user.username and user.username.lower() == 'khertadmin')
        if is_admin:
            return redirect('admin_portal')
        sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()
        if sub:
            return redirect('admin_portal')
            
        cust = getattr(user, 'customer_profile', None)
        if cust:
            return redirect('customer_portal')
        return redirect('admin_portal')
    
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            emp = getattr(user, 'employee', None)
            is_admin = user.is_superuser or user.is_staff or (emp and emp.role == 'Admin') or (username and username.lower() == 'khertadmin')
            
            if not is_admin:
                sub = Subscription.objects.filter(user=user).first()
                if not sub:
                    sub = Subscription.objects.filter(username=username).first()
                
                if sub and sub.status == 'Pending':
                    error_message = "Notice: Ang inyong GCash subscription payment ay PENDING pa sa Admin approval. Makakatanggap ka ng email notification o abangan ang pag-aprub ng admin."
                    return render(request, 'login.html', {'error_message': error_message})
                elif sub and sub.status == 'Rejected':
                    error_message = "Notice: Ang inyong subscription request ay hinarang ng Admin. Mangyaring mag-submit muli ng subscription sa aming payment page."
                    return render(request, 'login.html', {'error_message': error_message})

            login(request, user)
            if is_admin:
                return redirect('admin_portal')
            sub = Subscription.objects.filter(Q(user=user) | Q(username=username), status='Approved').first()
            if sub:
                return redirect('admin_portal')
                
            cust = getattr(user, 'customer_profile', None)
            if cust:
                return redirect('customer_portal')
            return redirect('admin_portal')
        else:
            sub = Subscription.objects.filter(username=username, status='Pending').first()
            if sub:
                error_message = f"Notice: Ang username na '{username}' ({sub.plan_name}) ay PENDING pa sa Admin approval ng GCash payment! Mag-hintay bago mag-login."
            else:
                error_message = "Maling username o password."
            
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def customer_portal(request):
    user = request.user
    emp = getattr(user, 'employee', None)
    is_admin = user.is_superuser or user.is_staff or (emp and emp.role == 'Admin') or (user.username and user.username.lower() == 'khertadmin')
    if is_admin:
        return redirect('admin_portal')

    sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()
    if sub:
        return redirect('admin_portal')

    cust = getattr(user, 'customer_profile', None)
    if not cust:
        return HttpResponse("You are not registered as a customer in the system.", status=403)
        
    return render(request, 'customer_portal.html', {'customer': cust})

def subscribe_view(request):
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        plan_name = request.POST.get('plan_name', 'Starter Plan (₱359)')
        amount_val = request.POST.get('amount', '359')
        gcash_ref = request.POST.get('gcash_reference', '').strip()
        
        if not name or not email or not username or not password or not gcash_ref:
            error_message = "Paki-kumpleto ang lahat ng field kasama ang GCash Reference Number."
        elif User.objects.filter(username=username).exists():
            error_message = "Ang username na ito ay nakarehistro na sa system. Pumili ng iba."
        elif Subscription.objects.filter(username=username, status='Pending').exists():
            error_message = "May umiiral nang pending subscription para sa username na ito. Mag-antay ng approval."
        else:
            try:
                sub = Subscription.objects.create(
                    name=name,
                    email=email,
                    username=username,
                    password=password,
                    plan_name=plan_name,
                    amount=Decimal(str(amount_val)),
                    gcash_reference=gcash_ref,
                    status='Pending'
                )
                AuditLog.objects.create(
                    user=username,
                    action="Submit Subscription",
                    module="Subscriptions",
                    details=f"New subscription request submitted: {name} ({email}), Plan: {plan_name}, Amount: PHP {amount_val}, GCash Ref: {gcash_ref}."
                )
                success_message = f"Salamat! Ang inyong subscription request ({plan_name}) at GCash Ref: {gcash_ref} ay na-submit na. Kapag na-verify at inaprobahan na ng Admin, maaari ka nang mag-log in!"
            except Exception as e:
                error_message = "Nagkaroon ng error sa pag-submit: " + str(e)

    plans = [
        {"id": "starter", "name": "Starter Plan", "price": "359", "period": "/ buwan", "desc": "Access sa Storefront, Admin Panel, Quick Orders, Inventory Master & Settings.", "badge": "Pang-Budget"},
        {"id": "standard", "name": "Standard Plan", "price": "549", "period": "/ buwan", "desc": "Access sa Storefront, Dashboard, Quick Orders, Inventory Master & Settings.", "badge": "Pinakasikat"},
        {"id": "vip", "name": "VIP Business", "price": "799", "period": "/ buwan", "desc": "Full Access kasama ang AI Stock Forecasting & Priority Support.", "badge": "Pinaka-Sulit"}
    ]
    
    return render(request, 'subscription.html', {
        'error_message': error_message,
        'success_message': success_message,
        'plans': plans,
        'gcash_number': '09366939816'
    })

def api_check_subscription(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return JsonResponse({'found': False, 'error': 'Ilagay ang iyong Email o Username.'})
        
    sub = Subscription.objects.filter(Q(email__iexact=query) | Q(username__iexact=query)).order_by('-created_at').first()
    if sub:
        return JsonResponse({
            'found': True,
            'username': sub.username,
            'name': sub.name,
            'email': sub.email,
            'plan_name': sub.plan_name,
            'amount': float(sub.amount),
            'gcash_reference': sub.gcash_reference,
            'status': sub.status,
            'created_at': sub.created_at.strftime('%Y-%m-%d %H:%M'),
            'approved_at': sub.approved_at.strftime('%Y-%m-%d %H:%M') if sub.approved_at else None
        })
    return JsonResponse({'found': False, 'error': 'Walang nahanap na subscription request sa Email/Username na ito.'})

def signup_view(request):
    return redirect('subscribe')

@csrf_exempt
def api_state(request):
    if request.method == 'GET':
        response = JsonResponse(get_current_state(request))
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    elif request.method == 'POST':
        try:
            if request.content_type and 'multipart/form-data' in request.content_type:
                data = request.POST
            else:
                try:
                    data = json.loads(request.body)
                except Exception:
                    data = request.POST
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
                    user=request.user if request.user.is_authenticated else None,
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
                
                log_audit(
                    request,
                    action="Create Sale",
                    module="Sales",
                    details=f"Created Invoice {invoice_no} worth PHP {total:.2f}. Method: {method}. Status: {status}."
                )
                return JsonResponse({"success": True, "invoice_no": invoice_no, "state": get_current_state()})

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
                        
                    log_audit(
                        request,
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

                log_audit(
                    request,
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
                    log_audit(
                        request,
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
                    log_audit(
                        request,
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

                    log_audit(
                        request,
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
                    
                    log_audit(
                        request,
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

                    log_audit(
                        request,
                        action="Create Purchase Order",
                        module="Purchase Orders",
                        details=f"Created PO {po_no} for {supplier.name} totaling PHP {total:.2f}."
                    )

            elif action == "approve_subscription":
                sub_id = data.get("subscription_id")
                sub = Subscription.objects.filter(id=sub_id).first()
                if sub:
                    user = User.objects.filter(username=sub.username).first()
                    if not user:
                        user = User.objects.create_user(username=sub.username, password=sub.password, email=sub.email)
                    else:
                        user.is_active = True
                        user.set_password(sub.password)
                        user.save()
                    
                    Customer.objects.get_or_create(
                        user=user,
                        defaults={
                            'name': sub.name,
                            'email': sub.email,
                            'contact': '',
                            'address': 'Subscribed Customer'
                        }
                    )
                    
                    sub.status = "Approved"
                    sub.user = user
                    sub.approved_at = timezone.now()
                    sub.save()
                    
                    log_audit(
                        request,
                        action="Approve Subscription",
                        module="Subscriptions",
                        details=f"Approved GCash subscription for {sub.name} ({sub.username}). Plan: {sub.plan_name}, GCash Ref: {sub.gcash_reference}."
                    )
                    return JsonResponse({"success": True, "message": f"Subscription for {sub.name} approved! User can now log in.", "state": get_current_state(request)})

            elif action == "reject_subscription":
                sub_id = data.get("subscription_id")
                notes = data.get("notes", "Rejected by Admin.")
                sub = Subscription.objects.filter(id=sub_id).first()
                if sub:
                    sub.status = "Rejected"
                    sub.admin_notes = notes
                    sub.save()
                    
                    log_audit(
                        request,
                        action="Reject Subscription",
                        module="Subscriptions",
                        details=f"Rejected subscription for {sub.name} ({sub.username}). Reason: {notes}."
                    )
                    return JsonResponse({"success": True, "message": f"Subscription for {sub.name} rejected.", "state": get_current_state(request)})

            elif action == "update_system_settings":
                user = request.user
                if not user or not user.is_authenticated:
                    return JsonResponse({"success": False, "error": "User not authenticated."})

                emp = getattr(user, 'employee', None)
                is_admin = user.is_superuser or user.is_staff or (emp and emp.role == 'Admin')
                sub = Subscription.objects.filter(Q(user=user) | Q(username=user.username), status='Approved').first()

                if not is_admin and not sub:
                    return JsonResponse({"success": False, "error": "Access Denied: Only active subscribed accounts with Admin Panel access can edit settings."})

                store_name_val = data.get("store_name", "").strip()
                email_val = data.get("email", "").strip()
                new_password = data.get("password", "").strip()
                
                # Update specific account credentials
                if email_val:
                    user.email = email_val
                if new_password:
                    user.set_password(new_password)
                    if sub:
                        sub.password = new_password
                        sub.save()
                user.save()

                if new_password:
                    from django.contrib.auth import update_session_auth_hash
                    update_session_auth_hash(request, user)

                # Update store name for this specific account
                if store_name_val:
                    if sub:
                        sub.name = store_name_val
                        if email_val:
                            sub.email = email_val
                        sub.save()

                    if emp:
                        emp.name = store_name_val
                        emp.save()

                    cust = getattr(user, 'customer_profile', None)
                    if cust:
                        if is_admin:
                            cust.user = None
                            cust.save()
                        else:
                            cust.name = store_name_val
                            if email_val:
                                cust.email = email_val
                            cust.save()
                    elif not is_admin:
                        Customer.objects.create(user=user, name=store_name_val, email=email_val or user.email)

                log_audit(
                    request,
                    action="Update System Settings",
                    module="Settings",
                    details=f"Updated Account & Store Settings: Store Name: '{store_name_val}', Email: '{email_val}', Password {'updated' if new_password else 'unchanged'}."
                )
                return JsonResponse({"success": True, "message": "System Settings, Store Name & Account Password updated successfully!", "state": get_current_state(request)})

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
                        
                    log_audit(
                        request,
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
                
                log_audit(
                    request,
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
                
                log_audit(
                    request,
                    action="Create Expense",
                    module="Accounting",
                    details=f"Recorded expense under '{cat}' worth PHP {amt:.2f}."
                )

            elif action == "create_category":
                cat_name = str(data.get("name", "")).strip()
                desc = str(data.get("description", "")).strip()
                if not cat_name:
                    return JsonResponse({"success": False, "error": "Category name is required."})
                
                Category.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    name=cat_name,
                    description=desc
                )
                log_audit(
                    request,
                    action="Create Category",
                    module="Products",
                    details=f"Created product category '{cat_name}'."
                )
                return JsonResponse({"success": True, "message": f"Category '{cat_name}' created successfully!", "state": get_current_state(request)})

            elif action == "delete_category":
                cat_id = data.get("category_id")
                Category.objects.filter(id=cat_id).delete()
                log_audit(
                    request,
                    action="Delete Category",
                    module="Products",
                    details=f"Deleted product category ID {cat_id}."
                )
                return JsonResponse({"success": True, "message": "Category deleted successfully!", "state": get_current_state(request)})

            elif action == "create_product":
                sku = str(data.get("sku", "")).strip()
                name = str(data.get("name", "")).strip()
                
                if not sku or not name:
                    return JsonResponse({"success": False, "error": "SKU and Product Name are required."})
                    
                if Product.objects.filter(sku__iexact=sku).exists():
                    return JsonResponse({"success": False, "error": f"A product with SKU '{sku}' already exists in inventory catalog."})
                    
                cost_price = Decimal(str(data.get("cost_price", 0)))
                wholesale_price = Decimal(str(data.get("wholesale_price", 0)))
                retail_price = Decimal(str(data.get("retail_price", 0)))
                stock_qty = int(data.get("stock_quantity", 0))
                min_stock = int(data.get("min_stock", 5))
                max_stock = int(data.get("max_stock", 100))
                barcode_str = data.get("barcode", "")
                
                brand_id = data.get("brand_id")
                cat_id = data.get("category_id")
                supplier_id = data.get("supplier_id")
                
                brand = Brand.objects.filter(id=brand_id).first() if brand_id and str(brand_id) not in ('', 'null', 'None') else None
                cat = Category.objects.filter(id=cat_id).first() if cat_id and str(cat_id) not in ('', 'null', 'None') else None
                supplier = Supplier.objects.filter(id=supplier_id).first() if supplier_id and str(supplier_id) not in ('', 'null', 'None') else None
                
                image_file = request.FILES.get('image') or request.FILES.get('image_file')
                image_url_val = data.get("image_url", "").strip() if isinstance(data.get("image_url"), str) else ""

                new_product = Product.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    sku=sku,
                    name=name,
                    brand=brand,
                    category=cat,
                    cost_price=cost_price,
                    wholesale_price=wholesale_price,
                    retail_price=retail_price,
                    stock_quantity=stock_qty,
                    min_stock=min_stock,
                    max_stock=max_stock,
                    barcode=barcode_str,
                    supplier=supplier
                )

                if image_file:
                    new_product.image_url = image_file
                    new_product.save()
                elif image_url_val:
                    new_product.image_url = image_url_val
                    new_product.save()
                
                log_audit(
                    request,
                    action="Add Product",
                    module="Products",
                    details=f"Added new product {name} ({sku}) with initial stock of {stock_qty} cases to catalog."
                )

            elif action == "update_product":
                sku = str(data.get("sku", "")).strip()
                prod = Product.objects.filter(sku=sku).first()
                if not prod:
                    return JsonResponse({"success": False, "error": f"Product with SKU '{sku}' not found."})
                
                name = str(data.get("name", "")).strip()
                if name:
                    prod.name = name
                
                if "cost_price" in data:
                    prod.cost_price = Decimal(str(data.get("cost_price", 0)))
                if "wholesale_price" in data:
                    prod.wholesale_price = Decimal(str(data.get("wholesale_price", 0)))
                if "retail_price" in data:
                    prod.retail_price = Decimal(str(data.get("retail_price", 0)))
                if "stock_quantity" in data:
                    prod.stock_quantity = int(data.get("stock_quantity", 0))
                if "min_stock" in data:
                    prod.min_stock = int(data.get("min_stock", 5))
                if "max_stock" in data:
                    prod.max_stock = int(data.get("max_stock", 100))
                if "barcode" in data:
                    prod.barcode = str(data.get("barcode", ""))
                
                brand_id = data.get("brand_id")
                cat_id = data.get("category_id")
                supplier_id = data.get("supplier_id")
                
                if brand_id is not None:
                    prod.brand = Brand.objects.filter(id=brand_id).first() if str(brand_id) not in ('', 'null', 'None') else None
                if cat_id is not None:
                    prod.category = Category.objects.filter(id=cat_id).first() if str(cat_id) not in ('', 'null', 'None') else None
                if supplier_id is not None:
                    prod.supplier = Supplier.objects.filter(id=supplier_id).first() if str(supplier_id) not in ('', 'null', 'None') else None

                image_file = request.FILES.get('image') or request.FILES.get('image_file')
                image_url_val = data.get("image_url", "").strip() if isinstance(data.get("image_url"), str) else ""

                if image_file:
                    prod.image_url = image_file
                elif image_url_val:
                    prod.image_url = image_url_val

                prod.save()

                log_audit(
                    request,
                    action="Update Product",
                    module="Products",
                    details=f"Updated product details and image for {prod.name} ({sku})."
                )

            elif action == "delete_product":
                sku = str(data.get("sku", "")).strip()
                prod_id = data.get("product_id")
                prod = None
                if sku:
                    prod = Product.objects.filter(sku=sku).first()
                elif prod_id:
                    prod = Product.objects.filter(id=prod_id).first()
                
                if prod:
                    prod_name = prod.name
                    prod_sku = prod.sku
                    prod.delete()
                    log_audit(
                        request,
                        action="Delete Product",
                        module="Products",
                        details=f"Deleted product '{prod_name}' ({prod_sku}) from inventory catalog."
                    )
                    return JsonResponse({"success": True, "message": f"Product '{prod_name}' deleted successfully!", "state": get_current_state(request)})
                return JsonResponse({"success": False, "error": "Product not found."})

            elif action == "delete_sale":
                invoice_no = str(data.get("invoice_no", "")).strip()
                sale_id = data.get("sale_id")
                sale = None
                if invoice_no:
                    sale = Sale.objects.filter(invoice_no=invoice_no).first()
                elif sale_id:
                    sale = Sale.objects.filter(id=sale_id).first()
                
                if sale:
                    inv = sale.invoice_no
                    tot = sale.total
                    sale.delete()
                    log_audit(
                        request,
                        action="Delete Sale Record",
                        module="Sales Ledger",
                        details=f"Deleted order record {inv} worth PHP {tot:.2f} from sales ledger."
                    )
                    return JsonResponse({"success": True, "message": f"Sale order '{inv}' deleted successfully!", "state": get_current_state(request)})
                return JsonResponse({"success": False, "error": "Sale record not found."})

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
    # Generates Excel sheets for Sales, Inventory, and Purchase Orders reports
    report_type = request.GET.get('type', 'sales')
    wb = Workbook()
    ws = wb.active
    
    if report_type == 'inventory':
        ws.title = "Inventory Balance Report"
        ws.append(["SKU", "Product Name", "Category", "Brand", "Cost Price (PHP)", "Wholesale Price (PHP)", "Retail Price (PHP)", "Current Stock", "Min Stock", "Status"])
        for p in Product.objects.all():
            status = "Ok"
            if p.stock_quantity == 0:
                status = "Out of Stock"
            elif p.stock_quantity <= p.min_stock:
                status = "Critical Low Stock"
            ws.append([p.sku, p.name, p.category.name if p.category else "", p.brand.name if p.brand else "", float(p.cost_price), float(p.wholesale_price), float(p.retail_price), p.stock_quantity, p.min_stock, status])
    elif report_type in ['po', 'purchase_orders']:
        ws.title = "Purchase Orders Report"
        ws.append(["PO Number", "Date", "Supplier Name", "Grand Total (PHP)", "Status", "Items Summary"])
        for po in PurchaseOrder.objects.order_by('-date'):
            items_str = ", ".join([f"{item.product.sku} x{item.qty}" for item in po.items.all() if item.product])
            ws.append([po.po_no, po.date.strftime("%Y-%m-%d %H:%M") if po.date else "", po.supplier.name if po.supplier else "N/A", float(po.total), po.status, items_str])
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
    # PDF generation for sales receipts, PO documents, inventory, or summary reports using ReportLab
    report_type = request.GET.get('type', 'sales')
    invoice_no = request.GET.get('invoice_no')
    po_no = request.GET.get('po_no')
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=15
    )
    normal_style = styles['Normal']
    
    if po_no:
        # Exporting specific Purchase Order Document PDF
        po = PurchaseOrder.objects.filter(po_no=po_no).first()
        if not po:
            return HttpResponse("Purchase Order not found", status=404)
            
        story.append(Paragraph("SHEYDE SARI-SARI STORE & DISTRIBUTORS", title_style))
        story.append(Paragraph("Official Purchase Order (Restock PO)", styles['Heading2']))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"PO Number: <b>{po.po_no}</b>", normal_style))
        story.append(Paragraph(f"Order Date: {po.date.strftime('%Y-%m-%d %H:%M') if po.date else 'N/A'}", normal_style))
        story.append(Paragraph(f"Supplier Name: <b>{po.supplier.name if po.supplier else 'General Supplier'}</b>", normal_style))
        story.append(Paragraph(f"Contact Person: {po.supplier.contact_person if po.supplier and po.supplier.contact_person else 'N/A'} ({po.supplier.phone if po.supplier else ''})", normal_style))
        story.append(Spacer(1, 15))
        
        data = [["SKU", "Product Description", "Qty (Cases)", "Unit Cost (PHP)", "Line Total (PHP)"]]
        for item in po.items.all():
            data.append([
                item.product.sku if item.product else "N/A",
                item.product.name[:30] if item.product else "Item",
                str(item.qty),
                f"{item.cost:.2f}",
                f"{item.total:.2f}"
            ])
        data.append(["", "", "", "Grand Total:", f"{po.total:.2f}"])
        
        table = Table(data, colWidths=[100, 210, 70, 80, 80])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284C7')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('GRID', (0,0), (-1,-2), 0.5, colors.grey),
            ('FONTNAME', (3,-1), (-1,-1), 'Helvetica-Bold'),
            ('LINEABOVE', (3,-1), (-1,-1), 1, colors.black),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"PO Status: <b>{po.status}</b>", normal_style))
        story.append(Spacer(1, 40))
        story.append(Paragraph("Authorized Supplier Procurement Document — Sheyde Sari-Sari Store ERP", normal_style))

    elif invoice_no:
        # Exporting specific Invoice
        sale = Sale.objects.filter(invoice_no=invoice_no).first()
        if not sale:
            return HttpResponse("Invoice not found", status=404)
        
        story.append(Paragraph("SHEYDE SARI-SARI STORE & ERP SYSTEM", title_style))
        story.append(Paragraph("Official Sales Invoice / Receipt", styles['Heading2']))
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
        story.append(Paragraph("Thank you for your patronage! Reconciled & Powered by Sheyde ERP", normal_style))

    elif report_type in ['po', 'purchase_orders']:
        # Purchase Orders Summary Report
        story.append(Paragraph("SHEYDE SARI-SARI STORE - Supplier Purchase Orders Report", title_style))
        story.append(Paragraph(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
        story.append(Spacer(1, 15))
        
        data = [["PO Number", "Date", "Supplier", "Total (PHP)", "Status"]]
        for po in PurchaseOrder.objects.order_by('-date'):
            data.append([
                po.po_no,
                po.date.strftime("%Y-%m-%d %H:%M") if po.date else "N/A",
                po.supplier.name[:22] if po.supplier else "N/A",
                f"{po.total:.2f}",
                po.status
            ])
            
        table = Table(data, colWidths=[120, 110, 150, 90, 75])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        story.append(Paragraph("Official Sheyde Sari-Sari Store Supplier Purchase Orders Report", normal_style))

    elif report_type == 'inventory':
        # Inventory Stock Master Report
        story.append(Paragraph("SHEYDE SARI-SARI STORE - Inventory Stock Master Report", title_style))
        story.append(Paragraph(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
        story.append(Spacer(1, 15))
        
        data = [["SKU", "Product Name", "Category", "Cost (₱)", "Wholesale (₱)", "Retail (₱)", "Stock", "Status"]]
        for p in Product.objects.all():
            status = "In Stock"
            if p.stock_quantity == 0:
                status = "Out of Stock"
            elif p.stock_quantity <= p.min_stock:
                status = "Low Stock"
                
            data.append([
                p.sku,
                p.name[:22],
                p.category.name[:14] if p.category else "General",
                f"{float(p.cost_price):.2f}",
                f"{float(p.wholesale_price):.2f}",
                f"{float(p.retail_price):.2f}",
                str(p.stock_quantity),
                status
            ])
            
        table = Table(data, colWidths=[65, 130, 80, 55, 65, 60, 40, 65])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        story.append(Paragraph("Official Sheyde Sari-Sari Store Stock Level Audit Report", normal_style))

    else:
        # General Sales Summary
        story.append(Paragraph("SHEYDE SARI-SARI STORE - Sales Summary Statement Report", title_style))
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
    filename = f"{report_type}_report_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    response.write(pdf)
    return response

