from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django import forms

from . import models, constants


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        try:
            user = models.User.objects.get(email=self.cleaned_data.get("email"))
            if user != None:
                raise ValidationError("Email in use.")
            return self.cleaned_data.get("email")
        except models.User.DoesNotExist:
            return self.cleaned_data.get("email")


class CreateTransactionForm(forms.Form):
    destination = forms.IntegerField(min_value=1)
    
    quantity = forms.FloatField(min_value=0)

    def clean_destination(self):
        try:
            user = models.User.objects.get(id=self.cleaned_data.get("destination"))

            if user == None:
                raise ValidationError("There is no recipient.")
            elif not user.is_active:
                raise ValidationError("There is no recipient.")
            elif user.groups.all()[0].name != constants.GROUP_USER:
                raise ValidationError("The recipient is not a user.")

            return self.cleaned_data.get("destination")
        except models.User.DoesNotExist:
            raise ValidationError("There is no recipient.")
