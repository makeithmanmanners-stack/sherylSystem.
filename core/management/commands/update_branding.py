from django.core.management.base import BaseCommand
from core.models import Employee, Supplier, Customer, AuditLog
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Updates database records replacing Sheryl with Sheyde and removing distributor branding.'

    def handle(self, *args, **options):
        # Update Employees
        emp_count = 0
        for emp in Employee.objects.all():
            if 'sheryl' in emp.name.lower():
                emp.name = emp.name.replace('Sheryl', 'Sheyde').replace('sheryl', 'sheyde')
                emp.save()
                emp_count += 1
        
        # Update Users
        user_count = 0
        for user in User.objects.all():
            changed = False
            if 'sheryl' in user.username.lower():
                user.username = user.username.lower().replace('sheryl', 'sheyde')
                changed = True
            if 'sheryl' in user.first_name.lower():
                user.first_name = user.first_name.replace('Sheryl', 'Sheyde').replace('sheryl', 'sheyde')
                changed = True
            if 'sheryl' in user.last_name.lower():
                user.last_name = user.last_name.replace('Sheryl', 'Sheyde').replace('sheryl', 'sheyde')
                changed = True
            if changed:
                user.save()
                user_count += 1

        # Update Customers
        cust_count = 0
        for cust in Customer.objects.all():
            if 'sheryl' in cust.name.lower():
                cust.name = cust.name.replace('Sheryl', 'Sheyde').replace('sheryl', 'sheyde')
                cust.save()
                cust_count += 1

        # Update Suppliers
        sup_count = 0
        for sup in Supplier.objects.all():
            changed = False
            if sup.email and 'distributors@' in sup.email:
                sup.email = sup.email.replace('distributors@', 'sales@')
                changed = True
            if 'distributor' in sup.name.lower() or 'distributor' in (sup.company_name or '').lower():
                sup.name = sup.name.replace('Distributor', 'Supplier').replace('distributor', 'supplier')
                if sup.company_name:
                    sup.company_name = sup.company_name.replace('Distributor', 'Supplier').replace('distributor', 'supplier')
                changed = True
            if 'sheryl' in sup.name.lower():
                sup.name = sup.name.replace('Sheryl', 'Sheyde').replace('sheryl', 'sheyde')
                changed = True
            if changed:
                sup.save()
                sup_count += 1

        self.stdout.write(self.style.SUCCESS(f'Branding update complete. Employees: {emp_count}, Users: {user_count}, Customers: {cust_count}, Suppliers: {sup_count}.'))
