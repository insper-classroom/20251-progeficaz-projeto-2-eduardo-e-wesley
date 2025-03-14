from main import app
from database.connection import connect_db
import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client



@patch('main.connect_db')
def test_listar_imoveis_retorna_sucesso(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, 'av. Europa', 'Avenida', 'Jd. Europa', 'São Paulo',
         '01449000', 'casa', 20000000, '2019-12-12'),
        (2, 'av. Brasil', 'Avenida', 'Jd. América', 'São Paulo',
         '01430001', 'apartamento', 50000000, '2002-12-31'),
    ]
    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis')
    assert response.status_code == 200

    assert response.get_json() == {
        'imoveis': [
            {
                'id': 1,
                'logradouro': 'av. Europa',
                'tipo_logradouro': 'Avenida',
                'bairro': 'Jd. Europa',
                'cidade': 'São Paulo',
                'cep': '01449000',
                'tipo': 'casa',
                'valor': 20000000,
                'data_aquisicao': '2019-12-12',
                '_links': [
                    {'href': '/imoveis/1', 'rel': 'self',   'type': 'GET'},
                    {'href': '/imoveis/1', 'rel': 'update', 'type': 'PUT'},
                    {'href': '/imoveis/1', 'rel': 'delete', 'type': 'DELETE'},
                ]
            },
            {
                'id': 2,
                'logradouro': 'av. Brasil',
                'tipo_logradouro': 'Avenida',
                'bairro': 'Jd. América',
                'cidade': 'São Paulo',
                'cep': '01430001',
                'tipo': 'apartamento',
                'valor': 50000000,
                'data_aquisicao': '2002-12-31',
                '_links': [
                    {'href': '/imoveis/2', 'rel': 'self',   'type': 'GET'},
                    {'href': '/imoveis/2', 'rel': 'update', 'type': 'PUT'},
                    {'href': '/imoveis/2', 'rel': 'delete', 'type': 'DELETE'},
                ]
            },
        ],
        '_links': [
            {'href': '/imoveis', 'rel': 'self',   'type': 'GET'},
            {'href': '/imoveis', 'rel': 'create', 'type': 'POST'},
        ]
    }


@patch('main.connect_db')
def test_listar_imoveis_retorna_erro_404_quando_nao_existem(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchall.return_value = []
    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis')
    assert response.status_code == 404

    assert response.get_json() == {
        'erro': 'Nenhum imóvel encontrado',
        '_links': [
            {'href': '/imoveis', 'rel': 'create', 'type': 'POST'},
        ]
    }



@patch('main.connect_db')
def test_criar_imovel_retorna_201_quando_sucesso(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    mock_connect_db.return_value = mock_conn

    novo_imovel = {
        'logradouro': 'av. Europa',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Jd. Europa',
        'cidade': 'São Paulo',
        'cep': '01449000',
        'tipo': 'casa',
        'valor': 20000000,
        'data_aquisicao': '2019-12-12',
    }

    response = client.post('/imoveis', json=novo_imovel)
    assert response.status_code == 201

    assert response.get_json() == {
        'mensagem': 'Imóvel adicionado com sucesso',
        '_links': [
            {'href': '/imoveis/1', 'rel': 'self',   'type': 'GET'},
            {'href': '/imoveis/1', 'rel': 'update', 'type': 'PUT'},
            {'href': '/imoveis/1', 'rel': 'delete', 'type': 'DELETE'},
            {'href': '/imoveis',   'rel': 'list_all', 'type': 'GET'},
        ]
    }
    mock_conn.commit.assert_called_once()



@patch('main.connect_db')
def test_criar_imovel_retorna_400_quando_dados_invalidos(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_connect_db.return_value = mock_conn

    response = client.post('/imoveis', json={})
    assert response.status_code == 400

    assert response.get_json() == {
        'erro': 'Dados inválidos ou faltantes',
        '_links': [
            {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis', 'rel': 'create',  'type': 'POST'},
        ]
    }



@patch('main.connect_db')
def test_get_imovel_por_id_retorna_200_quando_sucesso(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    
    mock_cursor.fetchone.return_value = (
        2, 'av. Brasil', 'Avenida', 'Jd. América', 'São Paulo',
        '01430001', 'apartamento', 50000000, '2002-12-31'
    )
    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis/2')
    assert response.status_code == 200

    assert response.get_json() == {
        'id': 2,
        'logradouro': 'av. Brasil',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Jd. América',
        'cidade': 'São Paulo',
        'cep': '01430001',
        'tipo': 'apartamento',
        'valor': 50000000,
        'data_aquisicao': '2002-12-31',
        '_links': [
            {'href': '/imoveis/2', 'rel': 'self',   'type': 'GET'},
            {'href': '/imoveis/2', 'rel': 'update', 'type': 'PUT'},
            {'href': '/imoveis/2', 'rel': 'delete', 'type': 'DELETE'},
            {'href': '/imoveis',   'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis',   'rel': 'create',   'type': 'POST'},
        ]
    }




@patch('main.connect_db')
def test_get_imovel_por_id_retorna_404_quando_nao_existe(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None
    mock_connect_db.return_value = mock_conn

    response = client.get('/imoveis/999')
    assert response.status_code == 404

    assert response.get_json() == {
        'erro': 'Imóvel não encontrado',
        '_links': [
            {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis', 'rel': 'create',   'type': 'POST'},
        ]
    }



@patch('main.connect_db')
def test_delete_imovel_retorna_200_quando_sucesso(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    mock_connect_db.return_value = mock_conn

    response = client.delete('/imoveis/1')
    assert response.status_code == 200

    assert response.get_json() == {
        'mensagem': 'Imóvel apagado com sucesso',
        '_links': [
            {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis', 'rel': 'create',   'type': 'POST'},
        ]
    }
    mock_conn.commit.assert_called_once()





@patch('main.connect_db')
def test_delete_imovel_retorna_404_quando_nao_existe(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_connect_db.return_value = mock_conn

    response = client.delete('/imoveis/999')
    assert response.status_code == 404

    assert response.get_json() == {
        'erro': 'Nenhum imóvel encontrado com o ID fornecido',
        '_links': [
            {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis', 'rel': 'create',   'type': 'POST'},
        ]
    }



@patch('main.connect_db')
def test_put_imovel_retorna_200_quando_sucesso(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 1
    mock_connect_db.return_value = mock_conn

    new_imovel_data = {
        'logradouro': 'Av. Brasil - 50',
        'tipo_logradouro': 'Avenida',
        'bairro': 'Jd. América',
        'cidade': 'São Paulo',
        'cep': '01430001',
        'tipo': 'apartamento',
        'valor': 50000000,
        'data_aquisicao': '2002-12-31',
    }

    response = client.put('/imoveis/1', json=new_imovel_data)
    assert response.status_code == 200

    assert response.get_json() == {
        'mensagem': 'Imóvel atualizado com sucesso',
        '_links': [
            {'href': '/imoveis/1', 'rel': 'self',   'type': 'GET'},
            {'href': '/imoveis/1', 'rel': 'update', 'type': 'PUT'},
            {'href': '/imoveis/1', 'rel': 'delete', 'type': 'DELETE'},
            {'href': '/imoveis',   'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis',   'rel': 'create',   'type': 'POST'},
        ]
    }
    mock_conn.commit.assert_called_once()




@patch('main.connect_db')
def test_put_imovel_retorna_404_quando_nao_existe(mock_connect_db, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.rowcount = 0
    mock_connect_db.return_value = mock_conn

    response = client.put('/imoveis/999', json={})
    assert response.status_code == 404

    assert response.get_json() == {
        'erro': 'Nenhum imóvel encontrado com o ID fornecido',
        '_links': [
            {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis', 'rel': 'create',   'type': 'POST'},
        ]
    }
