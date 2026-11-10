from typing import Optional

from django.contrib.auth import login
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from ..flows_base import FlowsBase
from ..settings import SIGNIN_ENABLED, SIGNIN_DISABLED_TEXT
from ..utils import get_registered_remotes


class SigninFlow(FlowsBase):
    """Base class for sign in flows."""

    flow_type: str = 'signin'
    enabled: bool = SIGNIN_ENABLED
    disabled_text: str = SIGNIN_DISABLED_TEXT

    def get_requested_form(self, request: HttpRequest) -> ModelForm:
        form = super().get_requested_form(request)
        form.remotes = get_registered_remotes().values()
        return form

    def handle_form_valid(self, request: HttpRequest, form: ModelForm) -> Optional[HttpResponse]:
        login(request, form.get_user())

        redirect_to = self.flow_args.get('redirect_to', self.default_redirect_to)

        if redirect_to:  # TODO Handle lambda variant with user as arg.
            return redirect(redirect_to)
