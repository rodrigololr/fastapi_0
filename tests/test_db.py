from sqlalchemy import select  # type: ignore

from fast_zero.models import Todo, User


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
    assert user.todos == []
    assert user.created_at is not None  # só garante que foi setado


def test_create_todo(session, user):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()

    todo = session.scalar(select(Todo))

    assert todo.description == 'Test Desc'
    assert todo.id == 1
    assert todo.state == 'draft'
    assert todo.title == 'Test Todo'
    assert todo.user_id == 1


def test_user_todo_relationship(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    session.commit()
    session.refresh(user)

    user = session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]
