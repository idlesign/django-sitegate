from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now

from sitegate.models import RemoteRecord
from sitegate.signin_flows.remotes.base import Remote, UserData
from sitegate.utils import get_registered_remotes


def test_links(request_client):
    client = request_client()
    content = client.get(reverse('login')).content.decode()
    assert 'Or sign in with' in content
    assert 'Google' in content
    assert 'Yandex' in content


def test_records(user):

    time_old = now() - timedelta(days=10)

    def create(*, old=False, **kwargs):
        record = RemoteRecord.objects.create(**kwargs)
        if old:
            record.time_created = time_old
            record.save()
        return record

    create(remote='a', old=True)
    create(remote='b')
    create(remote='c', user=user, old=True)
    create(remote='d', user=user)
    create(remote='e', user=user, remote_id='xx', old=True)
    create(remote='f', user=user, remote_id='xx')

    RemoteRecord.cleanup(ago=5)
    left = list(RemoteRecord.objects.order_by('id').values_list('remote', flat=True))

    assert left == ['b', 'c', 'd', 'e', 'f']


def test_remote_construct_user(request_post):
    remote = Remote(client_id='x')
    construct = remote.construct_user

    user_1_data = UserData(
        username='one',
        remote_id='1',
        emails=['1@1'],
        first_name='a1',
        last_name='a2',
    )
    user = construct(user_1_data)
    assert user.username == 'one'
    assert user.email == '1@1'
    assert user.first_name == 'a1'
    assert user.last_name == 'a2'

    # pick up existing user
    user_1_alt = construct(user_1_data)
    assert user_1_alt.id == user.id

    # another user with the same name
    # deduce username from email name part
    user_2 = construct(UserData(
        username='one', emails=['oneman@1'],
        remote_id='', first_name='', last_name='',
    ))
    assert user_2.id > user.id
    assert user_2.username == 'oneman'

    # yet another user with the same name
    # deduce username from full email
    user_3 = construct(UserData(
        username='one', emails=['oneman@2'],
        remote_id='', first_name='', last_name='',
    ))
    assert user_3.id > user_2.id
    assert user_3.username == 'oneman@2'

    # and yet another user with the same name
    # and email as nonactive user. give up trying
    user_3.is_active = False
    user_3.save()
    bogus_data = UserData(
        username='one', emails=['oneman@2'],
        remote_id='', first_name='', last_name='',
    )
    user_4 = construct(bogus_data)
    assert user_4 is None

    # check proper auth_finish failure
    record = RemoteRecord(remote='')
    record.save()

    response = remote.auth_finish(
        request_post(),
        user_data=bogus_data,
        remote_record=record,
        user=None,
    )
    assert response.status_code == 302


@pytest.mark.parametrize(
    ['alias', 'data_url', 'data_response'],
    [
        (
            'yandex',
            'https://login.yandex.ru/info?format=json',
            '{"id":"xx1", "login": "xx3", "emails": ["xx3@xx3"], "first_name": "xx4"}',
        ),
        (
            'google',
            'https://www.googleapis.com/oauth2/v1/userinfo?alt=json',
            '{"id":"xx1", "email": "xx3@xx3", "given_name": "xx4", "verified_email": true}',
        ),
    ]
)
def test_common(alias, data_url, data_response, request_client, response_mock, user_create):
    client = request_client()

    remote = get_registered_remotes()[alias]
    assert f'{remote}' == alias

    # user clicked on start auth link
    # we redirect to a remote
    response = client.post(remote.url_auth_start)
    assert response.status_code == 302

    record = RemoteRecord.objects.first()
    assert not record.user_id
    assert not record.remote_id
    assert not record.time_accepted
    assert f'{alias}-clid' in response.url
    assert record.code in response.url
    assert record.code in f'{record}'

    # a remote redirected user on callback
    # we render a page with js
    content = client.get(remote.url_auth_continue).content.decode()
    assert 'Signing in with' in content
    assert alias in content

    # token and other params are taken from # url part
    # and POSTed to the same view
    with response_mock(f'GET {data_url} -> 200:{data_response}'):
        response = client.post(remote.url_auth_continue, data={
            'access_token': 'dummy',
            'state': record.code,
        })
        assert response.status_code == 302

    user = User.objects.first()
    assert user.is_active
    assert user.username == 'xx3'
    assert user.email == 'xx3@xx3'
    assert user.first_name == 'xx4'
    assert user.last_name == ''

    record.refresh_from_db()
    assert record.remote_id == 'xx1'
    assert record.user_id == user.id
    assert record.time_accepted

    # code is is missing from data
    response = client.post(remote.url_auth_continue, data={})
    assert response.status_code == 302

    # no record exists
    response = client.post(remote.url_auth_continue, data={
        'state': 'some312312',
    })
    assert response.status_code == 302

    # users from record and request do not match
    user_2 = user_create()
    client_2 = request_client(user_2)
    response = client_2.post(remote.url_auth_continue, data={
        'state': record.code,
    })
    assert response.status_code == 302

    # user data fetch fail
    response = client.post(remote.url_auth_continue, data={
        'state': record.code,
    })
    assert response.status_code == 302

    # pick up a previous record
    record_2_accepted = now()
    record_2 = RemoteRecord(remote=alias, user=user_2, remote_id='xx2', time_accepted=record_2_accepted)
    record_2.save()

    data_response = data_response.replace('"xx1"', '"xx2"')

    with response_mock(f'GET {data_url} -> 200:{data_response}'):
        response = client.post(remote.url_auth_continue, data={
            'access_token': 'dummy2',
            'state': record.code,
        })
        assert response.status_code == 302
    record_2.refresh_from_db()
    assert record_2.time_accepted > record_2_accepted
    assert record_2.user == user_2
    assert record_2.remote_id == 'xx2'


def test_auth_remote_start(user_create, request_client):

    alias = 'yandex'
    remote = get_registered_remotes()[alias]

    # test auth start authorized and already linked
    user_2 = user_create()
    record = RemoteRecord(remote=alias, user=user_2)
    record.save()

    client = request_client(user=user_2)
    response = client.get(remote.url_auth_start)
    assert response.status_code == 405

    response = client.post(remote.url_auth_start)
    assert response.status_code == 302

    # auth start unknown remote alias
    response = client.post('/rauth/bogus/start/')
    assert response.status_code == 400


def test_auth_remote_continue(user_create, request_client):

    alias = 'yandex'

    user_1 = user_create()
    user_2 = user_create()

    record_1 = RemoteRecord(remote=alias, user=user_1)
    record_1.save()

    record_2 = RemoteRecord(remote=alias, user=user_2)
    record_2.save()

    client = request_client(user=user_2)

    # auth start unknown remote alias
    response = client.get('/rauth/bogus/')
    assert response.status_code == 400


def test_google(response_mock, request_post):

    remote = get_registered_remotes()['google']

    url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json'
    data = '{"id":"xx1", "email": "xx3@xx3", "given_name": "xx4", "verified_email": false}'

    with response_mock(f'GET {url} -> 200:{data}'):
        result = remote.get_user_data(request_post(), data={})
        assert result is None  # verified_email: false
