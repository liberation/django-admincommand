Django-AdminCommand
===================


Django-AdminCommand is a Django application that makes it possible
to run Django management commands from the admin.

Dependencies
============

 - django-async
 - django-sneak

Settings
========


You need to activate the Django admin in the settings and ``urls.py`` 
depending on your needs the configuration may vary, refer
to the Django documentation related to the 
`admin application <https://docs.djangoproject.com/en/dev/ref/contrib/admin/>`_.

Don't forget to add the application where you defined management
commands in the list of installed applications. This might be already
done but it might not be the case if you use an application to gather
all the management commands that must be admin commands.


Make magic happens
==================


Create a Django Management Command::

    # ./music/management/commands/lyrics.py


    class Command(BaseCommand):
        help = "Compute lyrics based an bitorological fluctuations"

        def handle(self, *args, **options):
            # algorithm that generated lyrics based on a title and a dictionary


Then you will have to create a configuration class for the command::

     # ./music/admincommands.py

     from admincommands.models import AdminCommand


     class Lyrics(AdminCommand):

          class form(forms.Form):
              title = forms.CharField()

          def get_command_arguments(self, forms_data):
              return [forms_data['title']], {}

And all is well, the new admin command will be available under the 
«Admin Command» area of the administration of the default admin site.

If you use custom admin site, don't forget to register 
``admincommand.models.AdminCommand`` to the admin site object.

Asynchronous tasks
==================

If you want to execute commands asynchronously you have to 
specify it in the AdminCommand configuration class with the 
``asynchronous`` property set to ``True``::

     # ./music/admincommands.py

     from admincommands.models import AdminCommand


     class Fugue(AdminCommand):

          asynchronous = True

          class form(forms.Form):
              title = forms.CharField()

          def get_command_arguments(self, forms_data):
              return [forms_data['title']], {}


You also need to run periodically ``flush_queue`` from ``django-async`` application for that matter don't forget to install the application.
