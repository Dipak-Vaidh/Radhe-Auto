"""
Create or update the default staff admin user (hashed password via set_password).
Run after deploy or when staff login fails: python manage.py create_staff_user
"""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

STAFF_USERNAME = 'radhe_admin'
STAFF_PASSWORD = 'RadheAdmin2026'
STAFF_EMAIL = 'admin@radhelocal.test'


class Command(BaseCommand):
    help = (
        'Create or update staff user (username=%s) with a secure hashed password. '
        'Use when staff login fails or after switching databases.'
    ) % STAFF_USERNAME

    def handle(self, *args, **options):
        db = settings.DATABASES['default']
        engine = db.get('ENGINE', '')
        name = db.get('NAME', '')
        host = db.get('HOST', '') or 'localhost'
        self.stdout.write(
            f'Target database: ENGINE={engine} NAME={name!r} HOST={host!r}'
        )

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=STAFF_USERNAME,
            defaults={
                'email': STAFF_EMAIL,
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        user.set_password(STAFF_PASSWORD)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        if not user.email:
            user.email = STAFF_EMAIL
        user.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(
            self.style.SUCCESS(
                f'{action} staff user. Username: {STAFF_USERNAME}  '
                f'(password set via set_password; not stored as plain text.)'
            )
        )
        self.stdout.write(
            'Verify in shell: get_user_model().objects.get(username="radhe_admin").check_password(...)'
        )
