from django.conf.urls import url

from .views import verify_email


def get_sitegate_urls() -> list:
    """Returns sitegate urlpatterns, that can be attached
    to urlpatterns of a project:

        # Example from urls.py.

        from sitegate.toolbox import get_sitegate_urls

        urlpatterns = patterns('',
            ...
            url(r'^login/$', 'apps.views.login', name='login'),
            ...
        ) + get_sitegate_urls()  # Attach.

    """
    url_verify = url(r'^verify_email/(?P<code>\S+)/$', verify_email, name='verify_email')

    return [url_verify]
