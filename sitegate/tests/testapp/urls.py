from django.conf.urls import url
from pytest_djangoapp.compat import get_urlpatterns

from sitegate.toolbox import get_sitegate_urls
from .views import login, register, HttpResponse


urlpatterns = get_urlpatterns([
    url(r'entrance/', lambda r: None),
    url(r'^ok/$', lambda r: HttpResponse('ok'), name='ok'),
    url(r'^fail/$', lambda r: HttpResponse('fail'), name='fail'),
    url(r'^login/$', login, name='login'),
    url(r'^register/$', register, name='register'),
] + get_sitegate_urls())
