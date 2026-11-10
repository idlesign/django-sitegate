"""Contains utility functions used by sitegate."""
from functools import WRAPPER_ASSIGNMENTS
from functools import wraps
from typing import Dict

from django.contrib.auth import get_user_model
from etc.toolbox import import_project_modules

from .settings import APP_MODULE_NAME

_REMOTES_REGISTRY: Dict[str, 'Remote'] = {}
"""Remote services available for sign in through. Indexed by their aliases."""

USER = get_user_model()

get_username_field = lambda: getattr(USER, 'USERNAME_FIELD', 'username')

if False:  # pragma: nocover
    from .signin_flows.remotes.base import Remote  # noqa


def available_attrs(fn):
    return WRAPPER_ASSIGNMENTS


def import_project_sitegate_modules():
    """Imports sitegates modules from registered apps."""
    return import_project_modules(APP_MODULE_NAME)


def register_remotes(*remotes: 'Remote'):
    """Registers (configures) remotes.

    :param remotes: Remote heirs instances.

    """
    global _REMOTES_REGISTRY

    for remote in remotes:
        _REMOTES_REGISTRY[remote.alias] = remote


def get_registered_remotes() -> Dict[str, 'Remote']:
    """Returns registered remotes dict indexed by their aliases."""
    return _REMOTES_REGISTRY


class DecoratorBuilder:
    """Decorators builder. Facilitates decorators creation.
    Inherit from this and implement `handle` method.

    """

    def __init__(self, args, kwargs):
        """Accepts decoration function arguments."""
        self._args_dec = list(args)
        self._kwargs_dec = dict(kwargs)

    def handle(self, func, args_func, kwargs_func, args_dec, kwargs_dec):
        raise NotImplementedError  # pragma: nocover

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
