from django.http import HttpResponseRedirect, HttpRequest
from django.utils.translation import gettext_lazy as _

from .base import Remote, UserData

if False:  # pragma: nocover
    from django.contrib.auth.models import User  # noqa


class Yandex(Remote):
    """Sign in using Yandex.

    Docs: https://yandex.ru/dev/oauth/

    Register your OAuth application at
        https://oauth.yandex.ru/

        Set scopes:
            API Яндекс ID - Доступ к адресу электронной почты --- required
            API Яндекс ID - Доступ к логину, имени и фамилии, полу --- optional

        Set callback URL:
            <your-domain-uri>/rauth/yandex/

    """
    alias: str = 'yandex'
    title: str = _('Yandex')

    @classmethod
    def _get_user_data(cls, request: HttpRequest, *, data: dict) -> UserData:

        user_data = cls._request_json(
            'https://login.yandex.ru/info?format=json',
            headers={'Authorization': f"OAuth {data.get('access_token')}"},
        )

        user_data = UserData(
            remote_id=user_data['id'],
            username=user_data['login'],
            emails=user_data['emails'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
        )

        return user_data

    def auth_start(self, request: HttpRequest, *, ticket: str) -> HttpResponseRedirect:
        return self.redirect(
            'https://oauth.yandex.ru/authorize?response_type=token&'
            f'client_id={self.client_id}&state={ticket}&display=popup')
