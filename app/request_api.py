import requests

URI_API = 'https://storeordersapi.herokuapp.com'


def get_headers(token):
    return {
        'Authorization': 'Bearer {}'.format(token)
    }


def register_user(name, login, email, password):
    data = {
        'nome': name,
        'login': login,
        'email': email,
        'senha': password
    }
    req = requests.post(URI_API + '/sec/register', data=data)
    return req.json()


def login_user(login, password):
    data = {
        'login': login,
        'senha': password
    }
    req = requests.post(URI_API + '/sec/login', data=data)
    return req.json()


def request_default(request):
    res = request.json()
    if 'auth' in res:
        if not res['auth']:
            raise Exception('Unauthorized')
    return res


def get_orders(token):
    req = requests.get(URI_API + '/api/pedidos/', headers=get_headers(token))
    return request_default(req)


def create_order(token, client_name, id_status, total_value, note):
    data = {
        'nome_cliente': client_name,
        'id_status': id_status,
        'valor_total': total_value,
        'observacao': note
    }
    req = requests.post(URI_API + '/api/pedidos/', headers=get_headers(token), data=data)
    return request_default(req)


def get_order(token, id_order):
    req = requests.get(URI_API + '/api/pedidos/{}/'.format(id_order), headers=get_headers(token))
    return request_default(req)


def update_order(token, id_order, client_name, id_status, total_value, note):
    data = {
        'nome_cliente': client_name,
        'id_status': id_status,
        'valor_total': total_value,
        'observacao': note
    }
    req = requests.put(URI_API + '/api/pedidos/{}/'.format(id_order), headers=get_headers(token), data=data)
    return request_default(req)


def delete_order(token, id_order):
    req = requests.delete(URI_API + '/api/pedidos/{}/'.format(id_order), headers=get_headers(token))
    return request_default(req)
