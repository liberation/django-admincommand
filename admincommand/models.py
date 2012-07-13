from sneak.models import SneakModel

from django import forms
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import signals
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.utils import DatabaseError
from django.utils.importlib import import_module

from admincommand.utils import generate_instance_name, generate_human_name


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

    def get_help(self):
        if hasattr(self, 'help'):
            return self.help
        return self.command().help

    def command(self):
        """Getter of the management command import core"""
        import core
        command = core.get_command(self.command_name())
        return command

    @classmethod
    def command_name(cls):
        return generate_instance_name(cls.__name__)

    def name(self):
        return generate_human_name(cls.__name__)

    def url_name(self):
        return type(self).__name__.lower()

    @classmethod
    def permission_codename(cls):
        return 'can_run_command_%s' % cls.command_name()

    @classmethod
    def all(cls):
        import core
        for runnable_command in core.get_admin_commands().values():
            yield runnable_command

def sync_db(verbosity = 0, interactive = False, signal = None, **kwargs):
    for app_module_path in settings.INSTALLED_APPS:
        try:
            admin_commands_path = '%s.admincommands' % app_module_path
            module = import_module(admin_commands_path)
        except ImportError:
            pass
    for subclass in AdminCommand.__subclasses__():
        codename = subclass.permission_codename()
        ct = ContentType.objects.get(
            model='admincommand',
            app_label='admincommand',
        )
        perm = Permission(
            codename=codename,
            content_type=ct,
            name = 'Can run %s' % subclass.command_name(),
        )
        perm.save()
signals.post_syncdb.connect(sync_db)
