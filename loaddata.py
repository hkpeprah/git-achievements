#!/usr/bin/env python
import os


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitachievements.settings.custom")

    from django.conf import settings
    from django.core.management import call_command

    for fixture in getattr(settings, 'FIXTURE_PATHS', []):
        call_command('loaddata', fixture)
