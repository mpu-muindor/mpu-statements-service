# Thanks to [dkarchmer](https://github.com/dkarchmer/aws-eb-docker-django)

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.count() == 0:
            admin = User.objects.create_superuser(email='', username='admin', password='admin')
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            logger.error('Admin accounts can only be initialized if no User exist')
