import sys
import django

django.setup()

from tenants.models import Tenant, Domain

print("Initializing django-tenants...")
pub, _ = Tenant.objects.get_or_create(schema_name='public', defaults={'name': 'Public'})
Domain.objects.get_or_create(domain='public.local', defaults={'tenant': pub, 'is_primary': True})

demo, _ = Tenant.objects.get_or_create(schema_name='demo', defaults={'name': 'Demo Tenant'})
Domain.objects.get_or_create(domain='telehealth.beenex.org', defaults={'tenant': demo, 'is_primary': True})
Domain.objects.get_or_create(domain='localhost', defaults={'tenant': demo, 'is_primary': False})
Domain.objects.get_or_create(domain='127.0.0.1', defaults={'tenant': demo, 'is_primary': False})
print("Tenant domain initialization complete.")
