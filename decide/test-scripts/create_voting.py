import json
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random


HOST = "http://127.0.0.1:8000"
USER = "decide1"
PASS = "decide1234"

def login(user=USER, password=PASS):
    data = {'username': user, 'password': password}
    response = requests.post(HOST + '/authentication/login/', data=data)
    token = response.json()
    return token


def create_voters(filename):
    """
    Create voters with requests library from filename.json, where key are
    usernames and values are the passwords.
    """
    with open(filename) as f:
        voters = json.loads(f.read())

    token = login()

    voters_pk = []
    invalid_voters = []
    for username, pwd in voters.items():
        token.update({'username': username, 'password': pwd})
        response = requests.post(HOST + '/authentication/register/', data=token)
        if response.status_code == 201:
            voters_pk.append({'id': response.json().get('user_pk'), 'username': username, 'pass': pwd})
        else:
            invalid_voters.append(username)
    return voters_pk, invalid_voters


def add_census(voters, voting_pk):
    """
    Add to census all voters_pk in the voting_pk.
    """
    token = login()

    data2 = {'voters': [v['id'] for v in voters], 'voting_id': voting_pk}
    auth = {'Authorization': 'Token ' + token.get('token')}
    response = requests.post(HOST + '/census/', json=data2, headers=auth)
    print(response.text)

def create_voting() -> int:
    token = login()
    data = {
            'name': 'Votación para estadísticas',
            'desc': 'Esta votación se crea de prueba para poder ver las estadísticas de manera más fácil',
            'question': 'Animal preferido',
            'question_opt': ['Gato', 'Perro', 'Hamster', 'Conejo', 'Carpincho', 'Jirafa']
        }
    auth = {'Authorization': 'Token ' + token.get('token')}
    response = requests.post(HOST + '/voting/', json=data, headers=auth)
    print(response.status_code)
    voting_id = json.loads(response.text)['id']

    data = {'action': 'start'}
    response = requests.put(f'{HOST}/voting/{voting_id}/', json=data, headers=auth)
    print(response.status_code)

    return voting_id

def vote(filename):
    voters, invalids = create_voters(filename)
    voting_id = create_voting()

    if len(invalids) == 0:
        add_census(voters, voting_id)

    with open(filename) as f:
        voters = json.loads(f.read())

    print('Votaciones: ')
    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    for username, password in voters.items():
        print(f'{username} está votando...')
        if len(invalids) != 0:
            token = login(username, password)
            id_ = json.loads(requests.post(f'{HOST}/authentication/getuser/', json=token).text)['id']
            v = dict()
            v['id'] = id_
            add_census([v], voting_id)
        
        driver.get(f'{HOST}/booth/{voting_id}')
        driver.find_element_by_id('username').send_keys(username)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_xpath('//*[@id="app-booth"]/div/form/button').click()
        i = random.randint(1,5)
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="q{i}"]'))).click()
        driver.find_element_by_xpath('//*[@id="app-booth"]/div/div/button').click()
        driver.find_element_by_xpath('//*[@id="app-booth"]/nav/ul/li/a').click()
    
    token = login()
    auth = {'Authorization': 'Token ' + token.get('token')}
    data = {'action': 'stop'}
    response = requests.put(f'{HOST}/voting/{voting_id}/', json=data, headers=auth)
    print(response.status_code)

    data = {'action': 'tally'}
    response = requests.put(f'{HOST}/voting/{voting_id}/', json=data, headers=auth)
    print(response.status_code)
    print(f'Ve a {HOST}/visualizer/{voting_id} para ver los resultados.')

current_path = '/'.join(__file__.split('/')[:-1])
vote(current_path + '/voters.json')
# print(create_voting())
# voters, invalids = create_voters(current_path + '/voters.json')
# add_census(voters, create_voting())
# print("Create voters with pk={0} \nInvalid usernames={1}".format(voters, invalids))
