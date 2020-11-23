import logging
import time

from django.conf import settings
from django.db import ProgrammingError
from django.core.management import call_command
from django.core.management.base import BaseCommand


logger = logging.getLogger('kompassi')


def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()

    user, created = User.objects.get_or_create(username='mahti', defaults=dict(
        first_name='Markku',
        last_name='Mahtinen',
        is_staff=True,
        is_superuser=True,
    ))

    if created:
        user.set_password('mahti')
        user.save()

        logger.warn('Created superuser "mahti" with password "mahti"')


class Command(BaseCommand):
    args = ''
    help = 'Docker development environment entry point'

    def handle(self, *args, **options):
        from infokala.models import Workflow

        test = settings.DEBUG

        if not test:
            raise ValueError('Should run with DEBUG=true')

        try:
            Workflow.objects.first()
        except ProgrammingError:
            call_command('migrate')
            call_command('infokala_setup_basic_workflow', 'tracon2017')
            create_superuser()

        call_command('runserver', '0.0.0.0:8000')
