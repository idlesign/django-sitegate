Customizing sign in
===================

**django-sitegate** by default uses a simple username/e-mail + password form. Although it is a rather common use case, inevitably
there should come times, when such a sign in form is not suitable. Should it be only just styling, or entire form
that you want to change, or provide several sign in options **sitegate** has some answers for you.

Further we'll consider a number of approaches to sign in customization. But just before we start, let's talk about sign in flows.



Sign in flows
-------------

**sitegate** uses the notion of ``sign in flows`` to describe sign in processes.

Besides some sign in logic each flow features a form which is used for signing in and a template to render that form.

And, of course, every sign in flow has its own **name**, so that we can address them and use at our will like so:

.. code-block:: python

    from django.shortcuts import render

    # Import a flow class to use.
    from sitegate.signin_flows.classic import ClassicSignin
    from sitegate.decorators import signin_view

    # And use that class for sign in.
    @signin_view(flow=ClassicSignin)
    def login(request):
        return render(request, 'login.html', {'title': 'Sign in'})


Hopefully you've already noticed this code is a spin off from *Getting Started* section. Not much have changed since,
though now we have a classical Django log in form (username + password) instead of a modern one.

The above example should give you an idea of how sign in flows can differ from each other.



Built-in sign in flows
----------------------

Sign in flow classes are places in ``sitegate.signin_flows`` module.

These are the options:


* Modern flows - ``sitegate.signin_flows.modern``


    * **ModernSignin**

        Modernized sign in flow based on classic from Django built-in with username/e-mail authentication support.

        *Default form:* username/e-mail + password

        .. note::

            This sign in flow is the default one. It means that it will be used if you decorate your view with ``@signin_view``
            decorator both without any parameters, or without ``flow`` parameter.


* Classic flows - ``sitegate.signin_flows.classic``


    * **ClassicSignin**

        Classic log in flow borrowed from Django built-in AuthenticationForm.

        *Default form:* username + password



Combining sign in flows
-----------------------

You can use more than one sign in flow with the same view, by stacking ``@signin_view`` decorators:

.. code-block:: python

    from django.shortcuts import render

    from sitegate.signin_flows.classic import ClassicSignin
    from sitegate.decorators import signup_view

    # We'll use some our mythical MySignin flow, so let's import it.
    from .my_signin_flows import MySignin

    # Stack our decorators.
    @signin_view(flow=MySignin)
    @signin_view(flow=ClassicSignin)
    def login(request):
        return render(request, 'login.html', {'title': 'Sign in'})


Additionally you'll need to extend your template. Let's extend the one from *Getting started* section:

.. code-block:: html

    {% extends "_base.html" %}
    {% load sitegate %}

    {% block page_contents %}
        <div class="my_signin_block one">
            {% sitegate_signin_form for ClassicSignin %}
        </div>
        <div class="my_signin_block two">
            {% sitegate_signin_form for MySignin %}
        </div>
    {% endblock %}


Now your users might use either of two log in methods.



Form templates
--------------

**sitegate** uses templates to render forms bound to sign in flows, and is shipped with several of them for your convenience.

Sign in form templates are stored under ``sitegate/templates/sitegate/signin/``. Feel free to examine them in need.

The following templates are shipped with the application:

* **form_as_p.html** - This  contents identical to that produced by *form.as_p*.

    .. note::

        This is the **default template**. It means that it will be used if you decorate your view with ``@signin_view``
        decorator both without ``template`` parameter given.


* **form_bootstrap.html** - This template produces HTML ready to use with Twitter Bootstrap Framework.

* **form_bootstrap3.html** - This template produces HTML ready to use with Bootstrap Framework version 3.

    .. note::

        This also requires `form-control` class to be batch applied for every form widget for proper form fields styling.

        See `Batch styling form widgets` section below.

        E.g: widget_attrs={'class': 'form-control'}


* **form_foundation.html** - This template produces HTML ready to use with Foundation Framework.



Swapping form templates
-----------------------

If the built-in templates is not what you want, you can swap them for your own:

.. code-block:: python

    from django.shortcuts import render

    from sitegate.decorators import signin_view

    # I command: use my template. Its name is `my_sign_in_form.html` %)
    @signin_view(template='my_sign_in_form.html')
    def login(request):
        return render(request, 'login.html', {'title': 'Sign in'})


.. note::

    You can address the built-in templates both by providing a full path and with a shortcut -
    *filename without an extension*.

    For example: ``sitegate/signin/form_bootstrap.html`` and ``form_bootstrap`` are interchangeable.


And that's all what you need to tell **sitegate** to use your custom template.



Batch styling form widgets
--------------------------

Now if the only thing that makes you uncomfortable with sign in is that form widgets (e.g. text inputs) lack
styling and, say, it is required by some CSS framework you use, **sitegate** will help you to handle it.

Use ``widget_attrs`` parameter for ``@signin_view`` decorator to accomplish the task:

.. code-block:: python

    from django.shortcuts import render

    from sitegate.decorators import signin_view

    # Let's use the built-in template for Twitter Bootstrap
    # and align widgets to span6 column,
    # and use field label as a placeholder, that will be rendered by Bootstrap as a hint inside text inputs.
    @signin_view(widget_attrs={'class': 'span6', 'placeholder': lambda f: f.label}, template='form_bootstrap')
    def login(request):
        return render(request, 'login.html', {'title': 'Sign in'})

The most interesting thing here is probably *lambda*. It receives field instance, so you can customize widget attribute
values in accordance with some field data.



Sign in signals
---------------

You can listen to Django built-in signals from ``django.contrib.auth.signals`` (**user_logged_in** and **user_login_failed**), and do some stuff when they are happen

See DjangoAuth contrib documentation for more information.
