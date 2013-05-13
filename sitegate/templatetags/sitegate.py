from django import template
from django.conf import settings

from ..exceptions import SiteGateError

register = template.Library()


@register.tag
def sitegate_signup_form(parser, token):
    """Renders sign up forms."""
    tokens = token.split_contents()
    tokens_num = len(tokens)

    if tokens_num == 1 or (tokens_num == 3 and tokens[1] == 'for'):
        flow_name = None
        if tokens_num == 3:
            flow_name = tokens[2]
        return sitegate_signup_formNode(flow_name)
    else:
        raise template.TemplateSyntaxError('"sitegate_signup_form" tag requires zero or two arguments. E.g. {%% sitesignup_form %%} or {%% sitesignup_form for ClassicSignup %%}.')


class sitegate_signup_formNode(template.Node):

    def __init__(self, flow_name):
        self.flow_name = flow_name

    def render(self, context):
        try:
            forms = context['request'].sitesignup['forms']
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
                raise SiteGateError('`sitegate_signup_form` tag is used but the appropriate sign form is not found in context.')
            return ''

        context.push()
        context['signup_form'] = flow_form
        content = template.loader.get_template(flow_form.template).render(context)
        context.pop()

        return content
