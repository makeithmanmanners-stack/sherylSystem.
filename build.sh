#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py update_branding
python manage.py seed_if_empty

python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_erp.settings'); django.setup(); from django.contrib.auth.models import User; from core.models import Employee; u, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'}); u.set_password('Sheydekertdeo051804'); u.is_superuser=True; u.is_staff=True; u.is_active=True; u.save(); Employee.objects.get_or_create(user=u, defaults={'name': 'Admin User', 'role': 'Admin', 'status': 'Active'}); k, _ = User.objects.get_or_create(username='Khertadmin', defaults={'email': 'khertadmin@example.com'}); k.set_password('Sheydekertdeo051804'); k.is_superuser=True; k.is_staff=True; k.is_active=True; k.save(); Employee.objects.get_or_create(user=k, defaults={'name': 'Khert Admin', 'role': 'Admin', 'status': 'Active'})"
