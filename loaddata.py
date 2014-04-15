#!/usr/bin/env python
import os


if __name__ == "__main__":
    if os.path.isfile('gitachievements/settings/custom.py'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitachievements.settings.custom")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitachievements.settings.common")

    from django.conf import settings
    from django.core.management import call_command

    for fixture in getattr(settings, 'FIXTURE_PATHS', []):
        call_command('loaddata', fixture)
