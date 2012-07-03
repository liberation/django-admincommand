from sneak.models import SneakModel

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

from admincommand.utils import generate_instance_name


ct, created = ContentType.objects.get_or_create(app_label='admincommand', model='admincommand')


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

    def __init__(self, *args, **kwargs):
        super(AdminCommand, self).__init__(*args, **kwargs)
        codename = self.permission_codename()
        self.perm, created = Permission.objects.get_or_create(
            codename=codename,
            content_type=ct,
        )
        if created:
            perm.name = 'Can Run %s' % self.command_name()
            perm.save()

    def command(self):
        """Getter of the management command import core"""
        import core
        command = core.get_command(self.command_name())
        return command

    def command_name(self):
        return generate_instance_name(type(self).__name__)

    def permission_codename(self):
        return 'can_run_command_%s' % self.command_name()

    @classmethod
    def all(cls):
        import core
        all = []
        for runnable_command in core.get_admin_commands().values():
            all.append(runnable_command)
        return all


class CommandOutput(models.Model):
    tasker = models.ForeignKey(User)
    command_name = models.CharField(max_length=255)
    output = models.TextField()

    def __unicode__(self):
        return self.command_name
