from django.shortcuts import redirect
from django.contrib.auth import login

from ..flows_base import FlowsBase
from ..settings import SIGNIN_ENABLED, SIGNIN_DISABLED_TEXT


class SigninFlow(FlowsBase):
    """Base class for sign in flows."""

    flow_type = 'signin'
    enabled = SIGNIN_ENABLED
    disabled_text = SIGNIN_DISABLED_TEXT

    def handle_form_valid(self, request, form):
        login(request, form.get_user())
        redirect_to = self.flow_args.get('redirect_to', self.default_redirect_to)
        if redirect_to:  # TODO Handle lambda variant with user as arg.
            return redirect(redirect_to)
