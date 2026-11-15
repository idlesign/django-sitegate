from django.utils.translation import gettext_lazy as _

from .base import CodeFlowRemote


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
    url_userinfo = 'https://gitlab.com/api/v4/user'
    scope = 'read_user'
