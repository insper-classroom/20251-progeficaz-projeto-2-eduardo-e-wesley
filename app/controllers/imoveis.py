from flask import Blueprint, request, jsonify
from repositories.imoveis_repo import *
from services.links import *

imoveis_bp = Blueprint('imoveis', __name__)

@imoveis_bp.route('/imoveis', methods=['GET'])
def listar_imoveis():
    rows = fetch_all_imoveis()
    if not rows:
        return jsonify({
            'erro': 'Nenhum imóvel encontrado',
            '_links': [{'href': '/imoveis', 'rel': 'create', 'type': 'POST'}]
        }), 404

    imoveis = []
    for (id_, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) in rows:
        imoveis.append({
            'id': id_,
            'logradouro': logradouro,
            'tipo_logradouro': tipo_logradouro,
            'bairro': bairro,
            'cidade': cidade,
            'cep': cep,
            'tipo': tipo,
            'valor': valor,
            'data_aquisicao': str(data_aquisicao),
            '_links': build_imovel_links(id_)
        })

    return jsonify({
        'imoveis': imoveis,
        '_links': build_list_links()
    }), 200


@imoveis_bp.route('/imoveis', methods=['POST'])
def criar_imovel():
    payload = request.get_json() or {}
    campos_obrigatorios = [
        'logradouro','tipo_logradouro','bairro','cidade',
        'cep','tipo','valor','data_aquisicao'
    ]
    if not all(campo in payload for campo in campos_obrigatorios):
        return jsonify({
            'erro': 'Dados inválidos ou faltantes',
            '_links': [
                {'href': '/imoveis','rel': 'list_all','type': 'GET'},
                {'href': '/imoveis','rel': 'create','type': 'POST'},
            ]
        }), 404

    novo_id = insert_imovel(payload)
    if novo_id:
        return jsonify({
            'mensagem': 'Imóvel adicionado com sucesso',
            '_links': build_message_links_create(novo_id)
        }), 201
    else:
        return jsonify({'erro': 'Dados inválidos ou faltantes'}), 400


@imoveis_bp.route('/imoveis/<int:imovel_id>', methods=['GET'])
def obter_imovel_por_id(imovel_id):
    row = fetch_imovel_by_id(imovel_id)
    if not row:
        return jsonify({
            'erro': 'Imóvel não encontrado',
            '_links': [
                {'href': '/imoveis','rel': 'list_all','type': 'GET'},
                {'href': '/imoveis','rel': 'create','type': 'POST'},
            ]
        }), 404

    (id_, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) = row

    return jsonify({
        'id': id_,
        'logradouro': logradouro,
        'tipo_logradouro': tipo_logradouro,
        'bairro': bairro,
        'cidade': cidade,
        'cep': cep,
        'tipo': tipo,
        'valor': valor,
        'data_aquisicao': str(data_aquisicao),
        '_links': build_detail_links(id_)
    }), 200


@imoveis_bp.route('/imoveis/<int:imovel_id>', methods=['PUT'])
def atualizar_imovel(imovel_id):
    payload = request.get_json() or {}
    campos_obrigatorios = [
        'logradouro','tipo_logradouro','bairro','cidade',
        'cep','tipo','valor','data_aquisicao'
    ]
    if not all(campo in payload for campo in campos_obrigatorios):
        return jsonify({
            'erro': 'Nenhum imóvel encontrado com o ID fornecido',
            '_links': [
                {'href': '/imoveis','rel': 'list_all','type': 'GET'},
                {'href': '/imoveis','rel': 'create','type': 'POST'},
            ]
        }), 404

    rows_affected = update_imovel(payload, imovel_id)
    if rows_affected == 0:
        return jsonify({
            'erro': 'Nenhum imóvel encontrado com o ID fornecido',
            '_links': [
                {'href': '/imoveis','rel': 'list_all','type': 'GET'},
                {'href': '/imoveis','rel': 'create','type': 'POST'},
            ]
        }), 404

    return jsonify({
        'mensagem': 'Imóvel atualizado com sucesso',
        '_links': build_detail_links(imovel_id)
    }), 200


@imoveis_bp.route('/imoveis/<int:imovel_id>', methods=['DELETE'])
def deletar_imovel(imovel_id):
    rows_affected = delete_imovel(imovel_id)
    if rows_affected == 0:
        return jsonify({
            'erro': 'Nenhum imóvel encontrado com o ID fornecido',
            '_links': [
                {'href': '/imoveis','rel': 'list_all','type': 'GET'},
                {'href': '/imoveis','rel': 'create','type': 'POST'},
            ]
        }), 404

    return jsonify({
        'mensagem': 'Imóvel apagado com sucesso',
        '_links': [
            {'href': '/imoveis','rel': 'list_all','type': 'GET'},
            {'href': '/imoveis','rel': 'create','type': 'POST'},
        ]
    }), 200


@imoveis_bp.route('/imoveis/tipo/<string:tipo_imovel>', methods=['GET'])
def listar_imoveis_por_tipo(tipo_imovel):
    rows = fetch_imoveis_by_param('tipo', tipo_imovel)
    if not rows:
        return jsonify({
            'erro': f'Nenhum imóvel encontrado do tipo "{tipo_imovel}"',
            '_links': [
                {'href': '/imoveis','rel': 'list_all','type': 'GET'},
                {'href': '/imoveis','rel': 'create','type': 'POST'},
            ]
        }), 404

    imoveis = []
    for (id_, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) in rows:
        imoveis.append({
            'id': id_,
            'logradouro': logradouro,
            'tipo_logradouro': tipo_logradouro,
            'bairro': bairro,
            'cidade': cidade,
            'cep': cep,
            'tipo': tipo,
            'valor': valor,
            'data_aquisicao': str(data_aquisicao),
            '_links': build_imovel_links(id_)
        })

    return jsonify({
        'imoveis': imoveis,
        '_links': build_list_links()
    }), 200


@imoveis_bp.route('/imoveis/cidade/<string:cidade_imovel>', methods=['GET'])
def listar_imoveis_por_cidade(cidade_imovel):
    rows = fetch_imoveis_by_param('cidade', cidade_imovel)
    if not rows:
        return jsonify({
            'erro': f'Nenhum imóvel encontrado na cidade "{cidade_imovel}"',
            '_links': [
                {'href': '/imoveis','rel': 'list_all','type': 'GET'},
                {'href': '/imoveis','rel': 'create','type': 'POST'},
            ]
        }), 404

    imoveis = []
    for (id_, logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao) in rows:
        imoveis.append({
            'id': id_,
            'logradouro': logradouro,
            'tipo_logradouro': tipo_logradouro,
            'bairro': bairro,
            'cidade': cidade,
            'cep': cep,
            'tipo': tipo,
            'valor': valor,
            'data_aquisicao': str(data_aquisicao),
            '_links': build_imovel_links(id_)
        })

    return jsonify({
        'imoveis': imoveis,
        '_links': build_list_links()
    }), 200
