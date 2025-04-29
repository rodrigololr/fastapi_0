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
