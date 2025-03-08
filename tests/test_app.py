from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_ola_lucas():
    client = TestClient(app) #Arrange: organização do teste

    response = client.get('/') # Act: o lugar q vai ter essa ação

    assert response.status_code == HTTPStatus.OK #Assert: Garantir que deu tudo certo
    assert response.json() == {'message': 'Olá lucas !'} #Assert: Garantir que enviou o olá lucas

    #json é a estrutura do dicionario na rede: (message': 'Olá lucas !) 
