# Customizing sign in

**django-sitegate** by default uses a simple username/e-mail + password form. Although it is a rather common use case, inevitably
there should come times, when such a sign in form is not suitable. Should it be only just styling, or entire form
that you want to change, or provide several sign in options **sitegate** has some answers for you.

Further we'll consider a number of approaches to sign in customization. But just before we start, let's talk about sign in flows.

## Sign in flows

**sitegate** uses the notion of `sign in flows` to describe sign in processes.

Besides some sign in logic each flow features a form which is used for signing in and a template to render that form.

And, of course, every sign in flow has its own **name**, so that we can address them and use at our will like so:

```python
from django.shortcuts import render

# Import a flow class to use.
from sitegate.signin_flows.classic import ClassicSignin
from sitegate.decorators import signin_view

# And use that class for sign in.
@signin_view(flow=ClassicSignin)
def login(request):
    return render(request, 'login.html', {'title': 'Sign in'})
```

The above example gives an idea of how sign in flows can differ from each other.

## Built-in sign in flows

Sign in flow classes are places in `sitegate.signin_flows` module.

These are the options:

* Modern flows — `sitegate.signin_flows.modern`

    * **ModernSignin**

        Modernized sign in flow based on classic from Django built-in with username/e-mail authentication support.

        *Default form:* username/e-mail + password

        !!! note

            This sign in flow is the default one. It means that it will be used if you decorate your view with `@signin_view`
            decorator both without any parameters, or without `flow` parameter.

        !!! warning

            This flow assumes that both E-mail and Username fields of Django User model are inhabited with the
            same value. Since Django imposes different limits to those fields, maximum value length is defined by
            the shortest of them (Username).

* Classic flows — `sitegate.signin_flows.classic`

    * **ClassicSignin**

        Classic log in flow borrowed from Django built-in AuthenticationForm.

        *Default form:* username + password

## Combining flows and templates

See [Customizing flows](025_flows_custom.md) for combining several flows in one view,
form template topics and batch widget styling.

## Redirect after sign in

After a successful sign in the user is redirected to the URL from the `next` request parameter
(as placed by Django's `login_required`), if it is present and safe (points to the current site).
This makes the standard flow work: an anonymous user visiting a protected page is redirected
to the sign in page and gets back to that page after signing in.

You can also redirect to a fixed URL passing `redirect_to` parameter to `@signin_view` as follows
(it is used when `next` is absent or unsafe):

```python
from django.shortcuts import render

from sitegate.decorators import signin_view

# Here we redirect to `/other_url`, but Django URL pattern names are also supported.
@signin_view(redirect_to='/other_url')
def login(request):
    return render(request, 'login.html', {'title': 'Sign in'})
```

## Sign in signals

You can listen to Django built-in signals from `django.contrib.auth.signals` (**user_logged_in** and **user_login_failed**), and do some stuff when they are happen

See DjangoAuth contrib documentation for more information.
