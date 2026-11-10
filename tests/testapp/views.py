try:
    from django.http.response import HttpResponse
except ImportError:
    from django.http import HttpResponse
from django.template.base import Template
from django.template.context import Context

from sitegate.decorators import signup_view, redirect_signedin, signin_view


def response_from_string(request, string):
    return HttpResponse(Template(string).render(Context({'request': request})))


@signup_view(activate_user=False, auto_signin=False, validate_email_domain=False, redirect_to='ok')
def register(request):
    return response_from_string(request, '{% load sitegate %}{% sitegate_signup_form %}')


@redirect_signedin('fail')
@signin_view(redirect_to='ok')
def login(request):
    return response_from_string(request, '{% load sitegate %}{% sitegate_signin_form %}')
