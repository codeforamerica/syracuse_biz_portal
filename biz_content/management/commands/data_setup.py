import factory
import os
from biz_content.tests import factories
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class AdminUserFactory(factory.DjangoModelFactory):
    """ AdminUserFactory
    Creates a new admin user for testing purposes
    in review apps on heroku. It can also be used locally.
    """
    class Meta:
        model = 'auth.User'

    email = 'admin@codeforamerica.org'
    username = 'admin'
    is_superuser = True
    is_staff = True
    is_active = True

    password = factory.PostGenerationMethodCall(
        'set_password', os.environ['TEST_ADMIN_PASSWORD'])


class Command(BaseCommand):
    help = 'Creates content and users from factories for initial deploy.'

    def handle(self, *args, **options):
        AdminUserFactory.create_batch(size=1)
