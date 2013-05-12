"""This file contains decorators used by sitegate."""
from functools import wraps

from django.utils.decorators import available_attrs

from .flows.modern import ModernSignup


def signup_view(function=None, **kwargs_dec):
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

    if function:
        return decorated_view(function)

    return decorated_view
