"""This file contains decorators used by sitegate."""
from django.shortcuts import redirect

from .signup_flows.modern import ModernSignup
from .signin_flows.modern import ModernSignin
from .utils import DecoratorBuilder


class FlowBuilder(DecoratorBuilder):

    def __init__(self, flow_cls, args, kwargs):
        self.flow_cls = flow_cls
        super(FlowBuilder, self).__init__(args, kwargs)

    def handle(self, func, args_func, kwargs_func, args_dec, kwargs_dec):
        kwargs_dec_ = dict(kwargs_dec)
        flow_class = kwargs_dec_.pop('flow', None)
        if flow_class is None:
            flow_class = self.flow_cls
        flow_obj = flow_class(**kwargs_dec_)
        return flow_obj.respond_for(func, args_func, kwargs_func)


class RedirectBuilder(DecoratorBuilder):

    def handle(self, func, args_func, kwargs_func, args_dec, kwargs_dec):
        if args_func[0].user.is_authenticated():
            args_dec_ = list(args_dec)
            if hasattr(args_dec[0], '__call__'):
                args_dec_.insert(0, '/')
            return redirect(*args_dec_, **kwargs_dec)
        return func(*args_func, **kwargs_func)


def signup_view(*args, **kwargs):
    """Decorator to mark views used for signup."""
    return FlowBuilder(ModernSignup, args, kwargs)


def signin_view(*args, **kwargs):
    """Decorator to mark views used for sign in."""
    return FlowBuilder(ModernSignin, args, kwargs)


def redirect_signedin(*args, **kwargs):
    """Decorator to mark views which should not be accessed by signed in users.
    Example: sign in & sign up pages.

    """
    return RedirectBuilder(args, kwargs)


def sitegate_view(*args_dec, **kwargs_dec):
    """Decorator to mark views used both for signup & sign in."""
    if len(args_dec):  # simple decoration w/o parameters
        return signup_view(signin_view(redirect_signedin(*args_dec, **kwargs_dec)))

    signin = signin_view(**kwargs_dec)
    signup = signup_view(**kwargs_dec)
    return lambda *args, **kwargs: signup(signin(redirect_signedin(*args, **kwargs)))
