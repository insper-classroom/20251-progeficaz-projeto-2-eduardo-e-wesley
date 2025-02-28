import pytest
from unittest.mock import patch, MagicMock
from api import app, connect_db

@pytest.fixture
def client():
    app.config['TESTING'] == True
    with app.test_client() as client:
        yield client

@patch('api.connect_db')
def test_get_alunos(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, 'Alice', 'abracadabra'),
        (2, 'Bob', 'Bob show bob'),
        (3, 'Sam', 'winchester'),
        (4, 'Scooby', 'Doobydoobydoo'),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.get('/alunos')

    assert response.status_code == 200

    expected_response = {
        'alunos': [
            {'id': 1, 'nome': 'Alice', 'frase':'abracadabra'},
            {'id': 2, 'nome': 'Bob', 'frase':'Bob show Bob'},
            {'id': 3, 'nome': 'Sam', 'frase':'winchester'},
            {'id': 4, 'nome': 'Scooby', 'frase':'Doobydoobydoo'}
        ]
    }
    assert response.get_json() == expected_response


def teste_get_alunos_vazio(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    response = client.get('/alunos')

    assert response.status_code == 404
    assert response.get_json() == {'erro':'Nenhum aluno encontrado'}