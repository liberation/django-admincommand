from django.core.management.base import BaseCommand


def fibonnaci(x):
    if x == 0:
        return 0
    if x == 1:
        return 1
    return fibonnaci(x-1) + fibonnaci(x-2)


class Command(BaseCommand):
    help = "Compute fibonnaci number"

    def handle(self, *args, **options):
        r = fibonnaci(int(args[0]))
        self.stdout.write('fibonnaci(%s) = %s' % (args[0],r))
