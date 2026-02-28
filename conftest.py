"""Pytest configuration for Django project."""
import os

import django
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devops_project.settings")
django.setup()
