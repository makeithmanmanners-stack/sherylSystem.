from django.core.management.base import BaseCommand
from core.models import Employee, Supplier, Customer, AuditLog
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Updates database records replacing Sheryl with Sheyde and removing distributor branding.'

    def handle(self, *args, **options):
        # Update Employees
        emp_count = Employee.objects.filter(name__icontains='Sheryl').update(name='Sheyde Vasquez')
        
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
            if changed:
                sup.save()
                sup_count += 1

        self.stdout.write(self.style.SUCCESS(f'Branding update complete. Employees updated: {emp_count}, Users updated: {user_count}, Suppliers updated: {sup_count}.'))
