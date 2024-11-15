import json

from random import choice

from locust import (
    HttpUser,
    SequentialTaskSet,
    TaskSet,
    task,
    between
)


HOST = "http://localhost:8000"
VOTING = 1


class DefVisualizer(TaskSet):

    @task
    def index(self):
        self.client.get("/visualizer/{0}/".format(VOTING))


class DefVoters(SequentialTaskSet):

    def on_start(self):
        with open('voters.json') as f:
            self.voters = json.loads(f.read())
        self.voter = choice(list(self.voters.items()))

    @task
    def login(self):
        username, pwd = self.voter
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def getuser(self):
        self.usr= self.client.post("/authentication/getuser/", self.token).json()
        print( str(self.user))

    @task
    def voting(self):
        headers = {
            'Authorization': 'Token ' + self.token.get('token'),
            'content-type': 'application/json'
        }
        self.client.post("/store/", json.dumps({
            "token": self.token.get('token'),
            "vote": {
                "a": "12",
                "b": "64"
            },
            "voter": self.usr.get('id'),
            "voting": VOTING
        }), headers=headers)


    def on_quit(self):
        self.voter = None

#Definimos las actividades de las que se compone el test de carga.
#Estas son cargar los usuarios del .json, iniciar sesión con esos datos, visitar el perfil
#y cerrar la sesión
class DefAuth(SequentialTaskSet):

    def on_start(self):
        with open('accounts.json') as f:
            self.users = json.loads(f.read())
        self.u = choice(list(self.users.items()))

    @task
    def login(self):
        username, pwd = self.u
        self.token = self.client.post("/authentication/login/", {
            "username": username,
            "password": pwd,
        }).json()

    @task
    def profile(self):
        username, pwd = self.u
        self.token = self.client.get("/authentication/profile/" + username)

    @task
    def logout(self):
        username, pwd = self.u
        self.token = self.client.get("/authentication/logoutgui/")

    def on_quit(self):
        self.voter = None

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)


class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)

#Definimos la ejecución del test con sus atributos
class Auth(HttpUser):
    host = HOST
    tasks = [DefAuth]
    wait_time= between(3,5)
