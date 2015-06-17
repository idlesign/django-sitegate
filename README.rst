django-sitegate
===============
http://github.com/idlesign/django-sitegate

.. image:: https://img.shields.io/pypi/v/django-sitegate.svg
    :target: https://pypi.python.org/pypi/django-sitegate

.. image:: https://img.shields.io/pypi/dm/django-sitegate.svg
    :target: https://pypi.python.org/pypi/django-sitegate

.. image:: https://img.shields.io/pypi/l/django-sitegate.svg
    :target: https://pypi.python.org/pypi/django-sitegate

.. image:: https://img.shields.io/coveralls/idlesign/django-sitegate/master.svg
    :target: https://coveralls.io/r/idlesign/django-sitegate

.. image:: https://img.shields.io/travis/idlesign/django-sitegate/master.svg
    :target: https://travis-ci.org/idlesign/django-sitegate

.. image:: https://img.shields.io/codeclimate/github/idlesign/django-sitegate.svg
   :target: https://codeclimate.com/github/idlesign/django-sitegate


What's that
-----------

*django-sitegate is a reusable application for Django to ease sign up & sign in processes.*

This application will handle most common user registration and log in flows for you.

**Sign in**

* username/e-mail + password
* username + password

**Sign up**

* username/e-mail + password
* invitation code + username/e-mail + password
* username + password
* username + e-mail + password
* username + password + password confirmation
* username + e-mail + password + password confirmation


Quick example
-------------

* Add the **sitegate** application to INSTALLED_APPS in your settings file (usually 'settings.py').
* Make sure `TEMPLATE_CONTEXT_PROCESSORS` in your settings file has `django.core.context_processors.request`.

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



Documentation
-------------

http://django-sitegate.readthedocs.org/
