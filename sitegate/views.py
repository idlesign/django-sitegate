from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

from .models import EmailConfirmation
from .settings import SIGNUP_VERIFY_EMAIL_ERROR_TEXT, SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT


def verify_email(request: HttpRequest, code: str, redirect_to: str = None) -> HttpResponse:
    """Verifies an account activation code a user received by e-mail.

    Requires Messages Django Contrib.

    :param request:
    :param code:
    :param redirect_to:

    """
    success = False

    valid_code = EmailConfirmation.is_valid(code)
    if valid_code:
        valid_code.activate()
        success = True

    if success:
        messages.success(request, SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT, 'success')
    else:
        messages.error(request, SIGNUP_VERIFY_EMAIL_ERROR_TEXT, 'danger error')

    if redirect_to is None:
        redirect_to = '/'

    return redirect(redirect_to)
