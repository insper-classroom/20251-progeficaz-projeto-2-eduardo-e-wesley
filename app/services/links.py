

def build_list_links():
    return [
        {'href': '/imoveis', 'rel': 'self',   'type': 'GET'},
        {'href': '/imoveis', 'rel': 'create', 'type': 'POST'},
    ]

def build_imovel_links(imovel_id):
    return [
        {'href': f'/imoveis/{imovel_id}', 'rel': 'self',   'type': 'GET'},
        {'href': f'/imoveis/{imovel_id}', 'rel': 'update', 'type': 'PUT'},
        {'href': f'/imoveis/{imovel_id}', 'rel': 'delete', 'type': 'DELETE'},
    ]

def build_detail_links(imovel_id):
    return build_imovel_links(imovel_id) + [
        {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
        {'href': '/imoveis', 'rel': 'create',   'type': 'POST'},
    ]

def build_message_links_create(imovel_id):
    return [
        {'href': f'/imoveis/{imovel_id}', 'rel': 'self',   'type': 'GET'},
        {'href': f'/imoveis/{imovel_id}', 'rel': 'update', 'type': 'PUT'},
        {'href': f'/imoveis/{imovel_id}', 'rel': 'delete', 'type': 'DELETE'},
        {'href': '/imoveis', 'rel': 'list_all', 'type': 'GET'},
    ]
