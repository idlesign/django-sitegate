import pytest
from django.urls import reverse

from sitegate.models import EmailConfirmation, BlacklistedDomain
from sitegate.signup_flows.base import SignupFlow
from sitegate.signup_flows.modern import ModernSignup


def test_verify_email(user, request_client, messages):
    result = request_client().get(reverse('verify_email', args=['42']))

    headers = getattr(result, 'headers', None)
    if headers is None:
        # pre Django 3.2
        location = result._headers['location'][1]
    else:
        location = headers['location']

    assert location.endswith('/')
    assert len(messages) == 1
    assert 'Unable to verify' in messages

    result = request_client().get(reverse('verify_email', args=[EmailConfirmation.add(user)]))
    assert 'successfully verified' in messages
    assert len(messages) == 2


def test_is_blacklisted():

    domain = BlacklistedDomain(domain='denied1.com', enabled=False)
    assert 'denied1.com' in f'{domain}'

    BlacklistedDomain.objects.bulk_create([
        domain,
        BlacklistedDomain(domain='denied2.com', enabled=True),
        BlacklistedDomain(domain='denied3.com', enabled=True),
        BlacklistedDomain(domain='denied4.co.uk', enabled=True)
    ])

    assert not BlacklistedDomain.is_blacklisted('example1@denied1.com')
    assert BlacklistedDomain.is_blacklisted('example2@denied2.com')
    assert BlacklistedDomain.is_blacklisted('example3@some.denied3.com')
    assert BlacklistedDomain.is_blacklisted('example3@some.denied3.COM')
    assert not BlacklistedDomain.is_blacklisted('example4@co.uk')
    assert BlacklistedDomain.is_blacklisted('example4@denied4.co.UK')
    assert BlacklistedDomain.is_blacklisted('example4@some.Denied4.co.UK')


class TestGenericSignupFlow:

    def test_init_exception(self):

        with pytest.raises(NotImplementedError):
            SignupFlow()

    def test_getflow_name(self):
        assert ModernSignup.get_flow_name() == 'ModernSignup'
