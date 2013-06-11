"""This file contains tests for sitegate."""
from uuid import uuid4

from django.utils import unittest
from django.core import urlresolvers
from django.test.client import RequestFactory
from django.conf.urls import patterns, url
from django.http import HttpResponseRedirect
from sitegate.decorators import signin_view, signup_view, redirect_signedin, sitegate_view
from sitegate.signup_flows.classic import *
from sitegate.signup_flows.modern import *
from sitegate.signin_flows.classic import *
from sitegate.signin_flows.modern import *
from sitegate.models import *
from sitegate.utils import USER


class MockUser(object):

    def __init__(self, logged_in):
        self.logged_in = logged_in

    def is_authenticated(self):
        return self.logged_in


urlpatterns = patterns('',
    url(r'entrance/', lambda r: None),
)


class DecoratorsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # set urlconf to test's one
        cls.urlconf_bak = urlresolvers.get_urlconf()
        urlresolvers.set_urlconf('sitegate.tests')

    @classmethod
    def tearDownClass(cls):
        urlresolvers.set_urlconf(cls.urlconf_bak)

    def setUp(self):
        self.req_factory = RequestFactory()

    def test_signin(self):
        # simple decoration
        response = signin_view(lambda req: req)(self.req_factory.get('/signin/'))
        self.assertTrue(hasattr(response, 'sitegate'))
        self.assertTrue('signin_forms' in response.sitegate)
        self.assertFalse('signup_forms' in response.sitegate)

        # simple decoration + view with args
        response = signin_view(lambda req, a1, a2='b': (req, a1, a2))(self.req_factory.get('/signin/'), 10, a2=20)
        self.assertTrue(hasattr(response[0], 'sitegate'))
        self.assertTrue('signin_forms' in response[0].sitegate)
        self.assertFalse('signup_forms' in response[0].sitegate)
        self.assertEqual(response[1], 10)
        self.assertEqual(response[2], 20)

        # stacking
        signin_view1 = signin_view(flow=ClassicSignin)
        signin_view2 = signin_view(flow=ModernSignin)
        response = signin_view1(signin_view2(lambda req: req))(self.req_factory.get('/signin/'))
        self.assertTrue(hasattr(response, 'sitegate'))
        self.assertTrue('signin_forms' in response.sitegate)
        self.assertFalse('signup_forms' in response.sitegate)
        self.assertTrue(len(response.sitegate['signin_forms']) == 2)
        dict_keys = list(response.sitegate['signin_forms'].keys())
        self.assertIsInstance(response.sitegate['signin_forms'][dict_keys[0]], ClassicSignin.form)
        self.assertIsInstance(response.sitegate['signin_forms'][dict_keys[1]], ModernSignin.form)

        # stacking with args
        signin_view1 = signin_view(flow=ClassicSignin, widget_attrs={'attr_name1': 'attr_value1'})
        signin_view2 = signin_view(flow=ModernSignin, widget_attrs={'attr_name2': 'attr_value2'})
        response = signin_view1(signin_view2(lambda req: req))(self.req_factory.get('/signin/'))
        self.assertTrue(hasattr(response, 'sitegate'))
        field = response.sitegate['signin_forms']['ClassicSignin'].fields.get('password')
        self.assertIn('attr_name1', field.widget.attrs)
        field = response.sitegate['signin_forms']['ModernSignin'].fields.get('password')
        self.assertIn('attr_name2', field.widget.attrs)

    def test_signup(self):
        # simple decoration
        response = signup_view(lambda req: req)(self.req_factory.get('/signup/'))
        self.assertTrue(hasattr(response, 'sitegate'))
        self.assertTrue('signup_forms' in response.sitegate)
        self.assertFalse('signin_forms' in response.sitegate)

        # simple decoration + view with args
        response = signup_view(lambda req, a1, a2='b': (req, a1, a2))(self.req_factory.get('/signup/'), 10, a2=20)
        self.assertTrue(hasattr(response[0], 'sitegate'))
        self.assertTrue('signup_forms' in response[0].sitegate)
        self.assertFalse('signin_forms' in response[0].sitegate)
        self.assertEqual(response[1], 10)
        self.assertEqual(response[2], 20)

        # stacking
        signup_view1 = signup_view(flow=ClassicSignup)
        signup_view2 = signup_view(flow=ModernSignup)
        response = signup_view1(signup_view2(lambda req: req))(self.req_factory.get('/signup/'))
        self.assertTrue(hasattr(response, 'sitegate'))
        self.assertTrue('signup_forms' in response.sitegate)
        self.assertFalse('signin_forms' in response.sitegate)
        self.assertTrue(len(response.sitegate['signup_forms']) == 2)
        dict_keys = list(response.sitegate['signup_forms'].keys())
        self.assertIsInstance(response.sitegate['signup_forms'][dict_keys[0]], ClassicSignup.form)
        self.assertIsInstance(response.sitegate['signup_forms'][dict_keys[1]], ModernSignup.form)

        # stacking with args
        signup_view1 = signup_view(flow=ClassicSignup, widget_attrs={'attr_name1': 'attr_value1'})
        signup_view2 = signup_view(flow=ModernSignup, widget_attrs={'attr_name2': 'attr_value2'})
        response = signup_view1(signup_view2(lambda req: req))(self.req_factory.get('/signup/'))
        self.assertTrue(hasattr(response, 'sitegate'))
        field = response.sitegate['signup_forms']['ClassicSignup'].fields.get('password1')
        self.assertIn('attr_name1', field.widget.attrs)
        field = response.sitegate['signup_forms']['ModernSignup'].fields.get('password1')
        self.assertIn('attr_name2', field.widget.attrs)

    def test_signinup(self):
        # simple decoration
        response = signin_view(signup_view(lambda req: req))(self.req_factory.get('/entrance/'))
        self.assertTrue(hasattr(response, 'sitegate'))
        self.assertTrue('signup_forms' in response.sitegate)
        self.assertTrue('signin_forms' in response.sitegate)

        # simple decoration + view with args
        response = signin_view(signup_view(lambda req, a1, a2='b': (req, a1, a2)))(self.req_factory.get('/entrance/'), 10, a2=20)
        self.assertTrue(hasattr(response[0], 'sitegate'))
        self.assertTrue('signup_forms' in response[0].sitegate)
        self.assertTrue('signin_forms' in response[0].sitegate)
        self.assertEqual(response[1], 10)
        self.assertEqual(response[2], 20)

        # stacking with args
        view_signin = signin_view(widget_attrs={'attr_name1': 'attr_value1'})
        view_signup = signup_view(widget_attrs={'attr_name2': 'attr_value2'})
        response = view_signin(view_signup(lambda req, a1, a2='b': (req, a1, a2)))(self.req_factory.get('/entrance/'), 10, a2=20)
        self.assertTrue(hasattr(response[0], 'sitegate'))
        self.assertTrue('signup_forms' in response[0].sitegate)
        self.assertTrue('signin_forms' in response[0].sitegate)
        self.assertEqual(response[1], 10)
        self.assertEqual(response[2], 20)
        field = response[0].sitegate['signin_forms']['ModernSignin'].fields.get('password')
        self.assertIn('attr_name1', field.widget.attrs)
        field = response[0].sitegate['signup_forms']['ModernSignup'].fields.get('password1')
        self.assertIn('attr_name2', field.widget.attrs)

    def test_redirect(self):
        # logged in
        # default redirect
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(logged_in=True)
        response = redirect_signedin(lambda req: req)(request)
        self.assertIsInstance(response, HttpResponseRedirect)

        # not logged in
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(logged_in=False)
        response = redirect_signedin(lambda req: req)(request)
        self.assertNotIsInstance(response, HttpResponseRedirect)

        # paametrized decoration
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(logged_in=True)
        redirector = redirect_signedin('/abc/')
        response = redirector(lambda req: req)(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response['Location'], '/abc/')

    def test_sitegate(self):
        # logged in
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(True)
        response = sitegate_view(lambda req: req)(request)
        self.assertIsInstance(response, HttpResponseRedirect)

        # not logged in

        # simple decoration
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(False)
        response = sitegate_view(lambda req: req)(request)
        self.assertNotIsInstance(response, HttpResponseRedirect)
        self.assertTrue(hasattr(response, 'sitegate'))
        self.assertTrue('signup_forms' in response.sitegate)
        self.assertTrue('signin_forms' in response.sitegate)

        # simple decoration + view with args
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(False)
        response = sitegate_view(lambda req, a1, a2='b': (req, a1, a2))(request, 10, a2=20)
        self.assertNotIsInstance(response, HttpResponseRedirect)
        self.assertTrue(hasattr(response[0], 'sitegate'))
        self.assertTrue('signup_forms' in response[0].sitegate)
        self.assertTrue('signin_forms' in response[0].sitegate)
        self.assertEqual(response[1], 10)
        self.assertEqual(response[2], 20)

        # parametrized decoration
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(False)
        view_sitegate = sitegate_view(widget_attrs={'attr_name1': 'attr_value1'})
        response = view_sitegate(lambda req, a1, a2='b': (req, a1, a2))(request, 10, a2=20)
        self.assertTrue(hasattr(response[0], 'sitegate'))
        field = response[0].sitegate['signin_forms']['ModernSignin'].fields.get('password')
        self.assertIn('attr_name1', field.widget.attrs)
        field = response[0].sitegate['signup_forms']['ModernSignup'].fields.get('password1')
        self.assertIn('attr_name1', field.widget.attrs)
        self.assertEqual(response[1], 10)
        self.assertEqual(response[2], 20)

class ClassicSignupFormsTest(unittest.TestCase):

    def test_classic_signup_attrs(self):
        f = ClassicSignupForm()
        fields = list(f.fields.keys())

        self.assertTrue('username' in fields)
        self.assertTrue('password1' in fields)
        self.assertTrue('password2' in fields)

    def test_simple_classic_signup_attrs(self):
        f = SimpleClassicSignupForm()
        fields = list(f.fields.keys())

        self.assertTrue('username' in fields)
        self.assertTrue('password1' in fields)
        self.assertFalse('password2' in fields)

    def test_classic_with_email_signup_attrs(self):
        f = ClassicWithEmailSignupForm()
        fields = list(f.fields.keys())

        self.assertTrue('username' in fields)
        self.assertTrue('email' in fields)
        self.assertTrue('password1' in fields)
        self.assertTrue('password2' in fields)

    def test_simple_classic_with_email_signup_attrs(self):
        f = SimpleClassicWithEmailSignupForm()
        fields = list(f.fields.keys())

        self.assertTrue('username' in fields)
        self.assertTrue('email' in fields)
        self.assertTrue('password1' in fields)
        self.assertFalse('password2' in fields)


class ModernSignupFormsTest(unittest.TestCase):

    def test_modern_signup_attrs(self):
        f = ModernSignupForm()
        fields = list(f.fields.keys())

        self.assertFalse('username' in fields)
        self.assertTrue('email' in fields)
        self.assertTrue('password1' in fields)
        self.assertFalse('password2' in fields)

    def test_invitation_signup_attrs(self):
        f = InvitationSignupForm()
        fields = list(f.fields.keys())

        self.assertFalse('username' in fields)
        self.assertTrue('code' in fields)
        self.assertTrue('email' in fields)
        self.assertTrue('password1' in fields)
        self.assertFalse('password2' in fields)


class GenericSignupFlowTest(unittest.TestCase):

    def test_init_exception(self):
        self.assertRaises(NotImplementedError, SignupFlow)

    def test_getflow_name(self):
        self.assertEqual(ModernSignup.get_flow_name(), 'ModernSignup')


class ClassicSigninFormsTest(unittest.TestCase):

    def test_classic_signin_attrs(self):
        f = ClassicSigninForm()
        fields = list(f.fields.keys())

        self.assertTrue('username' in fields)
        self.assertTrue('password' in fields)


class ModernSigninFormsTest(unittest.TestCase):

    def test_modern_signin_attrs(self):
        f = ModernSigninForm()
        fields = list(f.fields.keys())

        self.assertTrue('username' in fields)
        self.assertTrue('password' in fields)


class InvitationCodeModelTest(unittest.TestCase):

    def setUp(self):
        self.user = USER(username=str(uuid4()))
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_generate_code(self):
        code = InvitationCode.generate_code()
        self.assertIsNotNone(code)

    def test_add(self):
        code = InvitationCode.add(self.user)
        self.assertIsNotNone(code)
        self.assertEqual(code.creator, self.user)
        self.assertIsNone(code.acceptor)
        self.assertIsNotNone(code.time_created)
        self.assertIsNone(code.time_accepted)
        self.assertFalse(code.expired)

    def test_accept(self):
        code = InvitationCode.add(self.user)
        rows = InvitationCode.accept(code.code, self.user)
        self.assertEqual(rows, 1)
        updated_code = InvitationCode.objects.get(code=code.code)
        self.assertEqual(updated_code.acceptor, self.user)
        self.assertIsNotNone(updated_code.time_accepted)
        self.assertTrue(updated_code.expired)


class BlacklistedDomainModelTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        BlacklistedDomain.objects.bulk_create([
            BlacklistedDomain(domain='denied1.com', enabled=False),
            BlacklistedDomain(domain='denied2.com', enabled=True),
            BlacklistedDomain(domain='denied3.com', enabled=True)
        ])

    @classmethod
    def tearDownClass(cls):
        BlacklistedDomain.objects.all().delete()

    def test_is_blacklisted(self):
        self.assertFalse(BlacklistedDomain.is_blacklisted('example1@denied1.com'))
        self.assertTrue(BlacklistedDomain.is_blacklisted('example2@denied2.com'))
        self.assertTrue(BlacklistedDomain.is_blacklisted('example3@some.denied3.com'))
