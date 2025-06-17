# ranger/celery.py

import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ranger.settings")

# Create the Celery app
app = Celery("ranger")

# Load settings from Django's settings.py using the 'CELERY_' namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered apps
app.autodiscover_tasks()
