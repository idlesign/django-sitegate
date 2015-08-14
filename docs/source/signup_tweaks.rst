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

    An email with account activation link will be sent by **django-sitemessage** or by **django.core.mail.send_mail** when django-sitemessage is not available


.. note::

    Texts (both sent by email and shown on site) could be customized.

    See :ref:`Preferences <email-prefs>` chapter.



Sending confirmation email for changed emails
---------------------------------------------

View for email confirmation can also be used to confirm email changes. Django-sitegate does not provide
means to actually initiate email change so it's up to you to actually validate new emails, to generate required ``EmailConfirmation`` instance, tpgenerate activation url, to send email with url.

Example of generating url for included confirmation view:

.. code-block:: python

    from sitegate.models import EmailConfirmation
    from sitegate.settings import SIGNUP_VERIFY_EMAIL_VIEW_NAME
    from django.contrib.auth import get_user_model

    some_user = get_user_model().objects.all().first()
    code = EmailConfirmation.add(user=some_user, new_email='other_email@domain.com')

    email_confirmation_url = request.build_absolute_uri(reverse(SIGNUP_VERIFY_EMAIL_VIEW_NAME, args=(code.code,)))

    # now you can generate some email with this url and sendit to new email of user.


.. warning::

   This approach does not send anything to old email! It only ensures that new email is valid.
   So if someone will gain access to authorised user session on site then he or she will be able to change
   email without access to old mailbox.


If **settings.SIGNUP_VERIFY_EMAIL_ALLOW_DUPLICATES** is ``False`` (the default) then confirmation view will fail
if user tries to change email to email of exising user. But it's better to perform this check in your email change form.
Current confirmation view provides same messages for registration confirmation and email change confirmation. You can create your own confirmation view, example:

.. code-block:: python

	def custom_verify_email(request, code, redirect_to=None):
	    success = False

	    valid_code = EmailConfirmation.is_valid(code)
	    if valid_code and valid_code.user.is_active:  # also verify that user is already activated
	        valid_code.activate()
	        success = True

	    if success:
	        messages.success(request, _("Change of email confirmed"), 'success')
	    else:
	        messages.error(request, SIGNUP_VERIFY_EMAIL_ERROR_TEXT, 'danger error')

	    if redirect_to is None:
	        redirect_to = '/'

	    return redirect(redirect_to)
