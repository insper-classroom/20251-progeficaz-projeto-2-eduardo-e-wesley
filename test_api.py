import pytest
from unittest.mock import patch, MagicMock
from api import app, connect_db

@pytest.fixture
def client():
    app.config['TESTING'] == True
    with app.test_client() as client:
        yield client


@patch('api.connect_db')
def test_get_imoveis(mock_connect_db, client):

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, 'Alice', 'abracadabra'),
        (2, 'Bob', 'Bob show Bob'),
        (3, 'Sam', 'winchester'),
        (4, 'Scooby', 'Doobydoobydoo'),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis')

    assert response.status_code == 200

    expected_response = {
        'imoveis': [
            {'id': 1, 'imovel': 'Alice', 'endereço':'abracadabra'},
            {'id': 2, 'imovel': 'Bob', 'endereço':'Bob show Bob'},
            {'id': 3, 'imovel': 'Sam', 'endereço':'winchester'},
            {'id': 4, 'imovel': 'Scooby', 'endereço':'Doobydoobydoo'}
        ]
    }
    assert response.get_json() == expected_response



@patch('api.connect_db')
def test_get_imoveis_vazio(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []

    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis')
    assert response.status_code == 404

    assert response.get_json() == {'erro':'Nenhum imovel encontrado'}



@patch('api.connect_db')
def test_delete_passa(mock_connect_db,client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    #Simula o delete
    mock_cursor.rowcount = 1
    
    mock_cursor.fetchall.return_value = [
        (1, 'Alice', 'abracadabra'),
        (2, 'Bob', 'Bob show Bob'),
        (3, 'Sam', 'winchester'),
        (4, 'Scooby', 'Doobydoobydoo'),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.delete('/delete')
    assert response.status_code == 200

    expected_response = {'Mensagem':'Foram apagados 1 items'}
    assert response.get_json() == expected_response


@patch('api.connect_db')
def test_delete_nao_passa(mock_connect_db,client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_cursor.fetchall.return_value = [
        (1, 'Alice', 'abracadabra'),
        (2, 'Bob', 'Bob show Bob'),
    ]

    mock_connect_db.return_value = mock_conn
    response = client.delete('/delete')
    assert response.status_code == 404

    expected_response = {'Erro': "Nenhum imovel encontrado com o ID fornecido"}
    assert response.get_json() == expected_response


@patch('api.connect_db')
def test_put_imovel_passa(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, 'Alice', 'abracadabra'),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.put('/atualiza')
    assert response.status_code == 200

    expected_response = {'Mensagem':'Atualizado com Sucesso'}
    assert response.get_json() == expected_response


@patch('api.connect_db')
def test_put_imovel_nao_passa(mock_connect_db,client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, 'Alice', 'abracadabra'),
    ]

    mock_connect_db.return_value = mock_conn

    response = client.put('/atualiza')
    assert response.status_code == 404

    expected_response = {'Mensagem':'Nenhum imovel encontrado com o ID fornecido'}
    assert response.get_json() == expected_response
