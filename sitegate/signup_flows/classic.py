from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as ClassicSignupForm

from .base import SignupFlow


class ClassicSignup(SignupFlow):
    """Classic registration flow borrowed from Django built-in UserCreationForm."""

    form = ClassicSignupForm

    def add_user(self, request, form):
        return form.save()

    def sign_in(self, request, form, signup_result):
        form_data = form.cleaned_data
        return self.login_generic(request, form_data['username'], form_data['password1'])


class SimpleClassicSignupForm(ClassicSignupForm):
    """Classic form without the second password field."""

    def __init__(self, *args, **kwargs):
        super(SimpleClassicSignupForm, self).__init__(*args, **kwargs)
        del self.fields['password2']


class SimpleClassicSignup(ClassicSignup):
    """Classic registration flow borrowed from Django built-in
    without second password field.

    """

    form = SimpleClassicSignupForm


class ClassicWithEmailSignupForm(ClassicSignupForm):
    """Classic form with email field."""

    def __init__(self, *args, **kwargs):
        super(ClassicWithEmailSignupForm, self).__init__(*args, **kwargs)
        # Put e-mail field right after the username.
        self.fields.insert(1, 'email', forms.EmailField(label=_('E-mail')))


class ClassicWithEmailSignup(ClassicSignup):
    """Classic registration flow borrowed from Django built-in
    with additional e-mail field.

    """

    form = ClassicWithEmailSignupForm

    def add_user(self, request, form):
        user = super(form.__class__, form).save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.email = form.cleaned_data['email']
        user.save()
        return user


class SimpleClassicWithEmailSignupForm(ClassicWithEmailSignupForm):
    """Classic form with email field but without the second password field."""

    def __init__(self, *args, **kwargs):
        super(SimpleClassicWithEmailSignupForm, self).__init__(*args, **kwargs)
        del self.fields['password2']


class SimpleClassicWithEmailSignup(ClassicWithEmailSignup):
    """Classic registration flow borrowed from Django built-in
    with e-mail field, but without second password field.

    """

    form = SimpleClassicWithEmailSignupForm

