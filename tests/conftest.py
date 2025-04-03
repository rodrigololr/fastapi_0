import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)  # Arrange: organização do teste
    # colocamos o client como parametro na função
    # para facilitar nosso trabalho
