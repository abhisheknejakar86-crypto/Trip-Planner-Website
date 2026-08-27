"""
ASGI config for tripplanner project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tripplanner.settings")

application = get_asgi_application()
