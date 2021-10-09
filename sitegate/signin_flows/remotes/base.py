import logging
from typing import Optional, List, NamedTuple

from django.contrib.auth import login
from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.utils import timezone

from ...utils import USER

if False:  # pragma: nocover
    from django.contrib.auth.models import User  # noqa
    from ...models import RemoteRecord

LOG = logging.getLogger(__name__)


class UserData(NamedTuple):
    """Basic user data fetched from a remote."""

    username: str
    remote_id: str
    emails: List[str]
    first_name: str
    last_name: str


class Remote:
    """Base class for a Remote - an entity describing
    a remote service, providing information for user sign in.

    """
    alias: str = ''
    title: str = ''

    _auth_fail_prefix = 'Remote auth failed:'

    @classmethod
    def get_user_data(cls, request: HttpRequest, *, data: dict) -> Optional[UserData]:
        """Get user data from a remote.

        :param request:
        :param data: auth data

        """
        raise NotImplementedError  # pragma: nocover

    def construct_user(self, user_data: UserData) -> Optional['User']:
        """Spawns a new user instance. Return None on failure.

        :param user_data:

        """
        # try to get active (presumably with verified emails) users
        # NB: can be slow w/o index on email field if many users
        candidates = USER.objects.filter(email__in=user_data.emails, is_active=True).only('id')

        if len(candidates) == 1:
            # single candidate, let's use it.
            # in case of many candidate we won't guess, but create a new user
            return candidates[0]

        email_field = USER.get_email_field_name()

        def set_email(value: str):
            setattr(user, email_field, value)

        # too many or none candidates. let's create a new user
        user = USER(
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )
        set_email(user_data.emails[0])
        user.set_unusable_password()

        def save() -> bool:
            try:
                user.save()

            except IntegrityError:
                # DB unique username
                return False
            return True

        if not save():
            # current username is already taken
            # let's try getting those from emails
            for email in user_data.emails:
                user.username, _, _ = email.partition('@')
                set_email(email)
                if save():
                    break

            if not user.id:
                # still not saved. let's try emails
                for email in user_data.emails:
                    user.username = email
                    set_email(email)
                    if save():
                        break

            if not user.id:
                # give up trying
                LOG.error(
                    f'{self._auth_fail_prefix} unable to spawn a user '
                    f'for "{user_data.username}" with {user_data.emails}')

        return user if user.id else None

    def get_code_from_data(self, data: dict) -> '':
        """Return code for a RemoteRecord from the given data.

        :param data:

        """
        raise NotImplementedError  # pragma: nocover

    def auth_finish(
            self,
            request: HttpRequest,
            *,
            user_data: UserData,
            remote_record: 'RemoteRecord',
            user: Optional['User'],
    ) -> HttpResponseRedirect:
        """Finishes auth process.

        :param request:
        :param user_data:
        :param remote_record:
        :param user: current authorized user

        """
        with atomic():

            if not user:
                # user is not authorized spawn a new user instance
                try:
                    user = self.construct_user(user_data)

                except Exception as e:
                    LOG.exception(f'{self._auth_fail_prefix} unable to construct a user.')
                    return self.redirect()

            if not user:
                return self.redirect()

            remote_record.remote_id = user_data.remote_id
            remote_record.user = user
            remote_record.time_accepted = timezone.now()
            remote_record.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return self.redirect()

    def auth_continue(self, request: HttpRequest) -> HttpResponse:
        """Continues auth process.

        :param request:

        """
        context = {
            'url': request.build_absolute_uri(),
            'csrf': get_token(request),
            'remote': self,
        }
        return render(request, 'sitegate/remotes/generic.html', context)

    def auth_start(self, *, ticket: str) -> HttpResponseRedirect:
        """Redirects to a remote service to start auth.

        :param ticket: Identifier to prove our site is indeed
            has requested this auth.

        """
        raise NotImplementedError  # pragma: nocover

    def redirect(self, url: str = '') -> HttpResponseRedirect:
        """Performs a redirection to a given URL.

        :param url:

        """
        return redirect(url or '/')
