from django.urls import path
from pytest_djangoapp.compat import get_urlpatterns

from sitegate.toolbox import get_sitegate_urls
from .views import login, register, HttpResponse


urlpatterns = get_urlpatterns([
    path('entrance/', lambda r: None),
    path('ok/', lambda r: HttpResponse('ok'), name='ok'),
    path('fail/', lambda r: HttpResponse('fail'), name='fail'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
] + get_sitegate_urls())
