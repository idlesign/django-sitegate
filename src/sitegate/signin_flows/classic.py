from django.contrib.auth.forms import AuthenticationForm as ClassicSigninForm

from .base import SigninFlow


class ClassicSignin(SigninFlow):
    """Classic login flow borrowed from Django built-in AuthenticationForm."""

    form = ClassicSigninForm
