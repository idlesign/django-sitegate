from django import forms
try:
    from collections import OrderedDict
except ImportError:
    # python 2.6 or earlier, use backport
    from ordereddict import OrderedDict

from django.contrib.auth import authenticate, login

from .utils import apply_attrs_to_form_widgets


class FlowsBase(object):
    """Base class for signup and sign in flows."""

    flow_type = None
    default_form_template = 'form_as_p'
    default_redirect_to = '/'
    enabled = None
    disabled_text = None

    def __init__(self, **kwargs):
        if not getattr(self, 'form', False):
            raise NotImplementedError('Please define `form` attribute in your `%s` class.' % self.__class__.__name__)
        self.flow_args = kwargs

    def get_template_name(self, template_name):
        """Returns template path, either from a shortcut built-in template
        name (`form_as_p`) or a template path (`my_sitegate/my_tpl.html`).

        Note that template path can include one `%s` placeholder. In that case
        it will be replaced with flow type (`signin` or `signup`).

        """
        if template_name is None:
            # Build default template path.
            template_name = self.default_form_template
        if '.html' not in template_name:  # Shortcut, e.g.: .
            template_name = '%s%s.html' % ('sitegate/%s/', template_name)
        if '%s' in template_name:  # Fill in the flow type placeholder.
            template_name = template_name % self.flow_type
        return template_name

    def handle_form_valid(self, request, form):
        """"""
        raise NotImplementedError('Please implement `handle_form_valid` method in your `%s` class.' % self.__class__.__name__)

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

    def update_request(self, request, form):
        """Updates Request object with flows forms."""
        forms_key = '%s_forms' % self.flow_type

        # Use ordered forms dict in case _formNode wants to fetch the first defined.
        flow_dict = OrderedDict()
        try:
            flow_dict = request.sitegate[forms_key]
        except AttributeError:
            request.sitegate = {}
        except KeyError:
            pass

        flow_dict[self.get_flow_name()] = form
        request.sitegate[forms_key] = flow_dict

    @classmethod
    def get_flow_name(cls):
        """Returns sign up flow identifier from flow class name.
        Example: `classic` for `ClassicSignup`.

        """
        return cls.__name__

    @staticmethod
    def login_generic(request, username, password):
        """Helper method. Generic login with username and password."""
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return True
        return False

    def get_arg_or_attr(self, name, default=None):
        """Returns flow argument, as provided with sitegate decorators
           or attribute set as a flow class attribute or default."""
        if name in self.flow_args:
            return self.flow_args[name]
        try:
            return getattr(self, name)
        except AttributeError:
            return default

    def get_requested_form(self, request):
        """Returns an instance of a form requested."""
        flow_name = self.get_flow_name()
        flow_key = '%s_flow' % self.flow_type
        form_data = None

        if request.method == 'POST' and request.POST.get(flow_key, False) and request.POST[flow_key] == flow_name:
            form_data = request.POST

        form = self.init_form(form_data, widget_attrs=self.flow_args.get('widget_attrs', None),
                              template=self.get_template_name(self.flow_args.get('template', None)))
        # Attach flow identifying field to differentiate among several possible forms.
        form.fields[flow_key] = forms.CharField(required=True, initial=flow_name, widget=forms.HiddenInput)
        form.flow_enabled = self.enabled
        form.flow_disabled_text = self.disabled_text
        return form

    def init_form(self, form_data, widget_attrs=None, template=None):
        """Constructs, populates and returns a form."""
        form = self.form(data=form_data)
        form.template = template
        # Attach flow attribute to have access from flow forms (usually to call get_arg_or_attr())
        form.flow = self
        if widget_attrs is not None:
            apply_attrs_to_form_widgets(form, widget_attrs)
        return form
