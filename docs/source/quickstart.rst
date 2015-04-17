Getting started
===============

* Add the **sitegate** application to INSTALLED_APPS in your settings file (usually 'settings.py').
* Make sure `TEMPLATE_CONTEXT_PROCESSORS` in your settings file has `django.core.context_processors.request`.
  For Django 1.8+: `django.template.context_processors.request` should be defined in ``TEMPLATES/OPTIONS/context_processors``.

.. warning::

    If you are using a version Django < 1.7 AND are using a version of South < 1.0, add this to your settings:

    .. code-block:: python

        SOUTH_MIGRATION_MODULES = {
            'sitegate': 'sitegate.south_migrations',
        }



Quick example
-------------

Here follows the most straightforward way possible with ``django-sitegate`` to have both sign up & sign in
functionality on your page.


1. Use ``sitegate_view`` decorator to mark your view as the one handling both signups and signins:

    .. code-block:: python

        from django.shortcuts import render

        from sitegate.decorators import sitegate_view

        @sitegate_view  # This also prevents logged in users from accessing our sign in/sign up page.
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
