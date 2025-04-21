from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField


class EnregistrementForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', 'password1', 'password2']
