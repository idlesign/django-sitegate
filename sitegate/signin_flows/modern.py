from django import forms
from django.utils.translation import ugettext_lazy as _

from .base import SigninFlow
from .classic import ClassicSigninForm
from ..utils import USER


class ModernSigninForm(ClassicSigninForm):

    def __init__(self, request=None, *args, **kwargs):
        super(ModernSigninForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].label = u'%s / %s' % (_('Username'), _('Email'))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password and '@' in username:
            # Let's first try an e-mail auth.
            result = USER._default_manager.filter(email__iexact=username)
            if len(result) == 1:
                self.cleaned_data['username'] = result[0].username
            elif len(result) > 1:
                raise forms.ValidationError(_('There is more than one user with this e-mail. Please use your username to log in.'))

        return super(ModernSigninForm, self).clean()


class ModernSignin(SigninFlow):
    """Modernized login flow based on classic from Django built-in
    with username e-mail authentication support."""

    form = ModernSigninForm


