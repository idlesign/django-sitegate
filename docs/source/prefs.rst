Preferences
===========

Some of ``django-sitegate`` behavior can be customized using preferences system.

The following sitegate preferences are located in ``sitegate.settings`` module.

.. note::

    ``django-sitegate`` supports changing preferences runtime with the help of ``django-siteprefs`` -

    https://github.com/idlesign/django-siteprefs



SIGNIN_ENABLED
--------------

This indicates whether sigin is enabled. If disabled signin forms won't be rendered.

You can override the default value by defining ``SITEGATE_SIGNIN_ENABLED`` in ``settings.py`` of your project.


SIGNIN_DISABLED_TEXT
--------------------

This text will be rendered instead of a sign in form, if sign in is disabled (see ``SIGNIN_ENABLED``).


SIGNUP_ENABLED
--------------

This indicates whether sig up is enabled. If disabled signup forms won't be rendered.

You can override the default value by defining ``SITEGATE_SIGNUP_ENABLED`` in ``settings.py`` of your project.


SIGNUP_DISABLED_TEXT
--------------------

This text will be rendered instead of a sign up form, if sign up is disabled (see ``SIGNUP_ENABLED``).


.. _email-prefs:


SIGNUP_VERIFY_EMAIL_NOTICE
--------------------------

Text shown to a user after a registration form is submitted.

You can override the default value by defining ``SITEGATE_SIGNUP_VERIFY_EMAIL_NOTICE`` in ``settings.py`` of your project.


SIGNUP_VERIFY_EMAIL_TITLE
-------------------------

Title of a message sent to a user to verify his email address.

You can override the default value by defining ``SITEGATE_SIGNUP_VERIFY_EMAIL_TITLE`` in ``settings.py`` of your project.


SIGNUP_VERIFY_EMAIL_BODY
------------------------

Body (main text) of a message sent to a user to verify his email address.

.. note::

    This **must** include ``%(url)s`` marker, which will be replaced with an account activation URL.

You can override the default value by defining ``SITEGATE_SIGNUP_VERIFY_EMAIL_BODY` in ``settings.py`` of your project.

SIGNUP_VERIFY_EMAIL_CHANGE_foo_TITLE
------------------------------------

``foo`` should be replaced by "START", "CONTINUE" or "FINISH"

Title of a message sent to a old user's email (for ``START``) or to new user's email (for ``CONTINUE``)  to verify email change.
``FINISH`` is used when email confirmation is finished

You can override the default value by defining ``SIGNUP_VERIFY_EMAIL_CHANGE_foo_TITLE`` in ``settings.py`` of your project.


SIGNUP_VERIFY_EMAIL_CHANGE_foo_BODY
-----------------------------------

``foo`` should be replaced by "START", "CONTINUE" or "FINISH"

Body (main text) of a message send for email change confirmation.

.. note::

    This **must** include ``%(url)s`` and ``%(new_email)s`` markers for ``START`` and ``CONTINUE``, which will be replaced with an email change validation URL and new_email. For ``FINISH`` there should be NO markers

You can override the default value by defining ``SIGNUP_VERIFY_EMAIL_CHANGE_START_BODY` in ``settings.py`` of your project.



SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT
--------------------------------

A message shown to a user after he has followed an account activation URL if activation was a success.

You can override the default value by defining ``SITEGATE_SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT`` in ``settings.py`` of your project.


SIGNUP_VERIFY_EMAIL_ERROR_TEXT
------------------------------

A message shown to a user after he has followed an account activation URL if there was an error during an activation process.

You can override the default value by defining ``SITEGATE_SIGNUP_VERIFY_EMAIL_ERROR_TEXT`` in ``settings.py`` of your project.

SIGNUP_VERIFY_EMAIL_USE_GENERIC_CONFIRMATION
--------------------------------------------

If this is set to ``True`` then default viewname for email confirmation will be ``"generic_confirmation"`` instead of ``"verify_email"``.

SIGNUP_VERIFY_EMAIL_VIEW_NAME
-----------------------------

Name of view that processes email verification. If you are using ``sitegate.toolbox.get_sitegate_urls`` in your root urlconf then default value will be fine for you. If you are using it under some namespace or if you are using your own urlpattern and want to use ``@signup_view(verify_email=True)`` or are using customized classic signup flow with ``verify_email = True`` then you should
specify some meaningful viewname to ``sitegate.views.verify_email`` or ``sitegate.views.generic_confirmation`` (read about ``SIGNUP_VERIFY_EMAIL_USE_GENERIC_CONFIRMATION`` to know which one to choose).

Default value: ``"verify_email"`` or ``"generic_confirmation"`` depending on ``SIGNUP_VERIFY_EMAIL_USE_GENERIC_CONFIRMATION`` setting

SIGNUP_GENERIC_CONFIRMATION_VIEW_NAME
-------------------------------------

Just like ``SIGNUP_VERIFY_EMAIL_VIEW_NAME`` but for view ``sitegate.views.generic_confirmation``


SIGNUP_VERIFY_EMAIL_GENERIC_VIEW_DOMAIN_ARG
-----------------------------------------

When ``"generic_confirmation"`` is used to confirm user emails (read about
``SIGNUP_VERIFY_EMAIL_USE_GENERIC_CONFIRMATION`` and ``SIGNUP_VERIFY_EMAIL_VIEW_NAME`` for details)
then it's ``confirmation_domain`` argument can be changed by this setting.

SIGNUP_EMAIL_CHANGE_PROCESSING
------------------------------

When this setting is set to ``True`` then signal ``sitegate.signal_receivers.process_email_change`` receiver will be connected to
``sig_generic_confirmation_received`` signal to handle data that is fired by visiting urls that
were previously generated by visiting url returned by ``EmailConfirmation.start_email_change``, 
``EmailConfirmation.continue_email_change``.

Example workflow:
1. Active user wants to change email from ``user.email`` to ``new_email``
2. Your view calls ``EmailConfirmation.start_email_change(user, new_email, strict=True, send_email=True, request=request)`` which
   will send email with secret url to his current email address (when ``SIGNUP_EMAIL_CHANGE_TWO_STEPS == True``)
   or to his ``new_email`` (when ``SIGNUP_EMAIL_CHANGE_TWO_STEPS == False``).
3. user visits url from step 2. ``process_email_change`` processes this event and calls ``EmailConfirmation.continue_email_change(prev_code, secret_data, send_email=True, request=request)``
   or ``EmailConfirmation.finish_email_change(prev_code, secret_data, send_email=True, request=request)`` (depending on ``SIGNUP_EMAIL_CHANGE_TWO_STEPS``)
   that will send another email to ``new_email`` address with another secret url or will just change his current email to ``new_email``.

4. when ``SIGNUP_EMAIL_CHANGE_TWO_STEPS == True`` and user visits url from step 3 this will run ``EmailConfirmation.finish_email_change(user, secret_data, send_email=True, request=request)``


SIGNUP_EMAIL_CHANGE_TWO_STEPS
-----------------------------

When set to True then signal receivers activated by ``SIGNUP_EMAIL_CHANGE_PROCESSING``
will require confirmation from old url. When set to ``False`` then only confirmation from new
address will be required.

Default value: ``False``
