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
