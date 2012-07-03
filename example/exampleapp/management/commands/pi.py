# http://en.literateprograms.org/Pi_with_Machin%27s_formula_%28Python%29
from django.core.management.base import BaseCommand


def arccot(x, unity):
    sum = xpower = unity // x
    n = 3
    sign = -1
    while 1:
        xpower = xpower // (x*x)
        term = xpower // n
        if not term:
            break
        sum += sign * term
        sign = -sign
        n += 2
    return sum


def pi(digits):
    unity = 10**(digits + 10)
    pi = 4 * (4*arccot(5, unity) - arccot(239, unity))
    return pi // 10**10


class Command(BaseCommand):
    help = "Compute pi number"

    def handle(self, *args, **options):
        r = str(pi(int(args[0])))
        r = r[0] + '.' + r[1:]
        self.stdout.write('pi(%s) = %s' % (args[0],r))
