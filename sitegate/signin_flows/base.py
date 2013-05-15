from django import forms
from django.shortcuts import redirect

from ..flows_base import FlowsBase
from ..signals import sig_user_signup_success, sig_user_signup_fail


class SigninFlow(FlowsBase):
    """Base class for sign in flows."""

    flow_type = 'signin'

    def handle_form_valid(self, request, form):
        pass
