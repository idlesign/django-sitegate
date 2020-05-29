from django import forms
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .classic import SimpleClassicWithEmailSignup, SimpleClassicWithEmailSignupForm
from ..models import InvitationCode
from ..utils import USER

if False:  # pragma: nocover
    from django.contrib.auth.models import User  # noqa


def get_username_max_len() -> int:
    """Returns username maximum length as supported by Django."""

    fields = [field for field in USER._meta.fields if field.name == 'username']
    try:
        length = fields[0].max_length

    except IndexError:
        length = 30

    return length


USERNAME_MAX_LEN = get_username_max_len()


class ModernSignupForm(SimpleClassicWithEmailSignupForm):
    """Modernized form with unique e-mail field, without username and second password fields."""

    def __init__(self, *args, **kwargs):
        super(ModernSignupForm, self).__init__(*args, **kwargs)

        if 'username' in self.fields:
            del self.fields['username']

    def clean_email(self):
        email = super(ModernSignupForm, self).clean_email()

        if USER._default_manager.filter(email__iexact=email):
            raise forms.ValidationError(_('A user with that e-mail already exists.'))

        if len(email) > USERNAME_MAX_LEN:
            raise forms.ValidationError(
                _('E-mail length should be no more than %(max_len)s characters long.'),
                params={'max_len': USERNAME_MAX_LEN})

        return email


class ModernSignup(SimpleClassicWithEmailSignup):
    """Modernized registration flow based on classic from Django built-in
    with unique e-mail field, without username and second password fields.

    """
    form = ModernSignupForm

    def sign_in(self, request: HttpRequest, form: ModelForm, signup_result: 'User') -> bool:
        form_data = form.cleaned_data
        return self.login_generic(request, form_data['email'], form_data['password1'])

    def add_user(self, request: HttpRequest, form: ModelForm) -> 'User':

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

        new_fields = {'code': forms.CharField(label=_('Invitation code'))}
        new_fields.update(self.fields)
        self.fields = new_fields

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
