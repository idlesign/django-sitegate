import hashlib
import hmac
from time import time

from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from .base import Remote, UserData

if False:  # pragma: nocover
    from django.contrib.auth.models import User


class Telegram(Remote):
    """Sign in using Telegram Login Widget.

    Docs: https://core.telegram.org/widgets/login

    Not an OAuth flow: Telegram posts a payload signed with an HMAC
    of the bot token, and the signature is verified locally.

    Create a bot via https://t.me/BotFather and link your domain
    to it with /setdomain. The bot token is the secret.

    """
    alias: str = 'telegram'
    title: str = _('Telegram')

    uses_tickets: bool = False

    data_ttl: int = 86400
    """Signed data time to live in seconds."""

    def __init__(self, *, bot_token: str):
        super().__init__(client_id=bot_token)
        self.bot_token = bot_token

    def get_callback_data(self, request: HttpRequest) -> dict | None:
        """Telegram posts signed data with a `hash` field."""
        data = request.POST.dict() if request.method == 'POST' else request.GET.dict()
        return data if 'hash' in data else None

    def verify_data(self, data: dict) -> bool:
        """Verifies signed data from Telegram: signature and freshness."""
        received_hash = data.get('hash', '')

        check_string = '\n'.join(
            f'{key}={value}'
            for key, value in sorted(data.items())
            if key != 'hash'
        )

        secret = hashlib.sha256(self.bot_token.encode()).digest()
        expected = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected, received_hash):
            return False

        auth_date = data.get('auth_date', '')

        if not auth_date.isdigit():
            return False

        return (time() - int(auth_date)) <= self.data_ttl

    def _get_user_data(self, request: HttpRequest, *, data: dict) -> UserData:

        telegram_id = data['id']

        return UserData(
            remote_id=f'{telegram_id}',
            username=data.get('username') or f'tg{telegram_id}',
            emails=[],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
        )
