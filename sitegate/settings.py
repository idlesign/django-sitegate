from django.conf import settings
from django.utils.translation import ugettext_lazy as _


SIGNIN_ENABLED = getattr(settings, 'SITEGATE_SIGNIN_ENABLED', True)
SIGNIN_DISABLED_TEXT = getattr(settings, 'SITEGATE_SIGNIN_DISABLED_TEXT', _('Sign in is disabled.'))

SIGNUP_ENABLED = getattr(settings, 'SITEGATE_SIGNUP_ENABLED', True)
SIGNUP_DISABLED_TEXT = getattr(settings, 'SITEGATE_SIGNUP_DISABLED_TEXT', _('Sign up is disabled.'))


try:
    from siteprefs.toolbox import patch_locals, register_prefs, pref

    patch_locals()
    register_prefs(
        pref(SIGNIN_ENABLED, verbose_name=_('Signin enabled'), static=False),
        pref(SIGNIN_DISABLED_TEXT, verbose_name=_('Sign in disabled text'), help_text=_('This text is shown instead of a signin form when sign in in disabled.'), static=False),
        pref(SIGNUP_ENABLED, verbose_name=_('Signup enabled'), static=False),
        pref(SIGNUP_DISABLED_TEXT, verbose_name=_('Sign up disabled text'), help_text=_('This text is shown instead of a signup form when sign up in disabled.'), static=False)
    )

except ImportError:
    pass
