import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        """Handle the command"""
        self.stdout.write('Waiting for database...')
        db_conn = False
        while not db_conn:
            try:
                db_conn = connections["default"].ensure_connection()
                db_conn = True
            except OperationalError:
                self.stdout.write('Database is unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database is available!'))
