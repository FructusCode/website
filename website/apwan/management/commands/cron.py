import datetime
from django.core.management import BaseCommand, CommandError
import pytz
from website.apwan.models.token import Token

__author__ = 'Dean Gardiner'


class Command(BaseCommand):
    args = 'JOB'
    help = "Run the specified cron job"

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError("Invalid arguments")

        if args[0] in cron_commands:
            cron_commands[args[0]]()


def _cleanup_tokens():
    print "Cleaning up tokens..."
    print

    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    for token in Token.objects.filter(expire__lt=utc_now):
        print "Removing", token
        token.delete()

    print "Complete"


cron_commands = {
    'cleanup_tokens': _cleanup_tokens
}
