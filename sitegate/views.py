from django.contrib import messages
from django.core import signing
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import EmailConfirmation
from .settings import SIGNUP_VERIFY_EMAIL_ERROR_TEXT, SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT, SIGNUP_VERIFY_EMAIL_GENERIC_VIEW_DOMAIN_ARG
from .signals import sig_generic_confirmation_received


def verify_email(request, code, redirect_to=None):
    """Verifies an account activation code a user received by e-mail.

    Requires Messages Django Contrib.

    :param Requset request:
    :param str code:
    :param str redirect_to:
    :return:
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


def generic_confirmation(request, confirmation_domain, code, encrypted_data, redirect_to=None):
    """Verify code, decrypt data, fire signal and redirect.

    Redirect to: ``decrypted_data['redirect_to']`` or ``redirect_to`` argument or '/'.

    """
    code = get_object_or_404(EmailConfirmation, code=code)

    try:
        decrypted_data = code.decrypt_data(encrypted_data)
    except (signing.BadSignature):
        # someone tries to spoof data. Show no differece in wrong code and wrong data behaviour
        raise Http404

    try:
        sig_generic_confirmation_received.send(
            sender=generic_confirmation,
            confirmation_domain=confirmation_domain,
            code=code,
            decrypted_data=decrypted_data,
            request=request
        )
    except ValidationError as e:
        messages.error(request, '; '.join(e.messages), 'danger error')

    if confirmation_domain == SIGNUP_VERIFY_EMAIL_GENERIC_VIEW_DOMAIN_ARG:
        # this can be done through signal processing but "Explicit is better than implicit"
        success = False
        if code and (decrypted_data['email'] == code.user.email) and not code.expired:
            code.activate()
            success = True

        if success:
            messages.success(request, SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT, 'success')
        else:
            messages.error(request, SIGNUP_VERIFY_EMAIL_ERROR_TEXT, 'danger error')

    redirect_to = decrypted_data.get('redirect_to', None) or redirect_to or '/'
    return redirect(redirect_to)
