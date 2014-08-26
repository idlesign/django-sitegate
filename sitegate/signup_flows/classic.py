from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .base import SignupFlow
from ..utils import USER
from ..models import BlacklistedDomain, EmailConfirmation
from ..settings import SIGNUP_VERIFY_EMAIL_BODY, SIGNUP_VERIFY_EMAIL_TITLE, SIGNUP_VERIFY_EMAIL_NOTICE, SIGNUP_VERIFY_EMAIL_VIEW_NAME


class ClassicSignupForm(UserCreationForm):
    """Classic form tuned to support custom user model."""

    class Meta:
        model = USER
        fields = ('username',)

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

    email = forms.EmailField(label=_('Email'))

    class Meta:
        model = USER
        fields = ('username', 'email', 'password1', 'password2')

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

            try:
                from sitemessage.schortcuts import schedule_email
                self.schedule_email = schedule_email
            except ImportError as e:
                def schedule_email(text, to, subject):
                    send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [to.email])

                self.schedule_email = schedule_email

    def send_email(self, request, user):
        if getattr(self, 'schedule_email', False):
            code = EmailConfirmation.add(user)
            url = request.build_absolute_uri(reverse(SIGNUP_VERIFY_EMAIL_VIEW_NAME, args=(code.code,)))
            email_text = u'%s' % SIGNUP_VERIFY_EMAIL_BODY  # %s for PrefProxy objects.
            self.schedule_email(email_text % {'url': url}, user, u'%s' % SIGNUP_VERIFY_EMAIL_TITLE)
            messages.success(request, SIGNUP_VERIFY_EMAIL_NOTICE, 'info')

    def add_user(self, request, form):
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

