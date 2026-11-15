from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .base import CodeFlowRemote, UserData

if False:  # pragma: nocover
    from django.contrib.auth.models import User


class Gitlab(CodeFlowRemote):
    """Sign in using GitLab.

    Docs: https://docs.gitlab.com/ee/api/oauth2.html

    Register your OAuth application at
        https://gitlab.com/-/user_settings/applications

        Set scopes:
            read_user

        Set callback URL:
            <your-domain-uri>/rauth/gitlab/

    """
    alias: str = 'gitlab'
    title: str = _('GitLab')

    url_authorize = 'https://gitlab.com/oauth/authorize'
    url_token = 'https://gitlab.com/oauth/token'
    scope = 'read_user'

    def _get_user_data(self, request: HttpRequest, *, data: dict) -> UserData:

        token = self.exchange_code(request, data['code'])

        user = self._request_json(
            'https://gitlab.com/api/v4/user',
            headers={'Authorization': f'Bearer {token}'},
        )

        name = (user.get('name') or '').split(' ', 1)
        email = user.get('email') or ''

        return UserData(
            remote_id=str(user['id']),
            username=user['username'],
            emails=[email] if email else [],
            first_name=name[0] or '',
            last_name=name[1] if len(name) > 1 else '',
        )
