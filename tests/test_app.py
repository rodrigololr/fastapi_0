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
    #aqui eu tenho que mandar a senha pq
    #UserSchema pede isso
    # (user_id: int, user: UserSchema), oia aqui isso no app.py
    #pede essas duas coisas
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
