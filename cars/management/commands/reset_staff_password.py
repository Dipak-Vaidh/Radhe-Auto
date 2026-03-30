from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Alias for create_staff_user (same behavior).'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING('Use: python manage.py create_staff_user  (this command is an alias.)')
        )
        call_command('create_staff_user')
