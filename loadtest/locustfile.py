import json
from os import path
from django.core.files.uploadedfile import SimpleUploadedFile

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

class Visualizer(HttpUser):
    host = HOST
    tasks = [DefVisualizer]
    wait_time = between(3,5)



class Voters(HttpUser):
    host = HOST
    tasks = [DefVoters]
    wait_time= between(3,5)


class DefImportGroup(SequentialTaskSet):

    def on_start(self):
        with open('admin.json') as f:
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
    def importGroup(self):
        # Obtiene el path home/francisco/Escritorio/decide-part-chullo/decide/decide/authentication/files/testfiles/testgroup1.txt
        basepath = path.dirname(__file__)
        filepath = path.abspath(path.join(basepath, "..", "decide/census/files/testfiles/testgroup1.txt"))
        f = open(filepath, "r")
        files = {"file": f}

        self.client.post("/census/groups/import/", 
            data = {"name": "Grupo 1"}, files=files)        


# PARA QUE FUNCIONE, DESCOMENTAR @csrf_exempt en el método importGroup del views.py de authentication
class ImportGroup(HttpUser):
    host = HOST
    tasks = [DefImportGroup]
    wait_time= between(3,5)



class DefExportGroup(SequentialTaskSet):

    def on_start(self):
        with open('admin.json') as f:
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
    def exportGroup(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.client.post("/census/groups/export/", {
            "group": "Grupo 1",
        }, headers=headers)


# PARA QUE FUNCIONE, DESCOMENTAR @csrf_exempt en el método exportGroup del views.py de authentication
class ExportGroup(HttpUser):
    host = HOST
    tasks = [DefExportGroup]
    wait_time= between(3,5)