from django.urls import re_path

from .decorators import sitegate_view, signin_view, signup_view, redirect_signedin  # noqa
from .views import verify_email, remote_auth, remote_auth_start
from .utils import register_remotes  # noqa


def get_sitegate_urls() -> list:
    """Returns sitegate urlpatterns, that can be attached
    to urlpatterns of a project:

        # Example from urls.py.

        from sitegate.toolbox import get_sitegate_urls

        urlpatterns = patterns('',
            ...
            path('login/', 'apps.views.login', name='login'),
            ...
        ) + get_sitegate_urls()  # Attach.

    """
    urls = [
        re_path(r'^verify_email/(?P<code>\S+)/$', verify_email, name='verify_email'),
        re_path(r'^rauth/(?P<alias>\S+)/start/$', remote_auth_start, name='remote_auth_start'),
        re_path(r'^rauth/(?P<alias>\S+)/$', remote_auth, name='remote_auth'),
    ]
    return urls
