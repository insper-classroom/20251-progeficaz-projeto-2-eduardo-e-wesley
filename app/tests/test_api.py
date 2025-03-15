import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


@patch('controllers.imoveis.fetch_all_imoveis')
def test_listar_imoveis_retorna_sucesso(mock_fetch_all, client):
    mock_fetch_all.return_value = [
        (1, 'av. Europa', 'Avenida', 'Jd. Europa', 'São Paulo', '01449000', 'casa', 20000000, '2019-12-12'),
        (2, 'av. Brasil', 'Avenida', 'Jd. América', 'São Paulo', '01430001', 'apartamento', 50000000, '2002-12-31'),
    ]

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


@patch('controllers.imoveis.fetch_all_imoveis')
def test_listar_imoveis_retorna_erro_404_quando_nao_existem(mock_fetch_all, client):
    mock_fetch_all.return_value = []

    response = client.get('/imoveis')
    assert response.status_code == 404
    assert response.get_json() == {
        'erro': 'Nenhum imóvel encontrado',
        '_links': [
            {'href': '/imoveis', 'rel': 'create', 'type': 'POST'},
        ]
    }


@patch('controllers.imoveis.insert_imovel')
def test_criar_imovel_retorna_201_quando_sucesso(mock_insert, client):
    mock_insert.return_value = 1

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


@patch('controllers.imoveis.insert_imovel')
def test_criar_imovel_retorna_400_quando_dados_invalidos(mock_insert, client):
    mock_insert.return_value = None

    response = client.post('/imoveis', json={})
    assert response.status_code == 404
    assert response.get_json() == {
        'erro': 'Dados inválidos ou faltantes',
        '_links': [
            {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
            {'href': '/imoveis', 'rel': 'create',  'type': 'POST'},
        ]
    }



@patch('controllers.imoveis.fetch_imovel_by_id')
def test_get_imovel_por_id_retorna_200_quando_sucesso(mock_fetch_one, client):
    mock_fetch_one.return_value = (
        2, 'av. Brasil', 'Avenida', 'Jd. América', 'São Paulo',
        '01430001', 'apartamento', 50000000, '2002-12-31'
    )

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
            {'href': '/imoveis',   'rel': 'list_all','type': 'GET'},
            {'href': '/imoveis',   'rel': 'create',  'type': 'POST'},
        ]
    }


@patch('controllers.imoveis.fetch_imovel_by_id')
def test_get_imovel_por_id_retorna_404_quando_nao_existe(mock_fetch_one, client):
    mock_fetch_one.return_value = None

    response = client.get('/imoveis/999')
    assert response.status_code == 404
    assert response.get_json() == {
        'erro': 'Imóvel não encontrado',
        '_links': [
            {'href': '/imoveis','rel': 'list_all','type': 'GET'},
            {'href': '/imoveis','rel': 'create','type': 'POST'},
        ]
    }


@patch('controllers.imoveis.delete_imovel')
def test_delete_imovel_retorna_200_quando_sucesso(mock_delete, client):
    mock_delete.return_value = 1

    response = client.delete('/imoveis/1')
    assert response.status_code == 200
    assert response.get_json() == {
        'mensagem': 'Imóvel apagado com sucesso',
        '_links': [
            {'href': '/imoveis','rel': 'list_all','type': 'GET'},
            {'href': '/imoveis','rel': 'create','type': 'POST'},
        ]
    }

@patch('controllers.imoveis.delete_imovel')
def test_delete_imovel_retorna_404_quando_nao_existe(mock_delete, client):
    mock_delete.return_value = 0

    response = client.delete('/imoveis/999')
    assert response.status_code == 404
    assert response.get_json() == {
        'erro': 'Nenhum imóvel encontrado com o ID fornecido',
        '_links': [
            {'href': '/imoveis','rel': 'list_all','type': 'GET'},
            {'href': '/imoveis','rel': 'create','type': 'POST'},
        ]
    }


@patch('controllers.imoveis.update_imovel')
def test_put_imovel_retorna_200_quando_sucesso(mock_update, client):
    mock_update.return_value = 1
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
            {'href': '/imoveis',   'rel': 'list_all','type': 'GET'},
            {'href': '/imoveis',   'rel': 'create',  'type': 'POST'},
        ]
    }

@patch('controllers.imoveis.update_imovel')
def test_put_imovel_retorna_404_quando_nao_existe(mock_update, client):
    mock_update.return_value = 0

    response = client.put('/imoveis/999', json={})
    assert response.status_code == 404
    assert response.get_json() == {
        'erro': 'Nenhum imóvel encontrado com o ID fornecido',
        '_links': [
            {'href': '/imoveis','rel': 'list_all','type': 'GET'},
            {'href': '/imoveis','rel': 'create','type': 'POST'},
        ]
    }


@patch('controllers.imoveis.fetch_imoveis_by_param')
def test_listar_imoveis_por_tipo_sucesso(mock_fetch, client):
    mock_fetch.return_value = [
        (1, 'Rua A','Rua','Bairro A','São Paulo','01000-000','casa',300000,'2021-01-01'),
        (2, 'Av. B','Avenida','Bairro B','São Paulo','02000-000','casa',450000,'2022-02-02'),
    ]
    response = client.get('/imoveis/tipo/casa')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['imoveis']) == 2
    assert data['imoveis'][0]['tipo'] == 'casa'
    
    


@patch('controllers.imoveis.fetch_imoveis_by_param')
def test_listar_imoveis_por_tipo_erro_404_quando_nao_existem(mock_fetch, client):
    mock_fetch.return_value = []
    response = client.get('/imoveis/tipo/terreno')
    assert response.status_code == 404
    data = response.get_json()
    assert data['erro'] == 'Nenhum imóvel encontrado do tipo "terreno"'


@patch('controllers.imoveis.fetch_imoveis_by_param')
def test_listar_imoveis_por_cidade_sucesso(mock_fetch, client):
    mock_fetch.return_value = [
        (3, 'Rua X','Rua','Bairro X','Rio de Janeiro','22000-000','apartamento',800000,'2020-05-05')
    ]
    response = client.get('/imoveis/cidade/Rio%20de%20Janeiro')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['imoveis']) == 1
    assert data['imoveis'][0]['cidade'] == 'Rio de Janeiro'


@patch('controllers.imoveis.fetch_imoveis_by_param')
def test_listar_imoveis_por_cidade_erro_404_quando_nao_existem(mock_fetch, client):
    mock_fetch.return_value = []
    response = client.get('/imoveis/cidade/CidadeInexistente')
    assert response.status_code == 404
    data = response.get_json()
    assert data['erro'] == 'Nenhum imóvel encontrado na cidade "CidadeInexistente"'
