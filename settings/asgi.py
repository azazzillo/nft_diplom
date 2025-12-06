# Django
from django.core.asgi import get_asgi_application

# Python
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

application = get_asgi_application()
