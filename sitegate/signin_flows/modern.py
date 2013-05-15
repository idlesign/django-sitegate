from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as ClassicSignupForm

from .base import SigninFlow


class ModernSignin(SigninFlow):
    """"""

    form = ClassicSignupForm


