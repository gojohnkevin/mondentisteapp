from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

from accounts.models import (
    DeviceToken,
    Appointment,
    DentistDetail
)
from drelbaz.libs.utils import get_or_none


class LoginForm(forms.Form):
    email    = forms.CharField(label='Email', required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    user = None

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            try:
                validate_email(email)
                user = get_or_none(User, email=email.lower())
            except ValidationError:
                user = get_or_none(User, username=email)

            if not user:
                raise forms.ValidationError(_('The email you entered does not exist'))

            user = auth.authenticate(username=user.username, password=password)

            if not user:
                raise forms.ValidationError(_('Please enter a correct email and password. '\
                                              'Note that both fields are case-sensitive.'))
            elif not user.is_active:
                raise forms.ValidationError(_('This account is inactive.'))

            else:
                self.user = user
        else:
            raise forms.ValidationError(_('Email and Password fields are required'))

        return self.cleaned_data


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(input_formats=['%Y-%m-%d',])
    time = forms.TimeField(input_formats=['%H:%M',])
    class Meta:
        model = Appointment

class DentistDetailForm(forms.ModelForm):
    class Meta:
        model = DentistDetail

class DeviceTokenForm(forms.ModelForm):
    class Meta:
        model = DeviceToken
