from typing import Optional

from django import template
from django.conf import settings
from django.template import Context
from django.template.base import Parser, Token
from etc.templatetags.etc_misc import include_

from ..exceptions import SiteGateError

register = template.Library()

# register tag from etc so the user are not required to add etc in INSTALLED_APPS
register.tag('sitegate_include', include_)


class sitegate_flow_formNode(template.Node):
    """Base class for flow form nodes."""

    type: str = None

    def __init__(self, flow_name: Optional[str]):
        self.flow_name = flow_name

    def render(self, context: Context) -> str:
        try:
            forms = context['request'].sitegate[f'{self.type}_forms']

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
                raise SiteGateError(
                    f'`sitegate_{self.type}_form` tag is used but the appropriate form is not found in context.')
            return ''

        context.push()
        context[f'{self.type}_form'] = flow_form

        content = template.loader.get_template(
            flow_form.template).render(context.flatten())

        return content


def tag_builder(parser: Parser, token: Token, cls, flow_type):
    """Helper function handling flow form tags."""
    tokens = token.split_contents()
    tokens_num = len(tokens)

    if tokens_num == 1 or (tokens_num == 3 and tokens[1] == 'for'):

        flow_name = None

        if tokens_num == 3:
            flow_name = tokens[2]

        return cls(flow_name)

    raise template.TemplateSyntaxError(
        f'"sitegate_{flow_type}_form" tag requires zero or two arguments. '
        f'E.g. {{%% sitegate_{flow_type}_form %%}} or '
        f'{{%% sitegate_{flow_type}_form for ClassicSignup %%}}.')


@register.tag
def sitegate_signup_form(parser: Parser, token: Token):
    """Renders signup forms."""
    return tag_builder(parser, token, sitegate_signup_formNode, 'signup')


@register.tag
def sitegate_signin_form(parser: Parser, token: Token):
    """Renders signin forms."""
    return tag_builder(parser, token, sitegate_signin_formNode, 'signin')


class sitegate_signup_formNode(sitegate_flow_formNode):

    type = 'signup'


class sitegate_signin_formNode(sitegate_flow_formNode):

    type = 'signin'
