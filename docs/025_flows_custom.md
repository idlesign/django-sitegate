# Customizing flows

This page describes customization approaches common for both signup and sign in flows.

## Combining flows

You can use more than one flow with the same view, by stacking decorators:

```python
from django.shortcuts import render

from sitegate.decorators import signup_view
from sitegate.signup_flows.classic import ClassicSignup

from .my_signup_flows import MySignup

@signup_view(flow=MySignup)
@signup_view(flow=ClassicSignup)
def register(request):
    return render(request, 'register.html', {'title': 'Sign up'})
```

Address every flow by name in your template:

```html
{% load sitegate %}

<div class="one">{% sitegate_signup_form for ClassicSignup %}</div>
<div class="two">{% sitegate_signup_form for MySignup %}</div>
```

Now your users can use either of the methods. Sign in flows are combined
the same way with `@signin_view` and `{% sitegate_signin_form %}`.

## Form templates

**sitegate** renders flow forms with templates, shipped under
`sitegate/templates/sitegate/signup/` and `sitegate/templates/sitegate/signin/`:

* **form_as_p.html** — the default template, contents identical to that produced by *form.as_p*.

* **form_bootstrap.html**, **form_bootstrap3.html**, **form_bootstrap4.html**, **form_bootstrap5.html** — HTML ready
  to use with Bootstrap Framework.

    !!! note

        Requires `form-control` class to be batch applied to every form widget
        (see `Batch styling form widgets` below), e.g. `widget_attrs={'class': 'form-control'}`.

* **form_daisyui.html** — HTML ready to use with DaisyUI 5 (Tailwind CSS).

    !!! note

        Requires `input` class to be batch applied to every form widget,
        e.g. `widget_attrs={'class': 'input'}`.

* **form_foundation.html** — HTML ready to use with Foundation Framework.

## Swapping form templates

If the built-in templates are not what you want, you can swap them for your own
using the `template` decorator parameter:

```python
from sitegate.decorators import signup_view

@signup_view(template='my_sign_up_form.html')
def register(request):
    ...
```

Built-in templates can be addressed both by a full path and with a shortcut
(filename without extension): `sitegate/signup/form_bootstrap.html` and `form_bootstrap`
are interchangeable.

## Batch styling form widgets

Use the `widget_attrs` decorator parameter to apply attributes to every form widget:

```python
from sitegate.decorators import signup_view

@signup_view(widget_attrs={'class': 'span6', 'placeholder': lambda f: f.label}, template='form_bootstrap')
def register(request):
    ...
```

A lambda receives a field instance, so attribute values can depend on field data, e.g. its label.
