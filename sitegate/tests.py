"""This file contains tests for sitegate."""
from django.test import TestCase

from sitegate.flows.classic import *
from sitegate.flows.modern import *


class ClassicSignupFormsTest(TestCase):

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


class ModernSignupFormsTest(TestCase):

    def test_modern_signup_attrs(self):
        f = ModernSignupForm()
        fields = list(f.fields.keys())

        self.assertFalse('username' in fields)
        self.assertTrue('email' in fields)
        self.assertTrue('password1' in fields)
        self.assertFalse('password2' in fields)


class GenericSignupFlowTest(TestCase):

    def test_init_exception(self):
        self.assertRaises(NotImplementedError, SignupFlow)

    def test_getflow_name(self):
        self.assertEquals(ModernSignup.get_flow_name(), 'modern')


