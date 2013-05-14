"""This file contains decorators used by sitegate."""
from functools import wraps

from django.utils.decorators import available_attrs
from django.shortcuts import redirect

from .signup_flows.modern import ModernSignup


def signup_view(func=None, **kwargs_dec):
    """Decorator to mark views used for sign up."""
    def decorated_view(view_function):
        @wraps(view_function, assigned=available_attrs(view_function))
        def wrapper(request, *args, **kwargs):

            kwargs_dec_ = dict(kwargs_dec)
            flow_class = kwargs_dec_.pop('flow', None)
            if flow_class is None:
                flow_class = ModernSignup
            flow_obj = flow_class(**kwargs_dec_)

            return flow_obj.process_request(request, view_function, *args, **kwargs)
        return wrapper

    if func:
        return decorated_view(func)

    return decorated_view


def redirect_signedin(to='/', *args_dec, **kwargs_dec):
    """Decorator to mark views which should not be accessed by signed in users.
    Example: sign in & sign up pages.

    """
    def decorated_view(view_function, actual_to=to):
        @wraps(view_function, assigned=available_attrs(view_function))
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated():
                return redirect(actual_to, *args_dec, **kwargs_dec)
            return view_function(request, *args, **kwargs)
        return wrapper

    if hasattr(to, '__call__'):  # No params decorator.
        return decorated_view(to, '/')

    return decorated_view
