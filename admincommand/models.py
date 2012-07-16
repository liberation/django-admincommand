from django import forms

from sneak.models import SneakModel

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
        return generate_human_name(type(self).__name__)

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
