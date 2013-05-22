"""Contains utility functions used by sitegate."""
from functools import wraps

from django.utils.decorators import available_attrs

# Custom User model - Django 1.4 backward compatibility.
try:
    from django.contrib.auth import get_user_model
    USER = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    USER = User


def apply_attrs_to_form_widgets(form, attrs):
    """Applies the given html attributes to each form field widget."""
    for _, field in form.fields.items():
        attrs_ = dict(attrs)
        for name, val in attrs.items():
            if hasattr(val, '__call__'):
                attrs_[name] = val(field)
        field.widget.attrs = field.widget.build_attrs(attrs_)


class DecoratorBuilder(object):
    """Decorators builder. Facilitates decorators creation.
    Inherit from this and implement `handle` method.

    """

    def __init__(self, args, kwargs):
        """Accepts decoration function arguments."""
        self._args_dec = list(args)
        self._kwargs_dec = dict(kwargs)

    def handle(self, func, args_func, kwargs_func, args_dec, kwargs_dec):
        raise NotImplementedError('Please implement `handle` method.')

    def __call__(self, *args_call, **kwargs_call):
        def decorated(view_function):
            @wraps(view_function, assigned=available_attrs(view_function))
            def catcher(*args_func, **kwargs_func):
                return self.handle(view_function, args_func, kwargs_func, self._args_dec, self._kwargs_dec)
            return catcher

        # Case one: @dec('a', b='b')
        if len(args_call) and hasattr(args_call[0], '__call__'):
            return decorated(args_call[0])

        # Case two: @dec
        if len(self._args_dec) and hasattr(self._args_dec[0], '__call__'):
            return decorated(self._args_dec[0])(*args_call, **kwargs_call)

        return decorated
