#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py update_branding
python manage.py seed_if_empty

python -c "import os; import django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store_erp.settings'); django.setup(); from django.contrib.auth.models import User; u, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'}); u.set_password('Sheydekertdeo051804'); u.is_superuser=True; u.is_staff=True; u.save()"
