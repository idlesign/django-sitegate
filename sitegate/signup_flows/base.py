from collections import OrderedDict

from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from ..utils import apply_attrs_to_form_widgets
from ..signals import sig_user_signup_success, sig_user_signup_fail


class SignupFlow():
    """Base class for sign up flows."""

    form_template = 'sitesignup/form_as_p.html'
    redirect_to = '/'
    auto_login = True

    def __init__(self, **kwargs):
        if not getattr(self, 'form', False):
            raise NotImplementedError('Please define `form` attribute in your `%s` class.' % self.__class__.__name__)
        self.flow_args = kwargs

    @classmethod
    def get_flow_name(cls):
        """Returns sign up flow identifier from flow class name.
        Example: `classic` for `ClassicSignup`.

        """
        return cls.__name__.lower().replace('signup', '')

    def process_request(self, request, view_function, *args, **kwargs):
        """Makes the given request ready to handle sign ups and handles them."""
        try:
            signup_dict = request.sitesignup
        except AttributeError:
            # Use ordered forms dict in case sitesignup_formNode wants to fetch the first defined.
            signup_dict = {'forms': OrderedDict()}

        flow_name = self.get_flow_name()
        form_data = None

        if request.POST.get('signup_flow', False) and request.POST['signup_flow'] == flow_name:
            form_data = request.POST

        form = self.get_form(form_data, widget_attrs=self.flow_args.pop('widget_attrs', None), template=self.flow_args.pop('template', None))
        # Attach flow identifying field to differentiate among several possible sign up forms.
        form.fields['signup_flow'] = forms.CharField(required=True, initial=flow_name, widget=forms.HiddenInput)

        if form.is_valid():
            signup_result = self.add_user(request, form)
            if signup_result:
                sig_user_signup_success.send(self, signup_result=signup_result, flow=flow_name, request=request)
                auto_login = self.flow_args.pop('auto_login', self.auto_login)
                if auto_login:
                    self.sign_in(request, form, signup_result)
                redirect_to = self.flow_args.pop('redirect_to', self.redirect_to)
                if redirect_to:  # TODO Handle lambda variant with user as arg.
                    return redirect(redirect_to)
            else:
                sig_user_signup_fail.send(self, signup_result=signup_result, flow=flow_name, request=request)

        signup_dict['forms'][flow_name] = form
        request.sitesignup = signup_dict
        return view_function(request, *args, **kwargs)

    @staticmethod
    def login_generic(request, username, password):
        """Helper method. Generic login with username and password."""
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return True
        return False

    def add_user(self, request, form):
        """Adds (creates) user using form data."""
        raise NotImplementedError('Please implement `add_user()` method in your `%s` class.' % self.__class__.__name__)

    def sign_in(self, request, form, signup_result):
        """Signs in a user."""
        raise NotImplementedError('Please implement `login()` method in your `%s` class.' % self.__class__.__name__)

    def get_form(self, form_data, widget_attrs=None, template=None):
        """Constructs, populates and returns a sign up form."""
        form = self.form(form_data)
        if template is not None:
            form.template = template
        else:
            form.template = self.form_template
        if widget_attrs is not None:
            apply_attrs_to_form_widgets(form, widget_attrs)
        return form
