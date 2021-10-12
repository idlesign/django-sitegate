from pathlib import PurePath
from typing import Optional, Any, Type

from django import forms
from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from etc.toolbox import set_form_widgets_attrs


class FlowsBase:
    """Base class for signup and sign in flows."""

    flow_type: str = None
    """Flow type alias."""

    default_form_template: str = 'form_as_p'
    """Template name (w/o extension) to be used for form rendering."""

    default_redirect_to: str = '/'
    """Default path to redirect to after form processing."""

    enabled: bool = None
    """Whether the flow is available to use."""

    disabled_text: str = None
    """Text for users, rendered when the flow is disabled."""

    form: Type[ModelForm] = None
    """Form to be rendered for this flow."""

    def __init__(self, **kwargs):
        if not getattr(self, 'form', False):
            raise NotImplementedError(f'Please define `form` attribute in your `{self.__class__.__name__}` class.')
        self.flow_args = kwargs

    def get_template_name(self, template_name: Optional[str]) -> str:
        """Returns template path, either from a shortcut built-in template
        name (`form_as_p`) or a template path (`my_sitegate/my_tpl.html`).

        Note that template path can include one `%s` placeholder. In that case
        it will be replaced with flow type (`signin` or `signup`).

        """
        if template_name is None:
            # Build default template path.
            template_name = self.default_form_template

        if '.html' not in template_name:  # Shortcut, e.g.: .
            template_name = f'sitegate/%s/{template_name}.html'

        if '%s' in template_name:  # Fill in the flow type placeholder.
            template_name = template_name % self.flow_type

        return template_name

    def handle_form_valid(self, request: HttpRequest, form: ModelForm) -> Optional[HttpResponse]:
        raise NotImplementedError  # pragma:  nocover

    def respond_for(self, view_function, args, kwargs):
        """Returns a response for the given view & args."""

        request = args[0]
        form = self.get_requested_form(request)

        if form.is_valid():
            result = self.handle_form_valid(request, form)
            if result:
                return result

        self.update_request(request, form)

        return view_function(*args, **kwargs)

    def update_request(self, request: HttpRequest, form: ModelForm):
        """Updates Request object with flows forms."""
        forms_key = f'{self.flow_type}_forms'

        # Use ordered forms dict in case _formNode wants to fetch the first defined.
        flow_dict = {}

        try:
            flow_dict = request.sitegate[forms_key]

        except AttributeError:
            request.sitegate = {}

        except KeyError:
            pass

        flow_dict[self.get_flow_name()] = form
        request.sitegate[forms_key] = flow_dict

    @classmethod
    def get_flow_name(cls) -> str:
        """Returns sign up flow identifier from flow class name.
        Example: `classic` for `ClassicSignup`.

        """
        return cls.__name__

    @staticmethod
    def login_generic(request: HttpRequest, username: str, password: str) -> bool:
        """Helper method. Generic login with username and password."""

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return True

        return False

    def get_arg_or_attr(self, name: str, default: Any = None) -> Any:
        """Returns flow argument, as provided with sitegate decorators
           or attribute set as a flow class attribute or default."""

        if name in self.flow_args:
            return self.flow_args[name]

        try:
            return getattr(self, name)

        except AttributeError:
            return default

    def get_requested_form(self, request: HttpRequest) -> ModelForm:
        """Returns an instance of a form requested."""
        flow_name = self.get_flow_name()
        flow_key = f'{self.flow_type}_flow'
        flow_enabled = self.enabled
        form_data = None

        if (flow_enabled and
            request.method == 'POST' and
            request.POST.get(flow_key, False) and
            request.POST[flow_key] == flow_name):

            form_data = request.POST

        template = self.get_template_name(self.flow_args.get('template', None))

        form = self.init_form(
            form_data,
            widget_attrs=self.flow_args.get('widget_attrs', None),
            template=template
        )

        # Attach flow identifying field to differentiate among several possible forms.
        form.fields[flow_key] = forms.CharField(required=True, initial=flow_name, widget=forms.HiddenInput)
        form.flow_enabled = flow_enabled
        form.flow_disabled_text = self.disabled_text
        form.template_name = PurePath(template).stem

        return form

    def init_form(self, form_data: dict, widget_attrs: dict = None, template: str = None) -> ModelForm:
        """Constructs, populates and returns a form.

        :param form_data:
        :param widget_attrs:
        :param template:

        """
        form = self.form(data=form_data)

        form.template = template
        # Attach flow attribute to have access from flow forms (usually to call get_arg_or_attr())
        form.flow = self

        if widget_attrs is not None:
            set_form_widgets_attrs(form, widget_attrs)

        return form
