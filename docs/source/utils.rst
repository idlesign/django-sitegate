Utilities
=========

**django-sitegate** provides some utility functions for your pleasure.


@sitegate_view
--------------

This decorator is a shortcut comprising three basic decorators:

* @signin_view
* @signup_view
* @redirect_signedin


This decorator can accept the same keyword arguments as ``@signin_view`` and ``@signup_view``:

.. code-block:: python

    from django.shortcuts import render

    from sitegate.decorators import sitegate_view

    # Let's use Twitter Bootstrap template, and style both sign in & sign up form accordingly.
    @sitegate_view(widget_attrs={'class': 'span6', 'placeholder': lambda f: f.label}, template='form_bootstrap')
    def entrance(request):
        return render(request, 'entrance.html', {'title': 'Sign in & Sign up'})



@redirect_signedin
------------------

**sitegate** knowns that in most cases you don't want users to access sign in and sign up pages after they are logged in,
so it gives you ``@redirect_signedin`` decorator for your views:


.. note::

    This decorator redirects logged in users to another location, when they try to access the page.

    **Default redirect URL** is a site root - **/**


.. code-block:: python

        from django.shortcuts import render

        from sitegate.decorators import redirect_signedin

        @redirect_signedin  # Let's prevent logged in users from accessing our sign in page.
        def login(request):
            return render(request, 'login.html', {'title': 'Login'})


The decorator accepts the same parameters as ``redirect`` from ``django.shortcuts``.

It means that you can instruct it where logged in users should be redirected to:

.. code-block:: python

        @redirect_signedin('/some/url/for/those/already/logged/in/')
        def login(request):
            return render(request, 'login.html', {'title': 'Login'})


USER
----

Django 1.5 introduces custom user model support. To be compatible with that, **sitegate** is equipped
with **USER** variable which resides in ``sitegate.utils``. It will always address the appropriate User model,
so that you can use it in your sign up and sign in flows and forms.

.. warning::

    Please note, that **sitegate** with its' build-in sign in/up flows relies on the fact that User model
    has some basic attributes: *username*, *email*, *password*, *is_active*, *set_password*.


confirm email change
--------------------

.. versionadded:: 0.10.3

In your project you can use ``EmailConfirmation`` model to perform 1 or 2-step confirmation of email
changes. One-step confirmation (default) only sends email to new email address. Two-step confirmation
sends email to old address and after visiting url in this email it then send email to new address. To enable this validation:

1. set ``SIGNUP_EMAIL_CHANGE_PROCESSING`` in your settings.py to True
2. set ``SIGNUP_EMAIL_CHANGE_TWO_STEPS`` to ``True`` if you'd like to have 2 step confirmation
   or ``False`` for 1 step confirmation
3. in ``form.clean()`` of form where use changes email:
   
   .. code-block:: python

   		new_email = self.cleaned_data['email']
        self.cleaned_data['email'] = self.instance.email  # do not change email just yet.

        EmailConfirmation.start_email_change(self.instance, new_email=new_email, send_email=True, request=request)
        # note that you should pass request object ot form.clean(). For example: this may be done
        by overriding form.__init__ method to accept request argument and sotre it as self.request

If you do not like default email messages or you'd like to make any operations over confirmation url somewhere in your url:

.. code-block:: python

   url = EmailConfirmation.start_email_change(self.instance, new_email=new_email, send_email=False)
   url_with_domain = request.build_absolute_uri(url)
   some_processing(url_with_domain)

You may also force ``EmailConfirmation.start_email_change`` to ignore ``SIGNUP_EMAIL_CHANGE_PROCESSING``
setting by setting ``next_step`` argument to ``"continue_email_change"`` or ``"finish_email_change"``

generic confirmations
---------------------

email change confirmations are based on ``generic_confirmation`` view.

You can generate url for any ``EmailConfirmation`` instance with arbitrary confirmation_domain and data:

.. code-block:: python

        code = EmailConfirmation.add(some_user)
        url = code.confirmation_url_for_data('some-confirmation-domain', data_dict)
        url_with_domain = request.build_absolute_uri(url)

To process visits to this url you can connect some function to ``sig_generic_confirmation_received`` signal:

.. code-block:: python

		from django.dispatch import receiver

		from .signals import sig_generic_confirmation_received

		@receiver(sig_generic_confirmation_received)
		def some_receiver(sender, confirmation_domain, code, decrypted_data, request, *args, **kwargs):
			if confirmation_domain == 'some-confirmation-domain':
				# process decrypted_data which is the same as data_dict used to generate url
				# code is the same instance of EmailConfirmation that was used to generate url
				pass