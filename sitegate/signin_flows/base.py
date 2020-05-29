from typing import Optional

from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import login

from ..flows_base import FlowsBase
from ..settings import SIGNIN_ENABLED, SIGNIN_DISABLED_TEXT


class SigninFlow(FlowsBase):
    """Base class for sign in flows."""

    flow_type: str = 'signin'
    enabled: bool = SIGNIN_ENABLED
    disabled_text: str = SIGNIN_DISABLED_TEXT

    def handle_form_valid(self, request: HttpRequest, form: ModelForm) -> Optional[HttpResponse]:
        login(request, form.get_user())

        redirect_to = self.flow_args.get('redirect_to', self.default_redirect_to)

        if redirect_to:  # TODO Handle lambda variant with user as arg.
            return redirect(redirect_to)
