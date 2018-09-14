from sitegate.signup_flows.classic import ClassicWithEmailSignup, ClassicWithEmailSignupForm, ClassicSignupForm, \
    SimpleClassicSignupForm, SimpleClassicWithEmailSignupForm
from sitegate.utils import get_username_field


def test_signup(request_get, messages):
    flow = ClassicWithEmailSignup()
    assert flow.validate_email_domain
    assert not flow.verify_email
    assert not hasattr(flow, 'schedule_email')

    flow = ClassicWithEmailSignup(verify_email=True)
    assert flow.flow_args['verify_email']
    assert not flow.flow_args['activate_user']
    assert not flow.flow_args['auto_signin']
    assert hasattr(flow, 'schedule_email')

    form = ClassicWithEmailSignupForm({
        'username': 'abcom',
        'email': 'a@b.com',
        'password1': 'qwerty',
        'password2': 'qwerty',
    })
    form.flow = flow

    def fake_schedule_email(text, user, title):
        assert user.username == 'abcom'
        assert title == 'Account activation'

    flow.schedule_email = fake_schedule_email

    new_user = flow.add_user(request_get('/'), form)
    assert new_user.username == 'abcom'


class TestClassicSignupForms(object):

    def test_classic_signup_attrs(self):
        f = ClassicSignupForm()
        fields = set(f.fields.keys())

        assert get_username_field() in fields
        assert 'password1' in fields
        assert 'password2' in fields

    def test_classic_signup_validation(self, user_model):
        user_model._default_manager.create(
            username='test_duplicate', email='test_duplicate@mail.some')

        f = ClassicSignupForm(data={
            'username': 'test_duplicate',
            'email': 'test_duplicate@mail.some',
        })
        f.full_clean()
        assert 'username' in f.errors
        assert len(f.errors) == 3

        f = ClassicSignupForm(data={
            'username': 'test_duplicate',
            'email': 'test_duplicate@mail.some',
            'password1': 'password',
            'password2': 'password',
        })
        f.full_clean()
        assert 'username' in f.errors
        assert len(f.errors) == 1

    def test_simple_classic_signup_attrs(self):
        f = SimpleClassicSignupForm()
        fields = set(f.fields.keys())

        assert get_username_field() in fields
        assert 'password1' in fields
        assert 'password2' not in fields

    def test_classic_with_email_signup_attrs(self):
        f = ClassicWithEmailSignupForm()
        fields = set(f.fields.keys())

        assert get_username_field() in fields
        assert 'email' in fields
        assert 'password1' in fields
        assert 'password2' in fields

    def test_simple_classic_with_email_signup_attrs(self):
        f = SimpleClassicWithEmailSignupForm()
        fields = set(f.fields.keys())

        assert get_username_field() in fields
        assert 'email' in fields
        assert 'password1' in fields
        assert 'password2' not in fields


# @unittest.skipIf(settings.AUTH_USER_MODEL == 'auth.User', 'Custom user model required')
# class ClassicSignupCustomUserFormsTest(TestCase):
# 
#     def test_classic_signup_attrs():
#         f = ClassicSignupForm()
#         fields = set(f.fields.keys())
# 
#         assert 'email' in fields
#         assert 'password1' in fields
#         assert 'password2' in fields
# 
#     def test_classic_signup_validation():
#         get_user_model()._default_manager.create(
#             email='test_duplicate@mail.some',
#             date_of_birth=timezone.now().date(),
#         )
# 
#         f = ClassicSignupForm(data={
#             'email': 'test_duplicate@mail.some',
#         })
#         f.full_clean()
#         assert 'email' in f.errors
#         assert len(f.errors) == 3
# 
#         f = ClassicSignupForm(data={
#             'email': 'test_duplicate@mail.some',
#             'password1': 'password',
#             'password2': 'password',
#         })
#         f.full_clean()
#         assert 'email' in f.errors
#         assert len(f.errors) == 1
# 
#     def test_simple_classic_signup_attrs():
#         f = SimpleClassicSignupForm()
#         fields = set(f.fields.keys())
# 
#         assert 'username' not in fields
#         assert 'email' in fields
#         assert 'password1' in fields
#         assert 'password2' not in fields
# 
#     def test_classic_with_email_signup_attrs():
#         f = ClassicWithEmailSignupForm()
#         fields = set(f.fields.keys())
# 
#         assert 'username' not in fields
#         assert 'email' in fields
#         assert 'password1' in fields
#         assert 'password2' in fields
# 
#     def test_simple_classic_with_email_signup_attrs():
#         f = SimpleClassicWithEmailSignupForm()
#         fields = set(f.fields.keys())
# 
#         assert 'username' not in fields
#         assert 'email' in fields
#         assert 'password1' in fields
#         assert 'password2' not in fields
