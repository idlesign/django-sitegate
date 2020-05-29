from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.forms import ModelForm
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .base import SignupFlow
from ..models import BlacklistedDomain, EmailConfirmation
from ..settings import SIGNUP_VERIFY_EMAIL_BODY, SIGNUP_VERIFY_EMAIL_TITLE, SIGNUP_VERIFY_EMAIL_NOTICE, \
    SIGNUP_VERIFY_EMAIL_VIEW_NAME, USE_SITEMESSAGE
from ..utils import USER

if False:  # pragma: nocover
    from django.contrib.auth.models import User  # noqa


USERNAME_FIELD = getattr(USER, 'USERNAME_FIELD', 'username')


class ClassicSignupForm(UserCreationForm):

    """Classic form tuned to support custom user model."""

    error_messages = dict(UserCreationForm.error_messages, **{
        'duplicate_username': _('A user with that username already exists.'),
        'password_mismatch': _('The two password fields didn\'t match.'),
    })

    class Meta:
        model = USER
        fields = (USERNAME_FIELD,)

    def __init__(self, *args, **kwargs):
        super(ClassicSignupForm, self).__init__(*args, **kwargs)
        if USERNAME_FIELD != 'username' and 'username' in self.fields:
            del self.fields['username']

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            USER._default_manager.get(username=username)

        except USER.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])


class ClassicSignup(SignupFlow):
    """Classic registration flow borrowed from Django built-in UserCreationForm."""

    form = ClassicSignupForm

    def add_user(self, request: HttpRequest, form: ModelForm) -> 'User':
        return form.save()

    def sign_in(self, request: HttpRequest, form: ModelForm, signup_result: 'User') -> bool:
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

    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = USER

        if USERNAME_FIELD != 'email':
            fields = (USERNAME_FIELD, 'email', 'password1', 'password2')

        else:
            fields = (USERNAME_FIELD, 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(ClassicWithEmailSignupForm, self).__init__(*args, **kwargs)

    def clean_email(self):

        email = self.cleaned_data['email']

        if self.flow.get_arg_or_attr('validate_email_domain'):

            if BlacklistedDomain.is_blacklisted(email):
                raise forms.ValidationError(_('Sign Up with this email domain is not allowed.'))

        return email


class ClassicWithEmailSignup(ClassicSignup):
    """Classic registration flow borrowed from Django built-in
    with additional e-mail field.

    """
    form = ClassicWithEmailSignupForm
    validate_email_domain = True
    verify_email = False

    def __init__(self, **kwargs):
        super(ClassicWithEmailSignup, self).__init__(**kwargs)

        verify_email = self.get_arg_or_attr('verify_email')

        if verify_email:

            self.flow_args['activate_user'] = False
            self.flow_args['auto_signin'] = False

            if USE_SITEMESSAGE:
                from sitemessage.toolbox import get_message_type_for_app, schedule_messages, recipients

                def schedule_email(text, to, subject):
                    message_cls = get_message_type_for_app('sitegate', 'email_plain')
                    schedule_messages(message_cls(subject, text), recipients('smtp', to))

            else:

                def schedule_email(text, to, subject):
                    send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [to.email])

            self.schedule_email = schedule_email

    def send_email(self, request: HttpRequest, user: 'User'):

        if getattr(self, 'schedule_email', False):
            code = EmailConfirmation.add(user)
            url = request.build_absolute_uri(reverse(SIGNUP_VERIFY_EMAIL_VIEW_NAME, args=(code.code,)))

            email_text = f'{SIGNUP_VERIFY_EMAIL_BODY}'
            self.schedule_email(email_text % {'url': url}, user, f'{SIGNUP_VERIFY_EMAIL_TITLE}')

            messages.success(request, SIGNUP_VERIFY_EMAIL_NOTICE, 'info')

    def add_user(self, request: HttpRequest, form: ModelForm) -> 'User':

        user = super(form.__class__, form).save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.email = form.cleaned_data['email']
        user.save()

        self.send_email(request, user)

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

