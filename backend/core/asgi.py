"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

# import os
# import django
# from channels.routing import get_default_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
# django.setup()
# application = get_default_application()

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_asgi_application()