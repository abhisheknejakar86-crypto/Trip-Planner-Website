"""
WSGI config for tripplanner project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripplanner.settings")

application = get_wsgi_application()
