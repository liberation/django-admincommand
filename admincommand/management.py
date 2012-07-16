from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models import signals
from django.utils.importlib import import_module

import admincommand


def sync_db_callback(verbosity=0, interactive=False, signal=None, **kwargs):
    """
    Callback for post_syncdb signal that installs the ContentType and
    Permission necessary to use the app. This needs to be done manually
    because the app doesn't expose any concrete models.
    """

    for app_module_path in settings.INSTALLED_APPS:
        try:
            admin_commands_path = '%s.admincommands' % app_module_path
            import_module(admin_commands_path)
        except ImportError:
            pass
    for subclass in admincommand.models.AdminCommand.__subclasses__():
        codename = subclass.permission_codename()
        ct, created = ContentType.objects.get_or_create(
            model='admincommand',
            app_label='admincommand',
        )
        perm, created = Permission.objects.get_or_create(
            codename=codename,
            content_type=ct,
            name='Can run %s' % subclass.command_name(),
        )
signals.post_syncdb.connect(sync_db_callback, sender=admincommand.models)
