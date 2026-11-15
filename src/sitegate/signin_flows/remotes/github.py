from urllib.parse import quote

import requests
from django.http import HttpRequest, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from .base import Remote, UserData

if False:  # pragma: nocover
    from django.contrib.auth.models import User


class Github(Remote):
    """Sign in using GitHub (authorization code flow).

    Docs: https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps

    Register your OAuth application at
        https://github.com/settings/developers

        Set scopes:
            user:email

        Set callback URL:
            <your-domain-uri>/rauth/github/

    """
    alias: str = 'github'
    title: str = _('GitHub')

    def __init__(self, *, client_id: str, client_secret: str):
        super().__init__(client_id=client_id)
        self.client_secret = client_secret

    def get_callback_data(self, request: HttpRequest) -> dict | None:
        """GitHub calls back with GET carrying `code` and `state`."""
        if request.method == 'GET' and 'code' in request.GET:
            return request.GET.dict()

        return None

    def auth_start(self, request: HttpRequest, *, ticket: str) -> HttpResponseRedirect:
        return self.redirect(
            'https://github.com/login/oauth/authorize?'
            f'client_id={self.client_id}&state={ticket}&'
            f'redirect_uri={quote(self.get_url_auth_continue_absolute(request))}&'
            f'scope={quote("user:email")}')

    def exchange_code(self, code: str) -> str:
        """Exchanges an authorization code for an access token."""
        response = requests.post(
            'https://github.com/login/oauth/access_token',
            json={'client_id': self.client_id, 'client_secret': self.client_secret, 'code': code},
            headers={'Accept': 'application/json'},
            timeout=4,
        )
        response.raise_for_status()
        return response.json()['access_token']

    def _get_user_data(self, request: HttpRequest, *, data: dict) -> UserData:

        token = self.exchange_code(data['code'])
        headers = {'Authorization': f'Bearer {token}'}

        user = self._request_json('https://api.github.com/user', headers=headers)

        emails_response = self._request_json('https://api.github.com/user/emails', headers=headers)

        emails = [
            entry['email']
            for entry in emails_response
            if entry.get('verified') and entry.get('primary')
        ]

        if not emails:
            emails = [entry['email'] for entry in emails_response if entry.get('verified')]

        if user.get('email'):
            emails = [user['email'], *[email for email in emails if email != user['email']]]

        name = (user.get('name') or '').split(' ', 1)

        return UserData(
            remote_id=str(user['id']),
            username=user['login'],
            emails=emails,
            first_name=name[0] or '',
            last_name=name[1] if len(name) > 1 else '',
        )
