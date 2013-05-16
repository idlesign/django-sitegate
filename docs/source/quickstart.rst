Getting started
===============

Add the **sitegate** application to INSTALLED_APPS in your settings file (usually 'settings.py').


Quick example
-------------

Here follows the most straightforward way possible with ``django-sitegate`` to have both sign up & sign in
functionality on your page.


1. Use ``signup_view`` and ``signin_view`` decorators to mark your view as the one handling signups and sign ins respectively:

    .. code-block:: python

        from django.shortcuts import render

        from sitegate.decorators import signup_view, signin_view, redirect_signedin

        @signup_view
        @signin_view
        @redirect_signedin  # We also prevent logged in users from accessing our sign in/sign up page.
        def entrance(request):
            return render(request, 'entrance.html', {'title': 'Sign in & Sign up'})


2. Then in your template load ``sitegate`` tag library and put ``sitegate_signup_form`` & ``sitegate_signin_form`` tags
in place where you want a registration and sign in forms to be.

    .. code-block:: html

        {% extends "_base.html" %}
        {% load sitegate %}

        {% block page_contents %}
            <div class="my_signin_block">
                {% sitegate_signin_form %}
            </div>
            <div class="my_signup_block">
                {% sitegate_signup_form %}
            </div>
        {% endblock %}


You're done. Now your site visitors have an e-mail + password form to register and username/e-mail + password form to log in.

And mind that we've barely made a scratch of **sitegate**.
