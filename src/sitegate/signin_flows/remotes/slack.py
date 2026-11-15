from django.utils.translation import gettext_lazy as _

from .base import CodeFlowRemote


class Slack(CodeFlowRemote):
    """Sign in using Slack (OpenID Connect).

    Docs: https://api.slack.com/authentication/sign-in-with-slack

    Register your OAuth application at
        https://api.slack.com/apps

        Set scopes:
            openid email profile

        Set callback URL:
            <your-domain-uri>/rauth/slack/

    """
    alias: str = 'slack'
    title: str = _('Slack')

    url_authorize = 'https://slack.com/oauth/v2/authorize'
    url_token = 'https://slack.com/api/oauth.v2.access'
    url_userinfo = 'https://slack.com/api/openid.connect.userinfo'
    scope = 'openid email profile'

    user_field_id = 'sub'
    user_field_username = 'email'
