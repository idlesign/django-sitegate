import logging
from typing import Optional, List, NamedTuple

import requests
from django.contrib.auth import login
from django.db import IntegrityError
from django.db.transaction import atomic
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.functional import cached_property
from etc.toolbox import get_site_url

from ...signals import sig_user_signup_success, sig_user_signup_fail
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

    def __init__(self, *, client_id: str):
        self.client_id = client_id

    def __str__(self):
        return f'{self.alias}'

    @classmethod
    def _get_user_data(cls, request: HttpRequest, *, data: dict) -> UserData:
        """Get user data from a remote.

        :param request:
        :param data: auth data

        """
        raise NotImplementedError  # pragma: nocover

    @classmethod
    def _request_json(cls, url: str, *, headers: dict = None) -> dict:
        """Sends a request to get a json.

        :param url:
        :param headers:

        """
        headers = {
            **(headers or {}),
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=4,
        )

        response.raise_for_status()
        return response.json()

    @cached_property
    def url_auth_start(self) -> str:
        """URL to start this remote auth with."""
        return reverse('remote_auth_start', kwargs={'alias': self.alias})

    @cached_property
    def url_auth_continue(self) -> str:
        """URL to continue this remote auth with."""
        return reverse('remote_auth', kwargs={'alias': self.alias})

    def get_url_auth_continue_absolute(self, request: HttpRequest) -> str:
        """URL to continue this remote auth with.
        Also known as a Callback URL in OAuth process.

        """
        return f'{get_site_url(request)}{self.url_auth_continue}'

    def get_user_data(self, request: HttpRequest, *, data: dict) -> Optional[UserData]:
        """Get user data from a remote.

        :param request:
        :param data: auth data

        """
        try:
            return self._get_user_data(request, data=data)

        except Exception as _:
            LOG.exception(f'{self._auth_fail_prefix} unable get user data from remote.')
            return None

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

    def get_code_from_data(self, data: dict) -> str:
        """Returns a our code (from RemoteRecord.code) from data
        received from a remote.

        :param data:

        """
        return data.get('state', '').strip()

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
        flow_name = f'remote-{remote_record.remote_id}'

        with atomic():

            if not user:
                # user is not authorized spawn a new user instance
                try:
                    user = self.construct_user(user_data)

                except Exception as _:
                    LOG.exception(f'{self._auth_fail_prefix} unable to construct a user.')
                    sig_user_signup_fail.send(self, signup_result=None, flow=flow_name, request=request)
                    user = None

            if user:
                remote_record.remote_id = user_data.remote_id
                remote_record.user = user
                remote_record.time_accepted = timezone.now()
                remote_record.save()

        if not user:
            return self.redirect()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        sig_user_signup_success.send(
            self,
            signup_result=user,
            flow=flow_name,
            request=request)

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

    def auth_start(self, request: HttpRequest, *, ticket: str) -> HttpResponseRedirect:
        """Redirects to a remote service to start auth.

        :param request:
        :param ticket: Identifier to prove our site is indeed
            has requested this auth.

        """
        raise NotImplementedError  # pragma: nocover

    def redirect(self, url: str = '') -> HttpResponseRedirect:
        """Performs a redirection to a given URL.

        :param url:

        """
        return redirect(url or '/')
