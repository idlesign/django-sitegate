from datetime import timedelta
from typing import Optional
from uuid import uuid4

from django.conf import settings
from django.db import models, IntegrityError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from etc.models import InheritedModel

if False:  # pragma: nocover
    from django.contrib.auth.models import User  # noqa


USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class BlacklistedDomain(models.Model):

    domain = models.CharField(_('Domain name'), max_length=253, unique=True)

    enabled = models.BooleanField(
        _('Enabled'),
        help_text=_('If enabled visitors won\'t be able to sign up with this domain name in e-mail.'),
        db_index=True, default=True)

    class Meta:
        verbose_name = _('Blacklisted domain')
        verbose_name_plural = _('Blacklisted domains')

    @classmethod
    def is_blacklisted(cls, email: str) -> bool:
        """Checks whether the given e-mail is blacklisted.

        :param email:

        """
        domain = email.split('@', 1)[1].lower()

        # 'some.denied.co.uk' -> ['some.denied.co.uk', 'denied.co.uk', 'co.uk']
        sub_domains = [domain]
        for i in range(domain.count('.') - 1):
            sub_domains.append(sub_domains[i].split('.', 1)[-1])

        return cls.objects.filter(enabled=True, domain__in=sub_domains).exists()

    def __str__(self):
        return self.domain


class ModelWithCode(models.Model):

    code = models.CharField('dummy', max_length=128, unique=True, editable=False)
    time_created = models.DateTimeField(_('Date created'), auto_now_add=True)
    time_accepted = models.DateTimeField(_('Date accepted'), null=True, editable=False)
    expired = models.BooleanField(_('Expired'), help_text='dummy', db_index=True, default=False)

    class Meta:
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
    def is_valid(cls, code: str) -> bool:

        try:
            return cls.objects.get(code=code, expired=False)

        except (cls.MultipleObjectsReturned, cls.DoesNotExist):
            return False

    @staticmethod
    def generate_code() -> str:
        return str(uuid4()).replace('-', '')


class InvitationCode(InheritedModel, ModelWithCode):

    creator = models.ForeignKey(
        USER_MODEL, related_name='creators', verbose_name=_('Creator'), on_delete=models.CASCADE)

    acceptor = models.ForeignKey(
        USER_MODEL, related_name='acceptors', verbose_name=_('Acceptor'), null=True, blank=True,
        editable=False, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Invitation code')
        verbose_name_plural = _('Invitation codes')

    class Fields:
        code = _('Invitation code')
        expired = {'help_text': _('Visitors won\'t be able to sign up with an expired code.')}

    @classmethod
    def add(cls, creator: 'User') -> 'InvitationCode':
        new_code = cls(creator=creator)
        new_code.save(force_insert=True)
        return new_code

    @classmethod
    def accept(cls, code: str, acceptor: 'User'):
        return cls.objects.filter(code=code).update(acceptor=acceptor, expired=True, time_accepted=timezone.now())


class EmailConfirmation(InheritedModel, ModelWithCode):

    user = models.ForeignKey(USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Activation code')
        verbose_name_plural = _('Activation codes')

    class Fields:
        code = _('Activation code')
        expired = {'help_text': _('Expired codes couldn\'t be used for repeated account activations.')}

    @classmethod
    def add(cls, user: 'User') -> 'EmailConfirmation':
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


class RemoteRecord(ModelWithCode):
    """Stores data used for sign ins using remote services."""

    remote = models.CharField(_('Remote alias'), max_length=20, db_index=True)

    remote_id = models.CharField(
        _('Remote ID'), null=True, default=None, max_length=64, db_index=True, db_column='rid')

    user = models.ForeignKey(
        USER_MODEL, null=True, blank=True,
        related_name='remotes', verbose_name=_('User'), on_delete=models.CASCADE)

    expired = None

    class Meta:
        verbose_name = _('Remote record')
        verbose_name_plural = _('Remotes records')

    def __str__(self):
        return f'{self.remote} {self.code}'

    @classmethod
    def add(cls, *, remote: str, user: Optional['User']) -> 'RemoteRecord':
        record = cls(
            remote=remote,
            user=user,
        )
        record.save(force_insert=True)
        return record

    @classmethod
    def cleanup(cls, *, ago: int = None):
        """Removes remote records not linked to certain user.
        Useful for periodic background cleaning.

        :param ago: Days. Allows cleanup for stale records created X days ago.
            Defaults to None (cleanup all stale).

        """
        filter_kwargs = {
            'remote_id__isnull': True,
            'user_id__isnull': True,
        }

        if ago:
            filter_kwargs['time_created__lte'] = timezone.now() - timedelta(days=int(ago))

        cls.objects.filter(**filter_kwargs).delete()
