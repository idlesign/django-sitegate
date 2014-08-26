from django import forms
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from .classic import SimpleClassicWithEmailSignup, SimpleClassicWithEmailSignupForm
from ..models import InvitationCode
from ..utils import USER
from ..models import EmailConfirmation
from ..settings import SIGNUP_VERIFY_EMAIL_BODY, SIGNUP_VERIFY_EMAIL_TITLE, SIGNUP_VERIFY_EMAIL_NOTICE, SIGNUP_VERIFY_EMAIL_VIEW_NAME


class ModernSignupForm(SimpleClassicWithEmailSignupForm):
    """Modernized form with unique e-mail field, without username and second password fields."""

    def __init__(self, *args, **kwargs):
        super(ModernSignupForm, self).__init__(*args, **kwargs)
        del self.fields['username']

    def clean_email(self):
        email = super(ModernSignupForm, self).clean_email()
        if USER._default_manager.filter(email__iexact=email):
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
        if not hasattr(user, 'USERNAME_FIELD') or user.USERNAME_FIELD == 'username':
            user.username = form.cleaned_data['email']
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password1'])
        user.save()
        self.send_email(request, user)
        return user


class InvitationSignupForm(ModernSignupForm):
    """Modernized form with invitation code field."""

    def __init__(self, *args, **kwargs):
        super(InvitationSignupForm, self).__init__(*args, **kwargs)
        self.fields.insert(0, 'code', forms.CharField(label=_('Invitation code')))

    def clean_code(self):
        code = self.cleaned_data['code']
        if not InvitationCode.is_valid(code):
            raise forms.ValidationError(_('This invitation code is invalid.'))
        return code


class InvitationSignup(ModernSignup):
    """Modernized registration flow with additional invitation code field."""

    form = InvitationSignupForm

    def add_user(self, request, form):
        user = super(InvitationSignup, self).add_user(request, form)
        InvitationCode.accept(form.cleaned_data['code'], user)
        return user

