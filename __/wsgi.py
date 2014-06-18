"""
WSGI config for macdown project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os

# This needs to be set BEFORE Cling is imported.
# https://github.com/kennethreitz/dj-static/issues/28
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '__.settings.deploy')

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())
