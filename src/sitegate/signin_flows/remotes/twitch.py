from django.utils.translation import gettext_lazy as _

from .base import CodeFlowRemote


class Twitch(CodeFlowRemote):
    """Sign in using Twitch.

    Docs: https://dev.twitch.tv/docs/authentication/

    Register your OAuth application at
        https://dev.twitch.tv/console/apps

        Set scopes:
            user:read:email

        Set callback URL:
            <your-domain-uri>/rauth/twitch/

    """
    alias: str = 'twitch'
    title: str = _('Twitch')

    url_authorize = 'https://id.twitch.tv/oauth2/authorize'
    url_token = 'https://id.twitch.tv/oauth2/token'
    url_userinfo = 'https://api.twitch.tv/helix/users'
    scope = 'user:read:email'

    userinfo_root = 'data'
    user_field_id = 'id'
    user_field_username = 'login'
    user_field_name = 'display_name'

    def get_userinfo_headers(self, token: str) -> dict:
        """Twitch requires the client id alongside the token."""
        return {'Authorization': f'Bearer {token}', 'Client-Id': self.client_id}
