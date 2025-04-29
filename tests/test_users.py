from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_integrity_error(client, user, token):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_user_not_found_put(client, user):
    invalid_token = 'invalid_token_here'

    response = client.put(
        f'users/{user.id}',
        headers={'Authorizantion': f'Bearer {invalid_token}'},
        json={
            'id': 1,
            'username': 'rodrigo',
            'email': 'testemail@gmail.com',
            'password': 'coxinha123',
        },
    )
    # tive q colocar esse json aqui pq é oq ele espera
    # se não tiver o json vai dar erro de entrada 422
    # então nos testes sempre colocar a entrada certa
    # no assert que vc deve dizer o status.code q vai acontecer rs
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_user_not_found_delete(client, user):
    invalid_token = 'invalid_token_here'
    response = client.delete(
        f'users/{user.id}',
        headers={'Authorizantion': f'Bearer {invalid_token}'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_view_user_not_found(client):
    response = client.get('users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_view_user(client):
    # criar usuário antes do teste
    response = client.post(
        '/users/',
        json={
            'username': 'rodrigo',
            'email': 'user@example.com',
            'password': '123456',
        },
    )

    assert (
        response.status_code == HTTPStatus.CREATED
    )  # pra garantir que foi criado

    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'rodrigo',
        'email': 'user@example.com',
    }


def test_create_user_username_conflict(client):
    # criar usuário com username "rodrigo"
    client.post(
        '/users/',
        json={
            'username': 'rodrigo',
            'email': 'rodrigo@email.com',
            'password': '123456',
        },
    )

    # tentar criar outro com mesmo username
    response = client.post(
        '/users/',
        json={
            'username': 'rodrigo',
            'email': 'outro@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_conflict(client):
    # Criar usuário com email
    client.post(
        '/users/',
        json={
            'username': 'user1',
            'email': 'email@email.com',
            'password': '123456',
        },
    )

    # Tentar criar outro com mesmo email
    response = client.post(
        '/users/',
        json={
            'username': 'user2',
            'email': 'email@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_different_id_user_put(client, token):
    response = client.put(
        '/users/999',  # ID diferente
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'user1',
            'email': 'email@email.com',
            'password': '123456',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_different_id_user_delete(client, token):
    response = client.delete(
        '/users/43', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
