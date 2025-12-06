# Django
from django.core.wsgi import get_wsgi_application

# Python
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

application = get_wsgi_application()
