from sitegate.models import InvitationCode


def test_generate_code(user):
    assert InvitationCode.generate_code()


def test_add(user):
    code = InvitationCode.add(user)
    assert code
    assert code.creator == user
    assert code.acceptor is None
    assert code.time_created
    assert code.time_accepted is None
    assert not code.expired


def test_accept(user):
    code = InvitationCode.add(user)
    rows = InvitationCode.accept(code.code, user)
    assert rows == 1
    updated_code = InvitationCode.objects.get(code=code.code)
    assert updated_code.acceptor == user
    assert updated_code.time_accepted
    assert updated_code.expired
