from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SitegateConfig(AppConfig):
    """Sitegate configuration."""

    name: str = 'sitegate'
    verbose_name: str = _('Sign up & Sign in')

    def ready(self):
        from sitegate.utils import import_project_sitegate_modules
        import_project_sitegate_modules()
