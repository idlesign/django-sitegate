from django.http import HttpResponseRedirect

from sitegate.decorators import signin_view, signup_view, redirect_signedin, sitegate_view
from sitegate.signin_flows.classic import ClassicSignin
from sitegate.signin_flows.modern import ModernSignin
from sitegate.signup_flows.classic import ClassicSignup
from sitegate.signup_flows.modern import ModernSignup


def test_signin(request_get):
    # simple decoration
    response = signin_view(lambda req: req)(request_get('/signin/'))
    assert hasattr(response, 'sitegate')
    assert 'signin_forms' in response.sitegate
    assert 'signup_forms' not in response.sitegate

    # simple decoration + view with args
    response = signin_view(lambda req, a1, a2='b': (req, a1, a2))(request_get('/signin/'), 10, a2=20)
    assert hasattr(response[0], 'sitegate')
    assert 'signin_forms' in response[0].sitegate
    assert 'signup_forms' not in response[0].sitegate
    assert response[1] == 10
    assert response[2] == 20

    # stacking
    signin_view1 = signin_view(flow=ClassicSignin)
    signin_view2 = signin_view(flow=ModernSignin)
    response = signin_view1(signin_view2(lambda req: req))(request_get('/signin/'))
    assert hasattr(response, 'sitegate')
    assert 'signin_forms' in response.sitegate
    assert 'signup_forms' not in response.sitegate
    assert len(response.sitegate['signin_forms']) == 2
    dict_keys = list(response.sitegate['signin_forms'].keys())
    assert isinstance(response.sitegate['signin_forms'][dict_keys[0]], ClassicSignin.form)
    assert isinstance(response.sitegate['signin_forms'][dict_keys[1]], ModernSignin.form)

    # stacking with args
    signin_view1 = signin_view(flow=ClassicSignin, widget_attrs={'attr_name1': 'attr_value1'})
    signin_view2 = signin_view(flow=ModernSignin, widget_attrs={'attr_name2': 'attr_value2'})
    response = signin_view1(signin_view2(lambda req: req))(request_get('/signin/'))
    assert hasattr(response, 'sitegate')
    field = response.sitegate['signin_forms']['ClassicSignin'].fields.get('password')
    assert 'attr_name1' in field.widget.attrs
    field = response.sitegate['signin_forms']['ModernSignin'].fields.get('password')
    assert 'attr_name2' in field.widget.attrs


def test_signup(request_get):
    # simple decoration
    response = signup_view(lambda req: req)(request_get('/signup/'))
    assert hasattr(response, 'sitegate')
    assert 'signup_forms' in response.sitegate
    assert 'signin_forms' not in response.sitegate

    # simple decoration + view with args
    response = signup_view(lambda req, a1, a2='b': (req, a1, a2))(request_get('/signup/'), 10, a2=20)
    assert hasattr(response[0], 'sitegate')
    assert 'signup_forms' in response[0].sitegate
    assert 'signin_forms' not in response[0].sitegate
    assert response[1] == 10
    assert response[2] == 20

    # stacking
    signup_view1 = signup_view(flow=ClassicSignup)
    signup_view2 = signup_view(flow=ModernSignup)
    response = signup_view1(signup_view2(lambda req: req))(request_get('/signup/'))
    assert hasattr(response, 'sitegate')
    assert 'signup_forms' in response.sitegate
    assert 'signin_forms' not in response.sitegate
    assert len(response.sitegate['signup_forms']) == 2
    dict_keys = list(response.sitegate['signup_forms'].keys())
    assert isinstance(response.sitegate['signup_forms'][dict_keys[0]], ClassicSignup.form)
    assert isinstance(response.sitegate['signup_forms'][dict_keys[1]], ModernSignup.form)

    # stacking with args
    signup_view1 = signup_view(flow=ClassicSignup, widget_attrs={'attr_name1': 'attr_value1'})
    signup_view2 = signup_view(flow=ModernSignup, widget_attrs={'attr_name2': 'attr_value2'})
    response = signup_view1(signup_view2(lambda req: req))(request_get('/signup/'))
    assert hasattr(response, 'sitegate')
    field = response.sitegate['signup_forms']['ClassicSignup'].fields.get('password1')
    assert 'attr_name1' in field.widget.attrs
    field = response.sitegate['signup_forms']['ModernSignup'].fields.get('password1')
    assert 'attr_name2' in field.widget.attrs


def test_signinup(request_get):
    # simple decoration
    response = signin_view(signup_view(lambda req: req))(request_get('/entrance/'))
    assert hasattr(response, 'sitegate')
    assert 'signup_forms' in response.sitegate
    assert 'signin_forms' in response.sitegate

    # simple decoration + view with args
    response = signin_view(signup_view(lambda req, a1, a2='b': (req, a1, a2)))(
        request_get('/entrance/'), 10, a2=20)

    assert hasattr(response[0], 'sitegate')
    assert 'signup_forms' in response[0].sitegate
    assert 'signin_forms' in response[0].sitegate
    assert response[1] == 10
    assert response[2] == 20

    # stacking with args
    view_signin = signin_view(widget_attrs={'attr_name1': 'attr_value1'})
    view_signup = signup_view(widget_attrs={'attr_name2': 'attr_value2'})
    response = view_signin(view_signup(lambda req, a1, a2='b': (req, a1, a2)))(
        request_get('/entrance/'), 10, a2=20)

    assert hasattr(response[0], 'sitegate')
    assert 'signup_forms' in response[0].sitegate
    assert 'signin_forms' in response[0].sitegate
    assert response[1] == 10
    assert response[2] == 20
    field = response[0].sitegate['signin_forms']['ModernSignin'].fields.get('password')
    assert 'attr_name1' in field.widget.attrs
    field = response[0].sitegate['signup_forms']['ModernSignup'].fields.get('password1')
    assert 'attr_name2' in field.widget.attrs


def test_redirect(request_get, user_create):
    # logged in
    # default redirect
    request = request_get('/entrance/', user=user_create())
    response = redirect_signedin(lambda req: req)(request)
    assert isinstance(response, HttpResponseRedirect)

    # not logged in
    request = request_get('/entrance/', user=user_create(anonymous=True))
    response = redirect_signedin(lambda req: req)(request)
    assert not isinstance(response, HttpResponseRedirect)

    # paametrized decoration
    request = request_get('/entrance/', user=user_create())
    redirector = redirect_signedin('/abc/')
    response = redirector(lambda req: req)(request)
    assert isinstance(response, HttpResponseRedirect)
    assert response['Location'] == '/abc/'


def test_sitegate(request_get, user_create):
    # logged in
    request = request_get('/entrance/', user=user_create())
    response = sitegate_view(lambda req: req)(request)
    assert isinstance(response, HttpResponseRedirect)

    # not logged in

    # simple decoration
    request = request_get('/entrance/', user=user_create(anonymous=True))
    response = sitegate_view(lambda req: req)(request)
    assert not isinstance(response, HttpResponseRedirect)
    assert hasattr(response, 'sitegate')
    assert 'signup_forms' in response.sitegate
    assert 'signin_forms' in response.sitegate

    # simple decoration + view with args
    request = request_get('/entrance/', user=user_create(anonymous=True))
    response = sitegate_view(lambda req, a1, a2='b': (req, a1, a2))(request, 10, a2=20)
    assert not isinstance(response, HttpResponseRedirect)
    assert hasattr(response[0], 'sitegate')
    assert 'signup_forms' in response[0].sitegate
    assert 'signin_forms' in response[0].sitegate
    assert response[1] == 10
    assert response[2] == 20

    # parametrized decoration
    request = request_get('/entrance/', user=user_create(anonymous=True))
    view_sitegate = sitegate_view(widget_attrs={'attr_name1': 'attr_value1'})
    response = view_sitegate(lambda req, a1, a2='b': (req, a1, a2))(request, 10, a2=20)
    assert hasattr(response[0], 'sitegate')
    field = response[0].sitegate['signin_forms']['ModernSignin'].fields.get('password')
    assert 'attr_name1' in field.widget.attrs
    field = response[0].sitegate['signup_forms']['ModernSignup'].fields.get('password1')
    assert 'attr_name1' in field.widget.attrs
    assert response[1] == 10
    assert response[2] == 20
