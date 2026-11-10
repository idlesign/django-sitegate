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



SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT
--------------------------------

A message shown to a user after he has followed an account activation URL if activation was a success.

You can override the default value by defining ``SITEGATE_SIGNUP_VERIFY_EMAIL_SUCCESS_TEXT`` in ``settings.py`` of your project.


SIGNUP_VERIFY_EMAIL_ERROR_TEXT
------------------------------

A message shown to a user after he has followed an account activation URL if there was an error during an activation process.

You can override the default value by defining ``SITEGATE_SIGNUP_VERIFY_EMAIL_ERROR_TEXT`` in ``settings.py`` of your project.
