from uuid import uuid4

from django.db import models, IntegrityError
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from etc.models import InheritedModel


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


@python_2_unicode_compatible
class BlacklistedDomain(models.Model):

    domain = models.CharField(_('Domain name'), max_length=253, unique=True)
    enabled = models.BooleanField(_('Enabled'), help_text=_('If enabled visitors won\'t be able to sign up with this domain name in e-mail.'), db_index=True, default=True)

    class Meta:
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

    @classmethod
    def is_valid(cls, code):
        try:
            return cls.objects.get(code=code, expired=False)
        except (cls.MultipleObjectsReturned, cls.DoesNotExist):
            return False

    @staticmethod
    def generate_code():
        return str(uuid4()).replace('-', '')

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

    def __str__(self):
        return self.code

    class Meta:
        abstract = True


class InvitationCode(InheritedModel, ModelWithCode):

    class Fields:
        code = _('Invitation code')
        expired = {'help_text': _('Visitors won\'t be able to sign up with an expired code.')}

    creator = models.ForeignKey(USER_MODEL, related_name='creators', verbose_name=_('Creator'))
    acceptor = models.ForeignKey(USER_MODEL, related_name='acceptors', verbose_name=_('Acceptor'), null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _('Invitation code')
        verbose_name_plural = _('Invitation codes')

    @classmethod
    def add(cls, creator):
        new_code = cls(creator=creator)
        new_code.save(force_insert=True)
        return new_code

    @classmethod
    def accept(cls, code, acceptor):
        return cls.objects.filter(code=code).update(acceptor=acceptor, expired=True, time_accepted=timezone.now())


class EmailConfirmation(InheritedModel, ModelWithCode):

    class Fields:
        code = _('Activation code')
        expired = {'help_text': _('Expired codes couldn\'t be used for repeated account activations.')}

    user = models.ForeignKey(USER_MODEL, verbose_name=_('User'))

    class Meta:
        verbose_name = _('Activation code')
        verbose_name_plural = _('Activation codes')

    @classmethod
    def add(cls, user):
        new_code = cls(user=user)
        new_code.save(force_insert=True)
        return new_code

    def activate(self):
        self.expired = True
        self.time_accepted = timezone.now()
        self.save()

        user = self.user
        user.is_active = True
        user.save()
