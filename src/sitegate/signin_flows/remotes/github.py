from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .base import CodeFlowRemote, UserData

if False:  # pragma: nocover
    from django.contrib.auth.models import User


class Github(CodeFlowRemote):
    """Sign in using GitHub.

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

    url_authorize = 'https://github.com/login/oauth/authorize'
    url_token = 'https://github.com/login/oauth/access_token'
    scope = 'user:email'

    def _get_user_data(self, request: HttpRequest, *, data: dict) -> UserData:

        token = self.exchange_code(request, data['code'])
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
