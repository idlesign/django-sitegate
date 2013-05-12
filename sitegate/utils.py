"""Contains utility functions used by sitegate."""


def apply_attrs_to_form_widgets(form, attrs):
    """Utility method. Applies the given html attributes
    to every form fields widgets.

    """
    for _, field in form.fields.items():
        attrs_ = dict(attrs)
        for name, val in attrs.items():
            if hasattr(val, '__call__'):
                attrs_[name] = val(field)
        field.widget.attrs = field.widget.build_attrs(attrs_)
