#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if os.path.isfile('gitachievements/settings/custom.py'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitachievements.settings.custom")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gitachievements.settings.common")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
