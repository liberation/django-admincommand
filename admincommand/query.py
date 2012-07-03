from django.conf import settings

from sneak.query import ListQuerySet

from admincommand.models import AdminCommand


class CommandQuerySet(ListQuerySet):
    """Custom QuerySet to list runnable commands"""

    def filter(self, *args, **kwargs):
        return ListQuerySet(AdminCommand.all())
