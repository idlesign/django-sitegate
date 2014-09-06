from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class SitegateConfig(AppConfig):
    """Sitegate configuration."""

    name = 'sitegate'
    verbose_name = _('Sign up & Sign in')
