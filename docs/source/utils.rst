Utilities
=========

**django-sitegate** provides some utility functions for your pleasure.



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
