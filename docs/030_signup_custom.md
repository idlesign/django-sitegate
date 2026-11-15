# Customizing signup

**django-sitegate** by default uses a simple e-mail + password form. Although it is a rather common use case, inevitably
there should come times, when such a registration form is not suitable. Should it be only just styling, or entire form
that you want to change, or provide several registration options **sitegate** has some answers for you.

Further we'll consider a number of approaches to signup customization. But just before we start, let's talk about signup flows.

## Signup flows

**sitegate** uses the notion of `signup flows` to describe signup processes.

Besides some signup logic each flow features a form which is used for registration and a template to render that form.

And, of course, every signup flow has its own **name**, so that we can address them and use at our will like so:

```python
from django.shortcuts import render

# Import a flow class to use.
from sitegate.signup_flows.classic import ClassicSignup
from sitegate.decorators import signup_view

# And use that class for registration.
@signup_view(flow=ClassicSignup)
def register(request):
    return render(request, 'register.html', {'title': 'Sign up'})
```

The above example gives an idea of how signup flows can differ from each other.

## Built-in signup flows

Signup flow classes are places in `sitegate.signup_flows` module.

These are the options:

* Modern flows — `sitegate.signup_flows.modern`

    * **ModernSignup**

        Modernized registration flow based on classic from Django built-in with unique e-mail field, without username and second password fields.

        *Default form:* e-mail + password

        !!! note

            E-mail in this flow is unique and automatically stored both to e-mail and username.

        !!! note

            This sign up flow is the default one. It means that it will be used if you decorate your view with `@signup_view`
            decorator both without any parameters, or without `flow` parameter.

    * **InvitationSignup**

        Modernized registration flow with additional invitation code field.

        *Default form:* invitation code + e-mail + password

* Classic flows — `sitegate.signup_flows.classic`

    * **ClassicSignup**

        Classic registration flow borrowed from Django built-in UserCreationForm.

        *Default form:* username + password + password retype

    * **SimpleClassicSignup**

        Classic registration flow borrowed from Django built-in without second password field.

        *Default form:* username + password

    !!! note

        Keep in mind that e-mail in the classical flows below is not unique. It means that several users may have the same e-mail.

        If you're looking for unique e-mail functionality consider using **Modern** flow pack.

    * **ClassicWithEmailSignup**

        Classic registration flow borrowed from Django built-in with additional e-mail field.

        *Default form:* username + e-mail + password + password retype

    * **ClassicWithEmailSignup**

        Classic registration flow borrowed from Django built-in with e-mail field, but without second password field.

        *Default form:* username + e-mail + password

## Combining flows and templates

See [Customizing flows](025_flows_custom.md) for combining several flows in one view,
form template topics and batch widget styling.

## Redirect after signup

You can redirect to a URL passing `redirect_to` parameter to `@signup_view` as follows:

```python
from django.shortcuts import render

from sitegate.decorators import signup_view

# Here we redirect to `/other_url`, but Django URL pattern names are also supported.
@signup_view(redirect_to='/other_url')
def register(request):
    return render(request, 'register.html', {'title': 'Sign up'})
```

## Restricting signups

You can restrict signups from certain domains through Django Admin interface (`Blacklisted domains` under `Sitegate` section).

There you can define domain names that are not allowed in e-mail addresses.

Please note that all signup flows with e-mail fields will automatically validate domains against
the mentioned blacklist by default. To change this behaviour either override `validate_email_domain` flow class
attribute or provide `validate_email_domain` keyword attribute to `signup_view` decorator.

```python
...
@signup_view(validate_email_domain=False)
...
```

## Changing user activity status

By default every signup flow creates user account with status `active = True`.

To change this behaviour either override `activate_user` flow class attribute or provide `activate_user` keyword
attribute to `signup_view` decorator.

```python
...
@signup_view(activate_user=False)
...
```

## Automatic sign in on sign ups

By default every signup is followed on success by an automatic sign in. That could be changed by `auto_signin = False`.

To change this behaviour either override `auto_signin` flow class attribute or provide `auto_signin` keyword
attribute to `signup_view` decorator.

```python
...
@signup_view(auto_signin=False)
```

## Signup signals

These are signal bound to signup flows. They are stored in `sitegate.signals`.

You can listen to them (see Django documentation on signals), and do some stuff when they are happen:

* **sig_user_signup_success**

  Emitted when user successfully signs up.

  *Parameters:* `signup_result` — result object, e.g. created User; `flow` — signup flow name, `request` — Request object.

* **sig_user_signup_fail**

  Emitted when user sign up fails.

  *Parameters:* `signup_result` — result object, e.g. created User; `flow` — signup flow name, `request` — Request object.

## Custom signup flows examples

**Adding terms of service to the ModernSignup flow**

Define your signup form inheriting from `ModernSignupForm`:

```python
from sitegate.signup_flows.modern import ModernSignup, ModernSignupForm


class CustomizedSignupForm(ModernSignupForm):

    tos = forms.BooleanField(
        error_messages={'required': _('You must accept the terms and conditions')},
        label=_('I Agree To The Terms & Conditions')
    )

    class Meta:  # Redefine Meta if we have a custom User model.
        model = CustomizedUser
        fields = ('email', 'password1', 'phone', 'tos')
```

Define your signup flow inheriting from `ModernSignup`:

```python
class CustomizedSignup(ModernSignup):

    form = CustomizedSignupForm
```

Decorate your signup view with `@signup_view(flow=CustomizedSignup)`.
