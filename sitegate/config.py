from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SitegateConfig(AppConfig):
    """Sitegate configuration."""

    name: str = 'sitegate'
    verbose_name: str = _('Sign up & Sign in')
