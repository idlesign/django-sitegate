Getting started
===============

* Add the **sitegate** application to INSTALLED_APPS in your settings file (usually ``settings.py``).
* Apply DB migrations (``manage.py migrate``).


Quick example
-------------

Here follows the most straightforward way possible with ``django-sitegate`` to have both sign up & sign in
functionality on your page.


1. Use ``sitegate_view`` decorator to mark your view as the one handling both signups and signins:

    .. code-block:: python

        from django.shortcuts import render

        from sitegate.toolbox import sitegate_view

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

Sign in using remotes
---------------------

You can configure **sitegate** to allow users to log in with remote services, like ``Yandex`` and ``Google``.

1. Put ``sitegates.py`` file in one of your applications:

.. code-block:: python

    from sitegate.signin_flows.remotes.google import Google
    from sitegate.signin_flows.remotes.yandex import Yandex
    from sitegate.toolbox import register_remotes

    # We register our remotes.
    register_remotes(
        # Register OAuth clients (web application type) beforehand

        # https://oauth.yandex.ru/client/new
        # set <your-domain-uri>/rauth/yandex/ as a Callback URL
        Yandex(client_id='<your-client-id-here>'),

        # https://console.cloud.google.com/apis/credentials/oauthclient
        # set <your-domain-uri>/rauth/google/ as a Callback URL
        Google(client_id='<your-client-id-here>'),
    )

2. Attach sitegate URL patterns in your ``urls.py``:

    .. code-block:: python

        from sitegate.toolbox import get_sitegate_urls

        urlpatterns = patterns('',
            ...  # your urls here
        )

        # attach sitegate urls
        urlpatterns += get_sitegate_urls()


After that your users should see links to proceed using remote auth.
Those links are placed just below your Sign In form.

And mind that we've barely made a scratch of **sitegate**.
