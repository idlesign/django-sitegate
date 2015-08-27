"""Contains utility functions used by sitegate."""
from functools import wraps

from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import available_attrs

# Custom User model - Django 1.4 backward compatibility.
try:
    from django.contrib.auth import get_user_model
    USER = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
    USER = User
    get_user_model = lambda: USER

get_username_field = lambda: getattr(USER, 'USERNAME_FIELD', 'username')


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


def send_email(text, to, subject):
    try:
        from sitemessage.toolbox import get_message_type_for_app, schedule_messages, recipients
        message_cls = get_message_type_for_app('sitegate', 'email_plain')
        return schedule_messages(message_cls(subject, text), recipients('smtp', to))
    except ImportError:
        if isinstance(to, USER):
            to = to.email
        return send_mail(subject, text, settings.DEFAULT_FROM_EMAIL, [to])
