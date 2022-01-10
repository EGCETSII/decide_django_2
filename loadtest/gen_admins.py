import json
import requests


HOST = "http://127.0.0.1:8000"
USER = "decide2"
PASS = "complexpassword"

def login(user=USER, password=PASS):
    data = {'username': user, 'password': password}
    response = requests.post(HOST + '/authentication/login/', data=data)
    token = response.json()
    return token


def create_administrators(filename):
    
    with open(filename) as f:
        admins = json.loads(f.read())

    token = login()

    admins_pk = []
    invalid_admins = []
    for username, pwd in admins.items():
        token.update({'username': username, 'password': pwd, 'is_superuser': True})
        response = requests.post(HOST + '/authentication/register/', data=token)
        if response.status_code == 201:
            admins_pk.append({'id': response.json().get('user_pk'), 'username': username, 'pass': pwd})
        else:
            invalid_admins.append(username)
    return admins_pk, invalid_admins


current_path = '/'.join(__file__.split('/')[:-1])
admins, invalids = create_administrators(current_path + 'admin.json')
