# Preferences

Some of `django-sitegate` behavior can be customized using preferences system.

The following sitegate preferences are located in `sitegate.settings` module.
Override the defaults by defining the corresponding `SITEGATE_*` setting in `settings.py` of your project.

!!! note

    `django-sitegate` supports changing preferences runtime with the help of `django-siteprefs` —

    <https://github.com/idlesign/django-siteprefs>

## SIGNIN_ENABLED

This indicates whether sign in is enabled. If disabled sign in forms won't be rendered.

## SIGNIN_DISABLED_TEXT

This text will be rendered instead of a sign in form, if sign in is disabled (see `SIGNIN_ENABLED`).

## SIGNUP_ENABLED

This indicates whether sign up is enabled. If disabled sign up forms won't be rendered.

## SIGNUP_DISABLED_TEXT

This text will be rendered instead of a sign up form, if sign up is disabled (see `SIGNUP_ENABLED`).

## SIGNUP_VERIFY_EMAIL_NOTICE

Text shown to a user after a registration form is submitted.

## SIGNUP_VERIFY_EMAIL_TITLE

Title of a message sent to a user to verify his email address.

## SIGNUP_VERIFY_EMAIL_BODY

Body (main text) of a message sent to a user to verify his email address.

!!! note

    This **must** include `%(url)s` marker, which will be replaced with an account activation URL.

## SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT

A message shown to a user after he has followed an account activation URL if activation was a success.

## SIGNUP_VERIFY_EMAIL_ERROR_TEXT

A message shown to a user after he has followed an account activation URL if there was an error during an activation process.

## APP_MODULE_NAME

Name of the module sitegate searches project applications for, to import it automatically.
Useful for registering remotes and custom preferences. Defaults to `sitegates`.

## Other settings

`SITEGATE_USE_SITEMESSAGE` and `SITEGATE_USE_SITEPREFS` enable integration with `django-sitemessage`
and `django-siteprefs` respectively. Both are enabled automatically when the corresponding package
is present in `INSTALLED_APPS`.
