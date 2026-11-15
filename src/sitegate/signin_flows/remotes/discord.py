from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .base import CodeFlowRemote, UserData

if False:  # pragma: nocover
    from django.contrib.auth.models import User


class Discord(CodeFlowRemote):
    """Sign in using Discord.

    Docs: https://discord.com/developers/docs/topics/oauth2

    Register your OAuth application at
        https://discord.com/developers/applications

        Set scopes:
            identify email

        Set callback URL:
            <your-domain-uri>/rauth/discord/

    """
    alias: str = 'discord'
    title: str = _('Discord')

    url_authorize = 'https://discord.com/oauth2/authorize'
    url_token = 'https://discord.com/api/oauth2/token'
    scope = 'identify email'

    def _get_user_data(self, request: HttpRequest, *, data: dict) -> UserData:

        token = self.exchange_code(request, data['code'])

        user = self._request_json(
            'https://discord.com/api/users/@me',
            headers={'Authorization': f'Bearer {token}'},
        )

        if not user.get('verified'):
            raise ValueError('Email is not verified')

        email = user.get('email') or ''
        name = (user.get('global_name') or '').split(' ', 1)

        return UserData(
            remote_id=f"{user['id']}",
            username=user['username'],
            emails=[email] if email else [],
            first_name=name[0] or '',
            last_name=name[1] if len(name) > 1 else '',
        )
