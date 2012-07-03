from admincommand.models import AdminCommand

from django import forms


class Fibonnaci(AdminCommand):

    class form(forms.Form):
        x = forms.IntegerField()

    def get_command_arguments(self, forms_data):
        return [forms_data['x']], {}


class Pi(AdminCommand):

    asynchronous = True

    class form(forms.Form):
        digits = forms.IntegerField()

    def get_command_arguments(self, forms_data):
        return [forms_data['digits']], {}
