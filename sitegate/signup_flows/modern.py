from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from .classic import SimpleClassicWithEmailSignup, SimpleClassicWithEmailSignupForm


class ModernSignupForm(SimpleClassicWithEmailSignupForm):
    """Modernized form with unique e-mail field, without username and second password fields."""

    def __init__(self, *args, **kwargs):
        super(ModernSignupForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User._default_manager.filter(email__iexact=email):
            raise forms.ValidationError(_('A user with that e-mail already exists.'))
        return email


class ModernSignup(SimpleClassicWithEmailSignup):
    """Modernized registration flow based on classic from Django built-in
    with unique e-mail field, without username and second password fields.

    """

    form = ModernSignupForm

    def sign_in(self, request, form, signup_result):
        form_data = form.cleaned_data
        return self.login_generic(request, form_data['email'], form_data['password1'])

    def add_user(self, request, form):
        user = super(form.__class__, form).save(commit=False)
        user.username = form.cleaned_data['email']
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return user


