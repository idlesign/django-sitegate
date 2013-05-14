django-sitegate
===============
http://github.com/idlesign/django-sitegate


What's that
-----------

*django-sitegate is a reusable application for Django to ease sign up processes.*

This application will handle most common user registration flows for you.



Quick example
-------------

Add the **sitegate** application to INSTALLED_APPS in your settings file (usually 'settings.py').

Here follows the most straightforward way possible with ``django-sitegate`` to have a sign up
functionality on your page.


1. Use ``signup_view`` decorator to mark your view as the one handling signups:

    .. code-block:: python

        from django.shortcuts import render

        from sitegate.decorators import signup_view, redirect_signedin

        @signup_view
        @redirect_signedin  # We also prevent logged in users from accessing our sign in/sign up page.
        def login(request):
            return render(request, 'login.html', {'title': 'Login & Sign up'})


2. Then in your template load ``sitegate`` tag library and put ``sitegate_signup_form`` tag in place where you want a registration form to be.

    .. code-block:: html

        {% extends "_base.html" %}
        {% load sitegate %}

        {% block page_contents %}
            <div class="my_signup_block">
                {% sitegate_signup_form %}
            </div>
        {% endblock %}


You're done. Now your site visitors have an e-mail + password form to register.

And mind that we've barely made a scratch of **sitegate**.




Documentation
-------------

http://django-sitegate.readthedocs.org/
