from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from .signal_receivers import process_email_change
from .signals import sig_generic_confirmation_received
from .settings import SIGNUP_EMAIL_CHANGE_PROCESSING


class SitegateConfig(AppConfig):

    """Sitegate configuration."""

    name = 'sitegate'
    verbose_name = _('Sign up & Sign in')

    def ready(self):
        if SIGNUP_EMAIL_CHANGE_PROCESSING:
            sig_generic_confirmation_received.connect(process_email_change)
