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
