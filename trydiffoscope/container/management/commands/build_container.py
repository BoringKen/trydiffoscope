import optparse

from django.core.management.base import BaseCommand

from ...utils import build_container

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        optparse.make_option(
            '--force',
            dest='force',
            help="Always rebuild. [default: %default]",
            action='store_true',
            default=False,
        ),
    )

    def handle(self, *args, **options):
        build_container(options['force'])
