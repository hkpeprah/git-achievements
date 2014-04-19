from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Loads sample data into the datbase'

    def handle(self, *args, **options):
        """
        Reads from the fixture directories to load sample data into the database.
        Will overwrite any existing data for the specified fixtures if they already
        exist in the database.

        @return: None
        """
        for fixture in getattr(settings, 'FIXTURE_PATHS', []):
            call_command('loaddata', fixture)
