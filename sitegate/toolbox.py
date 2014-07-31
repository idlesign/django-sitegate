from django.conf.urls import patterns, url


def get_sitegate_urls():
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
    return patterns('', url(r'^verify_email/(?P<code>\S+)/$', 'sitegate.views.verify_email', name='verify_email'))
