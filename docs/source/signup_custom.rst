Customizing signups
===================

**django-sitegate** by default uses a simple e-mail + password form. Although it is a rather common use case, inevitably
there should come times, when such a registration form is not suitable. Should it be only just styling, or entire form
that you want to change, or provide several registration options **sitegate** has some answers for you.

Further we'll consider a number of approaches to signup customization. But just before we start, let's talk about signup flows.



Signup flows
------------

**sitegate** uses the notion of ``signup flows`` to describe signup processes.

Besides some signup logic each flow features a form which is used for registration and a template to render that form.

And, of course, every signup flow has its own **name**, so that we can address them and use at our will like so:

.. code-block:: python

    from django.shortcuts import render

    # Import a flow class to use.
    from sitegate.signup_flows.classic import ClassicSignup
    from sitegate.decorators import signup_view

    # And use that class for registration.
    @signup_view(flow=ClassicSignup)
    def login(request):
        return render(request, 'login.html', {'title': 'Login & Sign up'})


Hopefully you've already noticed this code is a spin off from *Getting Started* section. Not much have changed since,
though now we have a classical Django registration form (user name + password + password check) instead of a modern one.

The above example should give you an idea of how signup flows can differ from each other.



Built-in signup flows
---------------------

Signup flow classes are places in ``sitegate.signup_flows`` module.

These are the options:


* Modern flows - ``sitegate.signup_flows.modern``


    * **ModernSignup**

        Modernized registration flow based on classic from Django built-in with unique e-mail field, without username and second password fields.

        *Default form:* e-mail + password

        .. note::

            E-mail in this flow is unique and automatically stored both to e-mail and username.

        .. note::

            This sign up flow is the default one. It means that it will be used if you decorate your view with ``@signup_view``
            decorator both without any parameters, or without ``flow`` parameter.


* Classic flows - ``sitegate.signup_flows.classic``


    * **ClassicSignup**

        Classic registration flow borrowed from Django built-in UserCreationForm.

        *Default form:* username + password + password retype


    * **SimpleClassicSignup**

        Classic registration flow borrowed from Django built-in without second password field.

        *Default form:* username + password



    .. note::

        Keep in mind that e-mail in the classical flows below is not unique. It means that several users may have the same e-mail.

        If you're looking for unique e-mail functionality consider using **Modern** flow pack.


    * **ClassicWithEmailSignup**

        Classic registration flow borrowed from Django built-in with additional e-mail field.

        *Default form:* username + e-mail + password + password retype


    * **ClassicWithEmailSignup**

        Classic registration flow borrowed from Django built-in with e-mail field, but without second password field.

        *Default form:* username + e-mail + password



Combining signup flows
----------------------

You can use more than one signup flow with the same view, by stacking ``@signup_view`` decorators:

.. code-block:: python

    from django.shortcuts import render

    from sitegate.signup_flows.classic import ClassicSignup
    from sitegate.decorators import signup_view

    # We'll use some our mythical MySignup flow, so let's import it.
    from .my_signup_flows import MySignup

    # Stack our decorators.
    @signup_view(flow=MySignup)
    @signup_view(flow=ClassicSignup)
    def login(request):
        return render(request, 'login.html', {'title': 'Login & Sign up'})


Additionally you'll need to extend your template. Let's extend the one from *Getting started* section:

.. code-block:: html

    {% extends "_base.html" %}
    {% load sitegate %}

    {% block page_contents %}
        <div class="my_signup_block one">
            {% sitegate_signup_form for ClassicSignup %}
        </div>
        <div class="my_signup_block two">
            {% sitegate_signup_form for MySignup %}
        </div>
    {% endblock %}


Now your users might use either of two registration methods.



Form templates
--------------

**sitegate** uses templates to render forms bound to signup flows, and is shipped with several of them for your convenience.

Signup form templates are stored under ``sitegate/templates/sitegate/signup/``. Feel free to examine them in need.

The following templates are shipped with the application:

* **form_as_p.html** - This  contents identical to that produced by *form.as_p*.

    .. note::

        This is the **default template**. It means that it will be used if you decorate your view with ``@signup_view``
        decorator both without ``template`` parameter given.


* **form_bootstrap.html** - This template produces HTML ready to use with Twitter Bootstrap Framework.

* **form_foundation.html** - This template produces HTML ready to use with Foundation Framework.



Swapping form templates
-----------------------

If the built-in templates is not what you want, you can swap them for your own:

.. code-block:: python

    from django.shortcuts import render

    from sitegate.decorators import signup_view

    # I command: use my template. Its name is `my_sign_up_form.html` %)
    @signup_view(template='my_sign_up_form.html')
    def login(request):
        return render(request, 'login.html', {'title': 'Login & Sign up'})


And that's all what you need to tell **sitegate** to use your custom template.



Batch styling form widgets
--------------------------

Now if the only thing that makes you uncomfortable with sign up is that form widgets (e.g. text inputs) lack
styling and, say, it is required by some CSS framework you use, **sitegate** will help you to handle it.

Use ``widget_attrs`` parameter for ``@signup_view`` decorator to accomplish the task:

.. code-block:: python

    from django.shortcuts import render

    from sitegate.decorators import signup_view

    # Let's use the built-in template for Twitter Bootstrap
    # and align widgets to span6 column,
    # and use field label as a placeholder, that will be rendered by Bootstrap as a hint inside text inputs.
    @signup_view(widget_attrs={'class': 'span6', 'placeholder': lambda f: f.label}, template='sitegate/signup/form_bootstrap.html')
    def login(request):
        return render(request, 'login.html', {'title': 'Login & Sign up'})

The most interesting thing here is probably *lambda*. It receives field instance, so you can customize widget attribute
values in accordance with some field data.



Signup signals
--------------

These are signal bound to signup flows. They are stored in ``sitegate.signals``.

You can listen to them (see Django documentation on signals), and do some stuff when they are happen:


* **sig_user_signup_success**

  Emitted when user successfully signs up.

  *Parameters:* ``signup_result`` - result object, e.g. created User; ``flow`` - signup flow name, 'request' - Request object.


* **sig_user_signup_fail**

  Emitted when user sign up fails.

  *Parameters:* ``signup_result`` - result object, e.g. created User; ``flow`` - signup flow name, 'request' - Request object.

