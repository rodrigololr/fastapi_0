from sqlalchemy import select  # type: ignore

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='alice',
        password='secret',
        email='teste@test',
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user is not None
    assert user.id == 1
    assert user.username == 'alice'
    assert user.password == 'secret'
    assert user.email == 'teste@test'
    assert user.created_at is not None  # só garante que foi setado
