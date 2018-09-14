import pytest

try:
    from django.urls import reverse

except ImportError:  # Django < 2.0
    from django.core.urlresolvers import reverse

from sitegate.signin_flows.modern import ModernSigninForm
from sitegate.signup_flows.modern import ModernSignupForm, InvitationSignupForm


URL_REGISTER = reverse('register')
URL_LOGIN = reverse('login')


@pytest.fixture
def user_signup(request_client):

    def user_signup_(user, params=None):
        default_data = {'email': user.email, 'password1': user.password_plain, 'signup_flow': 'ModernSignup'}
        default_data.update(params or {})
        return request_client().post(URL_REGISTER, default_data)

    return user_signup_


@pytest.fixture
def user_signin(request_client):

    def user_signin_(user, params=None, client=None):
        default_data = {'username': user.email, 'password': user.password_plain, 'signin_flow': 'ModernSignin'}
        default_data.update(params or {})
        if not client:
            client = request_client()
        return client.post(URL_LOGIN, default_data)

    return user_signin_


def _regenerate_email(self, name_len=20):
    self._email = '{}@mail.com'.format('a' * name_len)
    return self._email


def test_modern_signin(user_signin, user_signup, user_create, user_model):

    user = user_create(attributes={'email': 'user@host.com'})
    user.delete()

    # login with wrong credentials
    response = user_signin(user, {'username': 'nobody'})
    assert response.status_code == 200
    assert b'Please enter a correct username and password' in response.content

    # create deactivated test user
    response = user_signup(user)
    assert response['location'].endswith(reverse('ok'))

    # inactive user login
    response = user_signin(user)
    assert (
            b'This account is inactive.' in response.content or
            b'Please enter a correct username and password' in response.content)

    # activate user and try to login again
    assert user_model.objects.count() == 1
    user_model.objects.all().update(is_active=True)
    response = user_signin(user)
    assert response['location'].endswith(reverse('ok'))

    # how about to login when user is already signed in?
    response = user_signin(user, client=response.client)
    assert response['location'].endswith(reverse('fail'))

    response.client.logout()

    # more than one user with this e-mail
    user_create(attributes={'email': user.email})
    # user_model.objects.create(username='dummy', )
    response = user_signin(user)

    assert b'There is more than one user with this e-mail.' in response.content


def test_modern_signup(user_signin, user_signup, user_create, user_model):

    user = user_create(attributes={'email': 'user@host.com'})
    user.delete()

    # create deactivated user
    response = user_signup(user)
    assert response['location'].endswith(reverse('ok'))

    # auto_signin = False
    assert not str(response.client.cookies).strip()

    # he can't login yet
    assert not response.client.login(username=user.username, password=user.password_plain)

    # check fields
    db_user = user_model._default_manager.get(username=user.email)
    assert db_user.email == user.email
    assert db_user.username == user.email

    # try to sign up with the same data for a second time
    response = user_signup(user)
    assert response.status_code == 200
    assert b'A user with that e-mail already exists.' in response.content

    # try to signup with email too long
    user.email = '%s@some.com' % ('long' * 100)
    response = user_signup(user)

    assert response.status_code == 200
    assert b'length should be no more than' in response.content


class TestModernSignupForms(object):

    def test_modern_signup_attrs(self):
        f = ModernSignupForm()
        fields = set(f.fields.keys())

        assert 'username' not in fields
        assert 'email' in fields
        assert 'password1' in fields
        assert 'password2' not in fields

    def test_invitation_signup_attrs(self):
        f = InvitationSignupForm()
        fields = set(f.fields.keys())

        assert 'username' not in fields
        assert 'code' in fields
        assert 'email' in fields
        assert 'password1' in fields
        assert 'password2' not in fields


class TestModernSigninForms(object):

    def test_modern_signin_attrs(self):
        f = ModernSigninForm()
        fields = set(f.fields.keys())

        assert 'username' in fields
        assert 'password' in fields
