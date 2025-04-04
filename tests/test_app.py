from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_lucas(client):
    response = client.get('/')  # Act: o lugar q vai ter essa ação

    assert (
        response.status_code == HTTPStatus.OK
    )  # Assert: Garantir que deu tudo certo
    assert response.json() == {
        'message': 'Olá lucas !'
    }  # Assert: Garantir que enviou o olá lucas

    # json é a estrutura do dicionario na rede: (message': 'Olá lucas !)


def test_create_user(client):
    response = client.post(
        '/users/',
        json={  # UserSchema
            'username': 'testname',
            'email': 'testemail@gmail.com',
            'password': 'coxinha123',
        },
    )  # Act: o lugar q vai ter essa ação

    # validar se chegou 201, created
    assert response.status_code == HTTPStatus.CREATED

    # validar o userPublic
    assert response.json() == {
        'id': 1,
        'username': 'testname',
        'email': 'testemail@gmail.com',
    }


def test_read_user(client):
    response = client.get('/users/')

    assert (
        response.status_code == HTTPStatus.OK
    )  # Assert: Garantir que deu tudo certo

    assert response.json() == {
        'users': [
            {'id': 1, 'username': 'testname', 'email': 'testemail@gmail.com'},
        ]
    }


def test_update_user(client):
    # aqui eu tenho que mandar a senha pq
    # UserSchema pede isso
    # (user_id: int, user: UserSchema), oia aqui isso no app.py
    # pede essas duas coisas
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'rodrigo',
            'email': 'testemail@gmail.com',
            'password': 'coxinha123',
        },
    )  # Act: o lugar q vai ter essa ação

    assert response.json() == {
        'id': 1,
        'username': 'rodrigo',
        'email': 'testemail@gmail.com',
    }


def test_delete_user(client):
    response = client.delete('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_user_not_found_put(client):
    response = client.put(
        'users/1',
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
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_user_not_found_delete(client):
    response = client.delete('users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


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
