from django.shortcuts import redirect

from ..flows_base import FlowsBase
from ..signals import sig_user_signup_success, sig_user_signup_fail
from ..settings import SIGNUP_ENABLED, SIGNUP_DISABLED_TEXT


class SignupFlow(FlowsBase):
    """Base class for signup flows."""

    flow_type = 'signup'
    auto_signin = True
    activate_user = True
    enabled = SIGNUP_ENABLED
    disabled_text = SIGNUP_DISABLED_TEXT

    def handle_form_valid(self, request, form):
        flow_name = self.get_flow_name()
        if not self.get_arg_or_attr('activate_user'):
            form.instance.is_active = False
        signup_result = self.add_user(request, form)
        if signup_result:
            sig_user_signup_success.send(self, signup_result=signup_result, flow=flow_name, request=request)
            if self.get_arg_or_attr('auto_signin'):
                self.sign_in(request, form, signup_result)
            redirect_to = self.flow_args.get('redirect_to', self.default_redirect_to)
            if redirect_to:  # TODO Handle lambda variant with user as arg.
                return redirect(redirect_to)
        else:
            sig_user_signup_fail.send(self, signup_result=signup_result, flow=flow_name, request=request)

    def add_user(self, request, form):
        """Adds (creates) user using form data."""
        raise NotImplementedError('Please implement `add_user()` method in your `%s` class.' % self.__class__.__name__)

    def sign_in(self, request, form, signup_result):
        """Signs in a user."""
        raise NotImplementedError('Please implement `login()` method in your `%s` class.' % self.__class__.__name__)
