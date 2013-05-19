"""This file contains tests for sitegate."""
from django.utils import unittest
from django.core import urlresolvers
from django.shortcuts import render
from django import template
from django.test.client import RequestFactory
from django.conf.urls import patterns, url
from django.http import HttpResponseRedirect

from sitegate.decorators import signin_view, signup_view, redirect_signedin, sitegate_view
from sitegate.signup_flows.classic import *
from sitegate.signup_flows.modern import *
from sitegate.signin_flows.classic import *
from sitegate.signin_flows.modern import *


class MockUser(object):
    def __init__(self, authorized):
        self.authorized = authorized

    def is_authenticated(self):
        return self.authorized


urlpatterns = patterns('',
    url(r'entrance/', lambda r: None),
)


@sitegate_view(widget_attrs={'attr_name': 'attr_value', 'attr_lambda': lambda f: f.label}, template='form_bootstrap')
def view_sitegate(request):
    return request


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

    def test_signin(self):
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

    def test_redirect(self):
        # logged in
        # default redirect
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(True)
        response = redirect_signedin(lambda req: req)(request)
        self.assertIsInstance(response, HttpResponseRedirect)

        # not logged in
        request = self.req_factory.get('/entrance/')
        request.user = MockUser(False)
        response = redirect_signedin(lambda req: req)(request)
        self.assertNotIsInstance(response, HttpResponseRedirect)

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
