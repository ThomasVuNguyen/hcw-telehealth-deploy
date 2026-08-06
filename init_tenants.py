import sys
import django

django.setup()

from tenants.models import Tenant, Domain
from django_tenants.utils import tenant_context
from mediaserver.models import Server

print("Initializing django-tenants...")
pub, _ = Tenant.objects.get_or_create(schema_name='public', defaults={'name': 'Public'})
Domain.objects.get_or_create(domain='public.local', defaults={'tenant': pub, 'is_primary': True})

demo, _ = Tenant.objects.get_or_create(schema_name='demo', defaults={'name': 'Demo Tenant'})
Domain.objects.get_or_create(domain='telehealth.beenex.org', defaults={'tenant': demo, 'is_primary': True})
Domain.objects.get_or_create(domain='localhost', defaults={'tenant': demo, 'is_primary': False})
Domain.objects.get_or_create(domain='127.0.0.1', defaults={'tenant': demo, 'is_primary': False})
Domain.objects.get_or_create(domain='patient.beenex.org', defaults={'tenant': demo, 'is_primary': False})
Domain.objects.get_or_create(domain='admin-telehealth.beenex.org', defaults={'tenant': demo, 'is_primary': False})

with tenant_context(demo):
    srv, created = Server.objects.get_or_create(
        url='https://livekit.beenex.org',
        defaults={
            'api_token': 'devkey',
            'api_secret': 'secret',
            'type': 'livekit',
            'is_active': True,
            'max_session_number': 10,
        }
    )
    if not created and (srv.api_token != 'devkey' or srv.api_secret != 'secret' or not srv.is_active or srv.url != 'https://livekit.beenex.org'):
        srv.url = 'https://livekit.beenex.org'
        srv.api_token = 'devkey'
        srv.api_secret = 'secret'
        srv.is_active = True
        srv.save()
        print("Updated LiveKit server record.")
    elif created:
        print("Created LiveKit server record.")

print("Tenant domain and LiveKit initialization complete.")
