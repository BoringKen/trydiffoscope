"""
WSGI config for trydiffoscope project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trydiffoscope.settings')

application = get_wsgi_application()
