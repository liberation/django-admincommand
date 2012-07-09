from sneak.models import SneakModel

from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.utils import DatabaseError

from admincommand.utils import generate_instance_name, generate_human_name

try:
    ct, created = ContentType.objects.get_or_create(app_label='admincommand', model='admincommand')
except DatabaseError:
    # if the database is not synced it will fail to create the content type
    pass


class AdminCommand(SneakModel):
    """Subclass this class to create an admin command
    class name should match the name of the command to be executed
    using the reverse algorithm used to construct instance names following
    the PEP8. For instance for a management command named
    ``fixing_management_policy`` the admin command class should be named
    ``FixingManagementPolicy``.
    """

    # :attribute asynchronous: True if the command should be executed
    # asynchronously
    asynchronous = False

    objects = None

    class form(forms.Form):
        pass

    def __init__(self, *args, **kwargs):
        super(AdminCommand, self).__init__(*args, **kwargs)
        codename = self.permission_codename()
        self.perm, created = Permission.objects.get_or_create(
            codename=codename,
            content_type=ct,
        )
        if created:
            import pdb; pdb.set_trace()
            self.perm.name = 'Can run %s' % self.command_name()
            self.perm.save()

    def get_help(self):
        if hasattr(self, 'help'):
            return self.help
        return self.command().help

    def command(self):
        """Getter of the management command import core"""
        import core
        command = core.get_command(self.command_name())
        return command

    def command_name(self):
        return generate_instance_name(type(self).__name__)

    def name(self):
        return generate_human_name(type(self).__name__)

    def url_name(self):
        return type(self).__name__.lower()

    def permission_codename(self):
        return 'can_run_command_%s' % self.command_name()

    @classmethod
    def all(cls):
        import core
        for runnable_command in core.get_admin_commands().values():
            yield runnable_command
