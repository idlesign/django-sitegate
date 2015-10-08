from django.conf import settings
from django.utils.translation import ugettext_lazy as _


SIGNIN_ENABLED = getattr(settings, 'SITEGATE_SIGNIN_ENABLED', True)
SIGNIN_DISABLED_TEXT = getattr(settings, 'SITEGATE_SIGNIN_DISABLED_TEXT', _('Sign in is disabled.'))

SIGNUP_ENABLED = getattr(settings, 'SITEGATE_SIGNUP_ENABLED', True)
SIGNUP_DISABLED_TEXT = getattr(settings, 'SITEGATE_SIGNUP_DISABLED_TEXT', _('Sign up is disabled.'))

SIGNUP_VERIFY_EMAIL_NOTICE = getattr(
    settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_NOTICE',
    _('Congratulations! You\'re almost done with the registration. Please check your mailbox '
      'for a message containing an account activation link.'))

SIGNUP_VERIFY_EMAIL_TITLE = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_TITLE', _('Account activation'))
SIGNUP_VERIFY_EMAIL_BODY = getattr(
    settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_BODY',
    _('Please follow the link below to activate your account:\n%(url)s'))

SIGNUP_VERIFY_EMAIL_CHANGE_START_TITLE = getattr(settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_START_TITLE', _('Email change confirmation'))
SIGNUP_VERIFY_EMAIL_CHANGE_START_BODY = getattr(
    settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_START_BODY',
    _('Please follow the link below to confirm that you are changing email from this email to %(new_email)s:\n%(url)s'))
SIGNUP_VERIFY_EMAIL_CHANGE_START_NOTICE = getattr(
    settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_START_NOTICE',
    _('To continue email change please check your current mailbox for a message containing confirmation link.'))

SIGNUP_EMAIL_CHANGE_TWO_STEPS = getattr(settings, 'SIGNUP_EMAIL_CHANGE_TWO_STEPS', False)

SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_TITLE = getattr(settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_TITLE', _('Email change confirmation'))
SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_BODY = getattr(
    settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_BODY',
    _('Please follow the link below to confirm that you are changing email to %(new_email)s:\n%(url)s'))
SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_NOTICE = getattr(
    settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_NOTICE',
    _('To finish email change please check your new mailbox for a message containing confirmation link.'))

SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_TITLE = getattr(settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_TITLE', _('Email change confirmed'))
SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_BODY = getattr(
    settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_BODY',
    _('Your email have been changed to %(new_email)s'))
SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_NOTICE = getattr(
    settings, 'SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_NOTICE',
    _('Change of your email have been confirmed.'))

SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT = getattr(
    settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT',
    _('E-mail was successfully verified. You can now proceed to sign in.'))
SIGNUP_VERIFY_EMAIL_ERROR_TEXT = getattr(
    settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_ERROR_TEXT',
    _('Unable to verify an e-mail. User account was not activated.'))

SIGNUP_VERIFY_EMAIL_USE_GENERIC_CONFIRMATION = getattr(settings, 'SIGNUP_VERIFY_EMAIL_USE_GENERIC_CONFIRMATION', False)
SIGNUP_VERIFY_EMAIL_VIEW_NAME = getattr(settings, 'SITEGATE_SIGNUP_VERIFY_EMAIL_VIEW_NAME', SIGNUP_VERIFY_EMAIL_USE_GENERIC_CONFIRMATION and 'generic_confirmation' or 'verify_email')
SIGNUP_GENERIC_CONFIRMATION_VIEW_NAME = getattr(settings, 'SIGNUP_GENERIC_CONFIRMATION_VIEW_NAME', 'generic_confirmation')
SIGNUP_VERIFY_EMAIL_GENERIC_VIEW_DOMAIN_ARG = getattr(settings, 'SIGNUP_VERIFY_EMAIL_GENERIC_VIEW_DOMAIN_ARG', 'email')
SIGNUP_EMAIL_CHANGE_PROCESSING = getattr(settings, 'SIGNUP_EMAIL_CHANGE_PROCESSING', False)


try:
    from siteprefs.toolbox import patch_locals, register_prefs, pref, pref_group
    from django.db.models import CharField

    patch_locals()
    register_prefs(
        pref(SIGNIN_ENABLED, verbose_name=_('Signin enabled'), static=False),
        pref(SIGNIN_DISABLED_TEXT, verbose_name=_('Sign in disabled text'),
             help_text=_('This text is shown instead of a signin form when sign in in disabled.'), static=False),
        pref(SIGNUP_ENABLED, verbose_name=_('Signup enabled'), static=False),
        pref(SIGNUP_DISABLED_TEXT, verbose_name=_('Sign up disabled text'),
             help_text=_('This text is shown instead of a signup form when sign up in disabled.'), static=False),

        pref_group(_('E-mail verification'), (
            pref(SIGNUP_VERIFY_EMAIL_NOTICE, verbose_name=_('Verification notice'),
                 help_text=_('Text shown to a user after a registration form is submitted.'), static=False),

            pref(SIGNUP_VERIFY_EMAIL_TITLE, verbose_name=_('Message title'),
                 help_text=_('Title of an email message containing an account activation URL.'),
                 static=False, field=CharField(max_length=160)),
            pref(SIGNUP_VERIFY_EMAIL_BODY, verbose_name=_('Message body'),
                 help_text=_('<b>NOTE:</b> Message body must include `%(url)s` marker to indicate a place '
                             'to put an activation URL at.'), static=False),

            pref(SIGNUP_VERIFY_EMAIL_CHANGE_START_TITLE, verbose_name=_('Confirm old email message title'),
                 help_text=_('Title of an email message to old address for mailchange verification'),
                 static=False, field=CharField(max_length=160)),
            pref(SIGNUP_VERIFY_EMAIL_CHANGE_START_BODY, verbose_name=_('Confirm old email message body'),
                 help_text=_('<b>NOTE:</b> Message body of an email message to old address for mailchange '
                             'verification. Must include `%(url)s` and `%(new_email)s` markers.'), static=False),
            pref(SIGNUP_VERIFY_EMAIL_CHANGE_START_NOTICE, verbose_name=_('Emailchange start notice'),
                 help_text=_('Text shown to a user after 2-step email change verification started'),
                 static=False, field=CharField(max_length=160)),

            pref(SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_TITLE, verbose_name=_('Confirm new email message title'),
                 help_text=_('Title of an email message to new address for mailchange verification'),
                 static=False, field=CharField(max_length=160)),
            pref(SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_BODY, verbose_name=_('Confirm new email message body'),
                 help_text=_('<b>NOTE:</b> Message body of an email message to new address for mailchange '
                             'verification. Must include `%(url)s` and `%(new_email)s` markers.'), static=False),
            pref(SIGNUP_VERIFY_EMAIL_CHANGE_CONTINUE_NOTICE, verbose_name=_('Emailchange continue notice'),
                 help_text=_('Text shown to a user when final message to confirm email was sended'),
                 static=False, field=CharField(max_length=160)),

            pref(SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_TITLE, verbose_name=_('Confirmed new email message title'),
                 help_text=_('Title of an email message to new address for mailchange verification finish'),
                 static=False, field=CharField(max_length=160)),
            pref(SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_BODY, verbose_name=_('Confirmed new email message body'),
                 help_text=_('<b>NOTE:</b> Message body of an email message to new address for mailchange '
                             'verification finish. Must include `%(new_email)s` marker.'), static=False),
            pref(SIGNUP_VERIFY_EMAIL_CHANGE_FINISH_NOTICE, verbose_name=_('Emailchange finish notice'),
                 help_text=_('Text shown to a user when email change was confirmed'),
                 static=False, field=CharField(max_length=160)),

            pref(SIGNUP_VERIFY_EMAIL_TITLE, verbose_name=_('Message title'),
                 help_text=_('Title of an email message containing an account activation URL.'),
                 static=False, field=CharField(max_length=160)),
            pref(SIGNUP_VERIFY_EMAIL_BODY, verbose_name=_('Message body'),
                 help_text=_('<b>NOTE:</b> Message body must include `%(url)s` marker to indicate a place '
                             'to put an activation URL at.'), static=False),

            pref(SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT, verbose_name=_('Verification success notice'),
                 help_text=_('A message shown to a user after he has followed an account activation URL '
                             'if activation was a success.'), static=False),
            pref(SIGNUP_VERIFY_EMAIL_ERROR_TEXT, verbose_name=_('Verification error notice'),
                 help_text=_('A message shown to a user after he has followed an account activation URL '
                             'if there was an error during an activation process.'), static=False),
        ))
    )

except ImportError:
    pass
