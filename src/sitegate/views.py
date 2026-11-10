from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.views.decorators.csrf import requires_csrf_token

from .models import EmailConfirmation, RemoteRecord
from .settings import SIGNUP_VERIFY_EMAIL_ERROR_TEXT, SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT
from .utils import get_registered_remotes


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


@requires_csrf_token
def remote_auth(request: HttpRequest, alias: str) -> HttpResponse:
    """Performs an authorization using data from a remote.
    
    For a user which is anonymous or not yet linked to target remote.

    :param request:
    :param alias: remote service alias

    """
    remote = get_registered_remotes().get(alias)

    if not remote:
        return HttpResponseBadRequest()

    if request.method == 'POST':
        data = request.POST.dict()
        code = remote.get_code_from_data(data)

        if not code:
            return remote.redirect()

        manager = RemoteRecord.objects

        remote_record = manager.filter(
            code=code,
            remote=alias,
        ).select_related('user').first()

        if not remote_record:
            return remote.redirect()

        user = remote_record.user
        request_user = request.user
        request_user = None if request_user.is_anonymous else request_user

        if user != request_user:
            # in case someone tries to mess with us
            return remote.redirect()

        user_data = remote.get_user_data(request, data=data)

        if not user_data:
            return remote.redirect()

        # try to find previous records for this remote_id
        previous_record = manager.filter(
            remote=alias,
            remote_id=user_data.remote_id,
        ).select_related('user').first()

        if previous_record:
            user = previous_record.user
            remote_record = previous_record

        return remote.auth_finish(
            request,
            user_data=user_data,
            remote_record=remote_record,
            user=user,
        )

    # this is GET
    return remote.auth_continue(request)


def remote_auth_start(request: HttpRequest, alias: str) -> HttpResponse:
    """Performs a redirect to another service for remote auth.

    :param request:
    :param alias: remote service alias

    """
    if not request.method == 'POST':
        return HttpResponseNotAllowed(['post'])

    remote = get_registered_remotes().get(alias)

    if not remote:
        return HttpResponseBadRequest()

    user = request.user

    if user.is_anonymous:
        user = None

    else:
        if RemoteRecord.objects.filter(user=user, remote=alias).exists():
            # local user profile is already signe in and linked to this remote
            return remote.redirect()

    # create a record bound to an unregistered or unlinked user
    record = RemoteRecord.add(
        remote=alias,
        user=user,
    )

    return remote.auth_start(request, ticket=record.code)
