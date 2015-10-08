from uuid import uuid4

import django
from django.conf import settings
from django.contrib import messages
from django.core import signing
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from etc.models import InheritedModel

from .settings import (
    SIGNUP_EMAIL_CHANGE_TWO_STEPS, SIGNUP_GENERIC_CONFIRMATION_VIEW_NAME,
    SIGNUP_EMAIL_CHANGE_PROCESSING,

    SIGNUP_VERIFY_EMAIL_CHANGE_START_TITLE, SIGNUP_VERIFY_EMAIL_CHANGE_START_BODY,
    SIGNUP_VERIFY_EMAIL_CHANGE_START_NOTICE,

    SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_TITLE, SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_BODY,
    SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_NOTICE,

    SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_TITLE, SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_BODY,
    SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_NOTICE,
)


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class BlacklistedDomain(models.Model):

    domain = models.CharField(_('Domain name'), max_length=253, unique=True)
    enabled = models.BooleanField(
        _('Enabled'),
        help_text=_('If enabled visitors won\'t be able to sign up with this domain name in e-mail.'),
        db_index=True, default=True)

    class Meta(object):
        verbose_name = _('Blacklisted domain')
        verbose_name_plural = _('Blacklisted domains')

    @classmethod
    def is_blacklisted(cls, email):
        domain = email.split('@', 1)[1].lower()

        # 'some.denied.co.uk' -> ['some.denied.co.uk', 'denied.co.uk', 'co.uk']
        sub_domains = [domain]
        for i in range(domain.count('.') - 1):
            sub_domains.append(sub_domains[i].split('.', 1)[-1])

        return cls.objects.filter(enabled=True, domain__in=sub_domains).exists()

    def __str__(self):
        return self.domain


@python_2_unicode_compatible
class ModelWithCode(models.Model):

    code = models.CharField('dummy', max_length=128, unique=True, editable=False)
    time_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    time_accepted = models.DateTimeField(_('Date accepted'), null=True, editable=False)
    expired = models.BooleanField(_('Expired'), help_text='dummy', db_index=True, default=False)

    class Meta(object):
        abstract = True

    def __str__(self):
        return self.code

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.code == '':
            while True:
                self.code = self.generate_code()
                try:
                    super(ModelWithCode, self).save(force_insert, force_update, **kwargs)
                except IntegrityError:
                    pass
                else:
                    break
        else:
            super(ModelWithCode, self).save(force_insert, force_update, **kwargs)

    @classmethod
    def is_valid(cls, code):
        try:
            return cls.objects.get(code=code, expired=False)
        except (cls.MultipleObjectsReturned, cls.DoesNotExist):
            return False

    @staticmethod
    def generate_code():
        return str(uuid4()).replace('-', '')


class InvitationCode(InheritedModel, ModelWithCode):

    creator = models.ForeignKey(USER_MODEL, related_name='creators', verbose_name=_('Creator'))
    acceptor = models.ForeignKey(USER_MODEL, related_name='acceptors', verbose_name=_('Acceptor'), null=True, blank=True, editable=False)

    class Meta(object):
        verbose_name = _('Invitation code')
        verbose_name_plural = _('Invitation codes')

    class Fields(object):
        code = _('Invitation code')
        expired = {'help_text': _('Visitors won\'t be able to sign up with an expired code.')}

    @classmethod
    def add(cls, creator):
        new_code = cls(creator=creator)
        new_code.save(force_insert=True)
        return new_code

    @classmethod
    def accept(cls, code, acceptor):
        return cls.objects.filter(code=code).update(acceptor=acceptor, expired=True, time_accepted=timezone.now())


class EmailConfirmation(InheritedModel, ModelWithCode):

    user = models.ForeignKey(USER_MODEL, verbose_name=_('User'))

    class Meta(object):
        verbose_name = _('Activation code')
        verbose_name_plural = _('Activation codes')

    class Fields(object):
        code = _('Activation code')
        expired = {'help_text': _('Expired codes couldn\'t be used for repeated account activations.')}

    @classmethod
    def add(cls, user):
        new_code = cls(user=user)
        new_code.save(force_insert=True)
        return new_code

    def encrypt_data(self, data):
        return signing.dumps(data, salt=self.code)

    def decrypt_data(self, encrypted_data):
        return signing.loads(encrypted_data, salt=self.code)

    def activate(self):
        self.expired = True
        self.time_accepted = timezone.now()
        self.save()

        user = self.user
        user.is_active = True
        user.save()

    def confirmation_url_for_data(self, confirmation_domain, data):
        encrypted_data = self.encrypt_data(data)
        url = reverse(
            SIGNUP_GENERIC_CONFIRMATION_VIEW_NAME,
            args=(confirmation_domain, self.code, encrypted_data)
        )
        return url

    @classmethod
    def start_email_change(cls, user, new_email, strict=True, send_email=True, request=None, next_step=None):
        """Start email change process, return url to SIGNUP_GENERIC_CPMFORMATION_VIEW_NAME view.

        1. generate new EmailConfirmation
        2. generate url to generic_confirmation view which will fire signal
           ``sig_generic_confirmation_received`` with arguments suitalbe to
           passed to ``EmailConfirmation.email_change_confirm_source_email``

        Processing of signal that is fired by visiting url with
        ``EmailConfirmation.email_change_confirm_source_email``
        can be enabled or disabled by boolean setting "SIGNUP_EMAIL_CHANGE_PROCESSING"
        (False by default). Or you can write your own signal receiver.

        """
        from .utils import send_email as send_email_func
        if hasattr(user, 'is_active') and (not user.is_active):
            raise ValidationError(_("Can't start email change process for inactive user"))
        if user.email.lower() == new_email.lower():
            raise ValidationError(_("To start email change process new email should differ from current email"))
        if send_email and not request:
            raise ValueError("``request`` argument is required when ``send_email`` is True")
        if next_step not in ('continue_email_change', 'finish_email_change', None):
            raise ValueError("Next step should be 'continue_email_change' or 'finish_email_change'")
        code = cls.add(user)
        data = {
            'new_email': new_email,
            'old_email': user.email,
            'strict': strict,
        }
        if next_step:
            data['next_step'] = next_step
        elif SIGNUP_EMAIL_CHANGE_TWO_STEPS:
            data['next_step'] = 'continue_email_change'
        else:
            data['next_step'] = 'finish_email_change'

        url = code.confirmation_url_for_data('email_change', data)

        if send_email:
            # %s for PrefProxy objects.
            if data['next_step'] == 'continue_email_change':
                email_text = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_START_BODY
                email_title = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_START_TITLE
                notice = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_START_NOTICE
            else:
                email_text = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_BODY
                email_title = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_TITLE
                notice = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_NOTICE
            send_email_func(email_text % {'url': request.build_absolute_uri(url), 'new_email': new_email}, user, email_title)
            messages.success(request, notice, 'info')
        return url

    @classmethod
    def continue_email_change(cls, prev_code, data, send_email=True, request=None):
        from .utils import send_email as send_email_func
        if prev_code.expired:
            raise ValidationError(_("Confirmation url have already been expired"), code='expired')
        if send_email and not request:
            raise ValueError("``request`` argument is required when ``send_email`` is True")

        prev_code.expired = True
        prev_code.save()
        strict = data.get('strict', False)

        user = prev_code.user
        if strict:
            if (user.email != data['old_email']):
                raise ValidationError(_("Email already changed"))
            if request and request.user != user:
                raise ValidationError(_("You should be logged in to confirm email change"))

        code = cls.add(user)

        new_data = dict(data)
        new_data['next_step'] = 'finish_email_change'

        email_text = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_BODY
        email_title = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_TITLE
        notice = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_NOTICE

        url = code.confirmation_url_for_data('email_change', new_data)

        if send_email:
            send_email_func(email_text % {'url': request.build_absolute_uri(url), 'new_email': data['new_email']}, data['new_email'], email_title)
            messages.success(request, notice, 'info')
        return url

    @classmethod
    def finish_email_change(cls, prev_code, data, send_email=True, request=None):
        from .utils import send_email as send_email_func
        if prev_code.expired:
            raise ValidationError(_("Confirmation url have already been expired"), code='expired')
        if send_email and not request:
            raise ValueError("``request`` argument is required when ``send_email`` is True")

        prev_code.expired = True
        prev_code.save()
        strict = data.get('strict', False)

        user = prev_code.user
        if strict:
            if (user.email != data['old_email']):
                raise ValidationError(_("Email already changed"))
            if request and request.user != user:
                raise ValidationError(_("You should be logged in to confirm email change"))

        user.email = data['new_email']
        user.save()

        email_text = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_BODY
        email_title = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_TITLE
        notice = u'%s' % SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_NOTICE

        if send_email:
            send_email_func(email_text % {'new_email': data['new_email']}, user, email_title)
            messages.success(request, notice, 'info')
        return True


if (django.VERSION < (1, 7)) and SIGNUP_EMAIL_CHANGE_PROCESSING:
    from .signal_receivers import process_email_change
    from .signals import sig_generic_confirmation_received
    sig_generic_confirmation_received.connect(process_email_change)
