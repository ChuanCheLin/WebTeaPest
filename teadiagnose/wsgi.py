"""
WSGI config for teadiagnose project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/ssl/.local/lib/python3.8/site-packages')
from django.core.wsgi import get_wsgi_application
path = '/home/ssl/WebTeaPest'
if path not in sys.path:
    sys.path.append(path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'teadiagnose.settings')
application = get_wsgi_application()
