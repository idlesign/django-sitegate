from django import template
from django.conf import settings

from ..exceptions import SiteGateError


register = template.Library()


class sitegate_flow_formNode(template.Node):
    """Base class for flow form nodes."""

    def __init__(self, flow_name):
        self.flow_name = flow_name

    def render(self, context):
        try:
            forms = context['request'].sitegate['%s_forms' % self.type]

            if self.flow_name is None:
                try:  # Try to use modern sign up.
                    flow_form = forms['ModernSignup']
                except KeyError:  # Try to get the first sign up flow form variable from request.
                    flow_form = forms[list(forms.keys())[0]]
            else:
                flow_form = forms[self.flow_name]
        except (AttributeError, KeyError):  # WSGI request attribute error; forms dict error.
            flow_form = None

        if flow_form is None:
            if settings.DEBUG:
                raise SiteGateError('`sitegate_%s_form` tag is used but the appropriate form is not found in context.' % self.type)
            return ''

        context.push()
        context['%s_form' % self.type] = flow_form
        content = template.loader.get_template(flow_form.template).render(context)
        context.pop()

        return content


def tag_builder(parser, token, cls, flow_type):
    """Helper function handling flow form tags."""
    tokens = token.split_contents()
    tokens_num = len(tokens)

    if tokens_num == 1 or (tokens_num == 3 and tokens[1] == 'for'):
        flow_name = None
        if tokens_num == 3:
            flow_name = tokens[2]
        return cls(flow_name)
    else:
        raise template.TemplateSyntaxError('"sitegate_%(type)s_form" tag requires zero or two arguments. E.g. {%% sitegate_%(type)s_form %%} or {%% sitegate_%(type)s_form for ClassicSignup %%}.' % {'type': flow_type})


@register.tag
def sitegate_signup_form(parser, token):
    """Renders signup forms."""
    return tag_builder(parser, token, sitegate_signup_formNode, 'signup')


@register.tag
def sitegate_signin_form(parser, token):
    """Renders signin forms."""
    return tag_builder(parser, token, sitegate_signin_formNode, 'signin')


class sitegate_signup_formNode(sitegate_flow_formNode):

    def __init__(self, flow_name):
        super(sitegate_signup_formNode, self).__init__(flow_name)
        self.type = 'signup'


class sitegate_signin_formNode(sitegate_flow_formNode):

    def __init__(self, flow_name):
        super(sitegate_signin_formNode, self).__init__(flow_name)
        self.type = 'signin'
