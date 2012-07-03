from StringIO import StringIO

from django.conf import settings
from django.core import management
from django.core.management import get_commands
from django.core.management import load_command_class
from django.utils.importlib import import_module
from django.core.management.base import BaseCommand

from async import schedule

from admincommand.models import AdminCommand, CommandOutput


# Cache variable to store runnable commands configuration defined
# as runnable commands in settings.ADMIN_COMMANDS
_command_configs = {}


def get_admin_commands():
    if not _command_configs:
        for app_module_path in settings.INSTALLED_APPS:
            try:
                admin_commands_path = '%s.admincommands' % app_module_path
                module = import_module(admin_commands_path)
            except ImportError:
                pass
            else:
                configs = dir(module)
                for config_name in configs:
                    AdminCommandClass = getattr(module, config_name)
                    if (isinstance(AdminCommandClass, type)
                        and AdminCommandClass is not AdminCommand
                        and issubclass(AdminCommandClass, AdminCommand)):
                        command_config = AdminCommandClass()
                        _command_configs[command_config.command_name()] = command_config
    return _command_configs


def get_command(name):
    # this is a copy pasted from django.core.management.call_command
    app_name = get_commands()[name]
    if isinstance(app_name, BaseCommand):
        # If the command is already loaded, use it directly.
        klass = app_name
    else:
        klass = load_command_class(app_name, name)
    return klass


def call_command(command_name, user, args=None, kwargs=None):
    """Call command and store output"""
    kwargs = kwargs if kwargs else {}
    args = args if args else []
    output = StringIO()
    kwargs['stdout'] = output
    management.call_command(command_name, *args, **kwargs)
    CommandOutput(
        tasker=user,
        output=output.getvalue(),
        command_name=command_name,
    ).save()


def run_command(command_config, cleaned_data, user):
    if hasattr(command_config, 'get_command_arguments'):
        args, kwargs = command_config.get_command_arguments(cleaned_data)
    else:
        args, kwargs = list(), dict()
    if command_config.asynchronous:
        task = schedule(call_command, [command_config.command_name(), args, kwargs, user.pk])
        return task
    else:
        # Change stdout to a StringIO to be able to retrieve output and
        # display it to the user
        output = StringIO()
        kwargs['stdout'] = output
        management.call_command(command_config.command_name(), *args, **kwargs)
        return output.getvalue()
