from uuid import uuid4

from django.db import models, IntegrityError
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


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
        blacklisted = cls.objects.filter(enabled=True).values('domain')
        for domain in blacklisted:
            if email.endswith(domain['domain']):
                return True
        return False


@python_2_unicode_compatible
class InvitationCode(models.Model):

    code = models.CharField(_('Invitation code'), max_length=128, unique=True, editable=False)
    time_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    time_accepted = models.DateTimeField(_('Date accepted'), null=True, editable=False)
    creator = models.ForeignKey(USER_MODEL, related_name='creators', verbose_name=_('Creator'))
    acceptor = models.ForeignKey(USER_MODEL, related_name='acceptors', verbose_name=_('Acceptor'), null=True, blank=True, editable=False)
    expired = models.BooleanField(_('Expired'), help_text=_('Visitors won\'t be able to sign up with an expired code.'), db_index=True, default=False)

    class Meta:
        verbose_name = _('Invitation code')
        verbose_name_plural = _('Invitation codes')

    @staticmethod
    def generate_code():
        return str(uuid4()).replace('-', '')

    @classmethod
    def add(cls, creator):
        new_code = cls(creator=creator)
        new_code.save(force_insert=True)
        return new_code

    @classmethod
    def is_valid(cls, code):
        try:
            cls.objects.get(code=code, expired=False)
        except (cls.MultipleObjectsReturned, cls.DoesNotExist):
            return False
        return True

    @classmethod
    def accept(cls, code, acceptor):
        return cls.objects.filter(code=code).update(acceptor=acceptor, expired=True, time_accepted=timezone.now())

    def save(self, force_insert=False, force_update=False, **kwargs):
        if self.code == '':
            while True:
                self.code = self.generate_code()
                try:
                    super(InvitationCode, self).save(force_insert, force_update, **kwargs)
                except IntegrityError:
                    pass
                else:
                    break
        else:
            super(InvitationCode, self).save(force_insert, force_update, **kwargs)

    def __str__(self):
        return self.code

