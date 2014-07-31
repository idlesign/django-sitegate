from django.conf import settings
from django.utils.translation import ugettext_lazy as _


SIGNIN_ENABLED = getattr(settings, 'SITEGATE_SIGNIN_ENABLED', True)
SIGNIN_DISABLED_TEXT = getattr(settings, 'SITEGATE_SIGNIN_DISABLED_TEXT', _('Sign in is disabled.'))

SIGNUP_ENABLED = getattr(settings, 'SITEGATE_SIGNUP_ENABLED', True)
SIGNUP_DISABLED_TEXT = getattr(settings, 'SITEGATE_SIGNUP_DISABLED_TEXT', _('Sign up is disabled.'))

SIGNUP_VERIFY_EMAIL_NOTICE = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_NOTICE', _('Congratulations! You\'re almost done with the registration. Please check your mailbox for a message containing an account activation link.'))

SIGNUP_VERIFY_EMAIL_TITLE = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_TITLE', _('Account activation'))
SIGNUP_VERIFY_EMAIL_BODY = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_BODY', _('Please follow the link below to activate your account:\n%(url)s'))

SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT', _('E-mail was successfully verified. You can now proceed to sign in.'))
SIGNUP_VERIFY_EMAIL_ERROR_TEXT = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_ERROR_TEXT', _('Unable to verify an e-mail. User account was not activated.'))

SIGNUP_VERIFY_EMAIL_VIEW_NAME = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_VIEW_NAME', 'verify_email')

try:
    from siteprefs.toolbox import patch_locals, register_prefs, pref, pref_group
    from django.db.models import CharField

    patch_locals()
    register_prefs(
        pref(SIGNIN_ENABLED, verbose_name=_('Signin enabled'), static=False),
        pref(SIGNIN_DISABLED_TEXT, verbose_name=_('Sign in disabled text'), help_text=_('This text is shown instead of a signin form when sign in in disabled.'), static=False),
        pref(SIGNUP_ENABLED, verbose_name=_('Signup enabled'), static=False),
        pref(SIGNUP_DISABLED_TEXT, verbose_name=_('Sign up disabled text'), help_text=_('This text is shown instead of a signup form when sign up in disabled.'), static=False),

        pref_group(_('E-mail verification'), (
            pref(SIGNUP_VERIFY_EMAIL_NOTICE, verbose_name=_('Verification notice'), help_text=_('Text shown to a user after a registration form is submitted.'), static=False),

            pref(SIGNUP_VERIFY_EMAIL_TITLE, verbose_name=_('Message title'), help_text=_('Title of an email message containing an account activation URL.'), static=False, field=CharField(max_length=160)),
            pref(SIGNUP_VERIFY_EMAIL_BODY, verbose_name=_('Message body'), help_text=_('<b>NOTE:</b> Message body must include `%(url)s` marker to indicate a place to put an activation URL at.'), static=False),

            pref(SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT, verbose_name=_('Verification success notice'), help_text=_('A message shown to a user after he has followed an account activation URL if activation was a success.'), static=False),
            pref(SIGNUP_VERIFY_EMAIL_ERROR_TEXT, verbose_name=_('Verification error notice'), help_text=_('A message shown to a user after he has followed an account activation URL if there was an error during an activation process.'), static=False),
        ))
    )

except ImportError:
    pass
