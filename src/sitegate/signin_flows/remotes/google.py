from urllib.parse import quote

from django.http import HttpResponseRedirect, HttpRequest
from django.utils.translation import gettext_lazy as _

from .base import Remote, UserData

if False:  # pragma: nocover
    from django.contrib.auth.models import User  # noqa


class Google(Remote):
    """Sign in using Google.

    Docs: https://developers.google.com/identity/protocols/oauth2/javascript-implicit-flow

    Register your OAuth application at
        https://console.cloud.google.com/apis/credentials

        Set scopes:
            https://developers.google.com/identity/protocols/oauth2/scopes?hl=ur#oauth2

            https://www.googleapis.com/auth/userinfo.email --- required
            https://www.googleapis.com/auth/userinfo.profile --- optional

        Set callback URL:
            <your-domain-uri>/rauth/google/

    """
    alias: str = 'google'
    title: str = _('Google')

    @classmethod
    def _get_user_data(cls, request: HttpRequest, *, data: dict) -> UserData:

        user_data = cls._request_json(
            'https://www.googleapis.com/oauth2/v1/userinfo?alt=json',
            headers={'Authorization': f"Bearer {data.get('access_token')}"},
        )

        email = user_data['email']

        if not user_data['verified_email']:
            raise ValueError(f'Email: {email} is not verified')

        login, _, _ = email.partition('@')
        
        user_data = UserData(
            remote_id=user_data['id'],
            username=login,
            emails=[email],
            first_name=user_data.get('given_name', ''),
            last_name=user_data.get('family_name', ''),
        )

        return user_data

    def auth_start(self, request: HttpRequest, *, ticket: str) -> HttpResponseRedirect:
        scope = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'
        return self.redirect(
            'https://accounts.google.com/o/oauth2/v2/auth?response_type=token&'
            f'client_id={self.client_id}&state={ticket}&'
            f'redirect_uri={quote(self.get_url_auth_continue_absolute(request))}&'
            f"scope={quote(scope)}")
