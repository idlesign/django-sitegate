Signup tweaks
=============

Here are some tips and tweaks for **django-sitegate** signup flows.


Sending confirmation email for email-aware signups
--------------------------------------------------

By default email-aware signup flows do not ask a user to verify his email address, to change this behaviour you need
to take some additional steps:

.. note::

    This feature depends upon `django-sitemessage <https://github.com/idlesign/django-sitemessage/>`_.

    Make sure it is installed and configured to use SMTP.


.. note::

    This feature also depends upon Django Messages Contrib. Make sure it is available.


* Either override `verify_email` flow class attribute or provide `verify_email` keyword attribute to `signup_view` decorator:

    .. code-block:: python

        ...
        @signup_view(verify_email=True)
        ...


* Attach **sitegate** urls to urlpatterns of your project (*urls.py*):

    .. code-block:: python

        from sitegate.toolbox import get_sitegate_urls

        urlpatterns = patterns('',
            ...
        )

        urlpatterns += get_sitegate_urls()


* You're done. Upon registration user will be notified he needs to confirm his email address.

    An email with account activation link will be sent by **django-sitemessage**.


.. note::

    Texts (both sent by email and shown on site) could be customized.

    See :ref:`Preferences <email-prefs>` chapter.

