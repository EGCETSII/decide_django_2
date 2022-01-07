from os import name
import time
import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from selenium.webdriver.support import select
from selenium.webdriver.common.by import By

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, Question, QuestionOption
from base.tests import SeleniumBaseTestCase
import re
from selenium.webdriver.support.ui import Select
import time
from django.core import mail

class VotingTestCase(BaseTestCase):

    def setUp(self):
        # Crea un grupo con dos usuarios y otro con un usuario para probar el funcionamiento de los grupos en las votaciones
        g1 = Group(name='Grupo 1', pk=100)
        g1.save()

        g2 = Group(name='Grupo 2', pk=101)
        g2.save()

        u1 = User(username='username1Grupo1', password='password')
        u1.save()
        u1.groups.set([g1])
        u1.save()

        u2 = User(username='username2Grupo1', password='password')
        u2.save()
        u2.groups.set([g1])
        u2.save()

        u3 = User(username='username3Grupo2', password='password')
        u3.save()
        u3.groups.set([g2])
        u3.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self, type):
        q = Question(desc='test question',type=type)
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    
    def create_voting_one_question_two_options(self,type):
        q = Question(desc='test question',type=type)
        q.save()
        opt1 = QuestionOption(question=q, option='option 1')
        opt1.save()
        opt2 = QuestionOption(question=q, option='option 2')
        opt2.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v
    
    def test_create_voting_one_question_two_options(self):
        voting_types= ['SO', 'MC']
        for type in voting_types:
            new_voting_to_store= self.create_voting_one_question_two_options(type)
            voting_retrieved_database= Voting.objects.get(pk= new_voting_to_store.pk)
            self.assertEquals(voting_retrieved_database.question.options.all()[0].option, 'option 1')
            self.assertEquals(voting_retrieved_database.question.options.all()[1].option, 'option 2')
            self.assertEquals(voting_retrieved_database.question.desc, 'test question')
            self.assertEquals(voting_retrieved_database.name, 'test voting')
            self.assertEquals(voting_retrieved_database.question.type, type )



    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes_single_option(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()
        clear = {}
        for opt in v.question.options.all():
            clear[opt.number] = 0
            for i in range(random.randint(0, 5)): # Añadimos un número de votaciones aleatorias a cada opción de la pregunta
                a, b = self.encrypt_msg(opt.number, v)
                data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'votes': [{ 'a': a, 'b': b }]
                }
                clear[opt.number] += 1
                user = self.get_or_create_user(voter.voter_id)
                self.login(user=user.username)
                voter = voters.pop()
                mods.post('store', json=data)
        return clear

    def store_votes_multiple_choice(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        choices= [opt for opt in v.question.options.all()]
        num_total_choices= len(choices)
        clear= {} # Indicará el número de veces que se ha votado cada opción

        for opt in choices: #Inicializamos el diccionario 
            clear[opt.number] = 0
    
        for voter in voters[:10]: #Realizamos votaciones múltiples con 10 usuarios
            votes= []
            for opt in random.sample(choices, random.randint(1,num_total_choices)): #El usuario selecciona varias opciones de forma aleatoria
                a, b = self.encrypt_msg(opt.number, v)
                encrypted_option= { 'a': a, 'b': b }
                votes.append(encrypted_option)
                clear[opt.number] += 1

            data = {
                    'voting': v.id,
                    'voter': voter.voter_id,
                    'votes': votes
                }
            user = self.get_or_create_user(voter.voter_id)
            self.login(user=user.username)
            mods.post('store', json=data)
        return clear

    def test_complete_voting_single_option(self):
      
            v = self.create_voting('SO')
            self.create_voters(v)
            v.create_pubkey()
            v.start_date = timezone.now()
            v.save()
            clear = self.store_votes_single_option(v)
            self.login()  # set token
            v.tally_votes(self.token)

            tally = v.tally
            tally.sort()
            tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}
            for q in v.question.options.all():

                self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

            for q in v.postproc:
                self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_complete_voting_multiple_choice(self):

            v = self.create_voting('MC')
            self.create_voters(v)
            v.create_pubkey()
            v.start_date = timezone.now()
            v.save()
            clear= self.store_votes_multiple_choice(v) # Método para guardar votos de selección múltiple
            self.login()  # set token
            v.tally_votes(self.token)

            tally = v.tally
            tally.sort()
            tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}
            for q in v.question.options.all():

                self.assertEqual(tally.get(q.number, 0), clear.get(q.number, 0))

            for q in v.postproc:
                self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        
        data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse'],
            'question_type': 'MC'
        }
        

        # Petición post correcta
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

        # Comprobamos que se ha creado la votación en la base de datos
        voting = Voting.objects.get(name='Example')
        self.assertEqual(voting.desc, 'Description example')
        self.assertEqual(voting.question.desc, 'I want a ')
        self.assertEqual(voting.question.type, 'MC')
        self.assertEquals(voting.question.options.all()[0].option, 'cat')
        self.assertEquals(voting.question.options.all()[1].option, 'dog')
        self.assertEquals(voting.question.options.all()[2].option, 'horse')

    
    # Comprueba que si no le ofrecemos a la API un tipo de votación, se crea de tipo "Single Option" de manera predeterminada
    def test_create_voting_from_API_SO_default(self):
        
        self.login()

        data_without_question_type= {
            'name': 'Example2',
            'desc': 'Description example2',
            'question': 'I want a...',
            'question_opt': ['cat', 'dog', 'horse'],
        }

        #Comprobamos que si no se envía el campo question_type , se asigna de forma predeterminada el tipo "single_option"
        response = self.client.post('/voting/', data_without_question_type, format='json')
        self.assertEqual(response.status_code, 201)
        voting = Voting.objects.get(name='Example2')
        self.assertEquals(voting.question.type, 'SO')

    def test_create_voting_from_api_incorrect_questionType(self):
        # login with user admin
        self.login()
        
        incorrect_data = {
            'name': 'Example',
            'desc': 'Description example',
            'question': 'I want a ',
            'question_opt': ['cat', 'dog', 'horse'],
            'question_type': 'XX'
        }
         # Petición post incorrecta (question_type incorrecto)
        response = self.client.post('/voting/', incorrect_data, format='json')
        self.assertEqual(response.status_code, 400) 

    def test_update_voting(self):
        voting = self.create_voting('SO')

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        # data = {'action': 'tally'}
        # response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        # self.assertEqual(response.status_code, 400)
        # self.assertEqual(response.json(), 'Voting already tallied')


    def test_create_voting_api_with_group(self):
        self.login()

        #formato incorrecto para groups
        data = {
            'name': 'vot_test2',
            'desc': 'desc_test2',
            'question': 'quest_test',
            'question_opt': ['1', '2'],
            'question_type': 'SO',
            'groups': 'prueba'
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)

        #intento crear votacion con grupo que no existe
        data = {
            'name': 'vot_test2',
            'desc': 'desc_test2',
            'question': 'quest_test',
            'question_opt': ['1', '2'],
            'question_type': 'SO',
            'groups': '145646'
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 400)

        #formato correcto para groups
        data = {
            'name': 'vot_test2',
            'desc': 'desc_test2',
            'question': 'quest_test',
            'question_opt': ['1', '2'],
            'question_type': 'SO',
            'groups': '100,101'
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

        voting = Voting.objects.get(name='vot_test2')
        self.assertEqual(voting.desc, 'desc_test2')

        numUsersInCensus = Census.objects.filter(voting_id=voting.pk).count()
        self.assertEqual(numUsersInCensus, 3)

class SeleniumTestCase(SeleniumBaseTestCase):    

    def setUp(self):
        a = Auth(name='prueba', url='http://localhost:8000', me=True)
        a.save()

        q = Question(desc='pregunta de prueba',type='SO')
        q.save()
        opt1 = QuestionOption(question=q, option='opcion 1')
        opt1.save()
        opt2 = QuestionOption(question=q, option='opcion 2')
        opt2.save()

        g1 = Group(name='Grupo 1', pk=100)
        g1.save()

        g2 = Group(name='Grupo 2', pk=101)
        g2.save()

        u1 = User(username='username1Grupo1', password='password')
        u1.save()
        u1.groups.set([g1])
        u1.save()

        u2 = User(username='username2Grupo1', password='password')
        u2.save()
        u2.groups.set([g1])
        u2.save()

        u3 = User(username='username3Grupo2', password='password')
        u3.save()
        u3.groups.set([g2])
        u3.save()

        return super().setUp()

    def test_create_question(self):
        self.login()
        self.driver.find_element_by_link_text('Questions').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_desc').send_keys('Descripción de prueba')
        self.driver.find_element_by_id('id_options-0-number').send_keys('1')
        self.driver.find_element_by_id('id_options-0-option').send_keys('Opción 1')
        self.driver.find_element_by_id('id_options-1-number').send_keys('2')
        self.driver.find_element_by_id('id_options-1-option').send_keys('Opción 2')
        select = Select(self.driver.find_element_by_id('id_type'))
        select.select_by_visible_text('Multiple_Choice')
        self.driver.find_element_by_name('_save').click()
        
        
        # Checks if it is stored in the database
        self.driver.find_element_by_link_text('Descripción de prueba').click()
        self.assertTrue(re.fullmatch(f'{self.live_server_url}/admin/voting/question/\\d*?/change/', self.driver.current_url))
        select = Select(self.driver.find_element_by_id('id_type'))
        self.assertEquals(select.first_selected_option.text,'Multiple_Choice')
        self.assertEquals(self.driver.find_element_by_id('id_desc').text,'Descripción de prueba' )



    def test_create_voting_correct(self):
        self.login()
        self.driver.find_element_by_link_text('Votings').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_name').send_keys('Votacion de prueba')
        self.driver.find_element_by_id('id_desc').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text('pregunta de prueba')

        self.driver.find_element_by_id('id_groups').send_keys('100,101')

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text('http://localhost:8000')

        self.driver.find_element_by_name('_save').click()        
        
        # Checks if it is stored in the database
        self.driver.find_element_by_link_text('Votacion de prueba').click()
        self.assertTrue(re.fullmatch(f'{self.live_server_url}/admin/voting/voting/\\d*?/change/', self.driver.current_url))

        # Comprueba que hay usuarios en el censo de dicha votacion
        self.driver.get(f'{self.live_server_url}/admin/census/census/')
        self.driver.find_element_by_tag_name(name='tr')

        # Compruebo que funciona el update de la votacion
        self.driver.get(f'{self.live_server_url}/admin/voting/voting/')
        self.driver.find_element_by_link_text('Votacion de prueba').click()
        self.driver.find_element_by_id('id_name').send_keys(' modificada')
        self.driver.find_element_by_id('id_groups').clear()
        self.driver.find_element_by_name('_save').click() 
        self.driver.find_element_by_link_text('Votacion de prueba modificada').click()
        self.assertTrue(re.fullmatch(f'{self.live_server_url}/admin/voting/voting/\\d*?/change/', self.driver.current_url))
        
        self.driver.get(f'{self.live_server_url}/admin/census/census/')
        self.assertEquals(len(self.driver.find_elements_by_tag_name(name='tr')), 0)



    
    # Varios casos incorrectos
    def test_create_voting_incorrect(self):
        self.login()

        #formato incorrecto para los grupos
        self.driver.find_element_by_link_text('Votings').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_name').send_keys('Votacion de prueba')
        self.driver.find_element_by_id('id_desc').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text('pregunta de prueba')

        self.driver.find_element_by_id('id_groups').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text('http://localhost:8000')

        self.driver.find_element_by_name('_save').click()        
        
        self.driver.find_element_by_class_name('errornote')

        # compruebo con grupo que no existe
        self.driver.find_element_by_id('id_groups').send_keys('14367')
        self.driver.find_element_by_name('_save').click()        
        
        self.driver.find_element_by_class_name('errornote')

class VotingNotificationTestCase(BaseTestCase):
    def setUp(self):
        # Crea un grupo con dos usuarios y otro con un usuario para probar el funcionamiento de los grupos en las votaciones
        g1 = Group(name='Grupo 1', pk=100)
        g1.save()

        g2 = Group(name='Grupo 2', pk=101)
        g2.save()

        u1 = User(username='username1Grupo1', password='password')
        u1.save()
        u1.groups.set([g1])
        u1.save()

        u2 = User(username='username2Grupo1', password='password')
        u2.save()
        u2.groups.set([g1])
        u2.save()

        u3 = User(username='username3Grupo2', password='password')
        u3.save()
        u3.groups.set([g2])
        u3.save()

        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        pk = v.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self, type):
        q = Question(desc='test question',type=type)
        q.save()
        for i in range(5):
            opt = QuestionOption(question=q, option='option {}'.format(i+1))
            opt.save()
        v = Voting(name='test voting', question=q)
        v.save()

        a, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        return v

# Prueba que los renders vayan a la vista correcta
    def test_notifications_template_OK(self):
        response = self.client.get('/voting/notifications_admin/')
        self.assertTemplateUsed(response, 'list_admin_notifications.html')

        response = self.client.get('/voting/notifications/')
        self.assertTemplateUsed(response, 'list_user_notifications.html')

# Prueba el envío de correo electrónico
    def test_send_email(self):
        mail.send_mail('Asunto', 'Mensaje',
            'from@example.com', ['to@example.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Asunto')




class SeleniumNotificationTestCase(SeleniumBaseTestCase):    

    def setUp(self):
        a = Auth(name='prueba', url='http://localhost:8000', me=True)
        a.save()

        q = Question(desc='pregunta de prueba',type='SO')
        q.save()
        opt1 = QuestionOption(question=q, option='opcion 1')
        opt1.save()
        opt2 = QuestionOption(question=q, option='opcion 2')
        opt2.save()

        g1 = Group(name='Grupo 1', pk=100)
        g1.save()

        g2 = Group(name='Grupo 2', pk=101)
        g2.save()

        g3 = Group(name='Grupo 3', pk=102)
        g3.save()

        g4 = Group(name='Grupo 4', pk=103)
        g4.save()

        u1 = User(username='username1Grupo1', password='grupo123')
        u1.save()
        u1.groups.set([g1])
        u1.save()

        u2 = User(username='username2Grupo1', password='password')
        u2.save()
        u2.groups.set([g1])
        u2.save()

        u3 = User(username='username3Grupo2', password='password')
        u3.save()
        u3.groups.set([g2])
        u3.save()

        return super().setUp()

#   Prueba que un usuario administrador recibe en su apartado de notificaciones todas las nuevas votaciones
    def test_all_notifications_exist(self):

        self.login()
        self.driver.find_element_by_link_text('Votings').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_name').send_keys('Votacion de prueba')
        self.driver.find_element_by_id('id_desc').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text('pregunta de prueba')

        self.driver.find_element_by_id('id_groups').send_keys('100,101')

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text('http://localhost:8000')

        self.driver.find_element_by_name('_save').click()  
        self.driver.find_element_by_link_text('TERMINAR SESIÓN').click()            

        self.driver.get("{}".format(self.live_server_url))

        votings = Voting.objects.all()

        self.credentials = {
            'username': 'testuser',
            'password': 'decide1234',
            'is_staff': True}
        
        User.objects.create_user(**self.credentials)
        user=User.objects.get(username="testuser")
        self.assertTrue(user.is_active)
                
        self.driver.get(f"{self.live_server_url}/authentication/iniciar_sesion/")
        self.driver.find_element(By.ID, "id_username").send_keys("testuser")
        self.driver.find_element(By.ID, "id_password").send_keys("decide1234")
        self.driver.find_element_by_xpath('//button["Inicie sesión"]').click()
        
        self.driver.get("{}/voting/notifications_admin/".format(self.live_server_url))
        votings_in_view = len(self.driver.find_elements_by_xpath('//tr'))-1
        self.assertEquals(len(votings),votings_in_view)
        
# #   Prueba que si un usuario no puede votar en una votación no le aparece dicha votación en su apartado de notificaciones
    def test_notification_not_match_user(self):

        self.login()
        self.driver.find_element_by_link_text('Votings').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_name').send_keys('Votacion de prueba')
        self.driver.find_element_by_id('id_desc').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text('pregunta de prueba')

        self.driver.find_element_by_id('id_groups').send_keys('100,101')

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text('http://localhost:8000')

        self.driver.find_element_by_name('_save').click()  
        self.driver.get(f'{self.live_server_url}/admin/voting/voting/')
        self.driver.find_element_by_name('_selected_action').click()
        self.driver.find_element_by_xpath("//select[@name='action']/option[text()='Start']").click()
        self.driver.find_element_by_name('index').click()
        self.driver.find_element_by_link_text('TERMINAR SESIÓN').click()            

        self.driver.get("{}".format(self.live_server_url))

        votings = Voting.objects.all()

        self.credentials = {
            'username': 'testuser',
            'password': 'decide1234',
            'is_staff': True}
        
        User.objects.create_user(**self.credentials)
        user=User.objects.get(username="testuser")
        self.assertTrue(user.is_active)
                
        self.driver.get(f"{self.live_server_url}/authentication/iniciar_sesion/")
        self.driver.find_element(By.ID, "id_username").send_keys("testuser")
        self.driver.find_element(By.ID, "id_password").send_keys("decide1234")
        self.driver.find_element_by_xpath('//button["Inicie sesión"]').click()
        
        self.driver.get("{}/voting/notifications/".format(self.live_server_url))
        votings_in_view = len(self.driver.find_elements_by_xpath('//tr')) -1
        self.assertNotEquals(len(votings),votings_in_view)

# # Prueba que cuando se crea una votacion en la que un usuario puede participar se le añade a su apartado de notificaciones
    def test_notification_by_user(self):

        self.login()

        self.credentials = {
            'username': 'testuser',
            'password': 'decide1234'}
        
        User.objects.create_user(**self.credentials)
        user=User.objects.get(username="testuser")
        user.groups.set(['100'])
        self.assertTrue(user.is_active)

        self.driver.find_element_by_link_text('Votings').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_name').send_keys('Votacion de prueba')
        self.driver.find_element_by_id('id_desc').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text('pregunta de prueba')

        self.driver.find_element_by_id('id_groups').send_keys('100,101')

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text('http://localhost:8000')

        self.driver.find_element_by_name('_save').click()  
        self.driver.get(f'{self.live_server_url}/admin/voting/voting/')
        self.driver.find_element_by_name('_selected_action').click()
        self.driver.find_element_by_xpath("//select[@name='action']/option[text()='Start']").click()
        self.driver.find_element_by_name('index').click()
        self.driver.find_element_by_link_text('TERMINAR SESIÓN').click()            

        self.driver.get("{}".format(self.live_server_url))

        votings = Voting.objects.all()

        
        self.driver.get(f"{self.live_server_url}/authentication/iniciar_sesion/")
        self.driver.find_element(By.ID, "id_username").send_keys("testuser")
        self.driver.find_element(By.ID, "id_password").send_keys("decide1234")
        self.driver.find_element_by_xpath('//button["Inicie sesión"]').click()
        
        self.driver.get("{}/voting/notifications/".format(self.live_server_url))
        votings_in_view = len(self.driver.find_elements_by_xpath('//tr')) -1
        self.assertEquals(len(votings),votings_in_view)

# Prueba el envío de correo electrónico a los usuarios que pueden participar en la votación
    def test_send_email_voting_start(self):
        self.login()

        self.credentials = {
            'username': 'testuser',
            'password': 'decide1234',
            'email': 'testuser@gmail.com'}
        
        User.objects.create_user(**self.credentials)
        user=User.objects.get(username="testuser")
        user.groups.set(['102'])
        self.assertTrue(user.is_active)

        self.driver.find_element_by_link_text('Votings').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_name').send_keys('Votacion de prueba')
        self.driver.find_element_by_id('id_desc').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text('pregunta de prueba')

        self.driver.find_element_by_id('id_groups').send_keys('102')

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text('http://localhost:8000')

        self.driver.find_element_by_name('_save').click()  
        self.driver.get(f'{self.live_server_url}/admin/voting/voting/')
        self.driver.find_element_by_name('_selected_action').click()
        self.driver.find_element_by_xpath("//select[@name='action']/option[text()='Start']").click()          
        self.driver.find_element_by_name('index').click()
        self.driver.find_element_by_link_text('TERMINAR SESIÓN').click()    

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Nueva votación creada')
        self.assertEqual(mail.outbox[0].to, ['testuser@gmail.com'])                 #Se envía el correo al usuario que puede participar


# Prueba el envío de correo electrónico a los usuarios que pueden participar en la votación
    def test_not_send_email_voting_start(self):
        self.login()

        self.credentials = {
            'username': 'testuser',
            'password': 'decide1234',
            'email': 'testuser@gmail.com'}


        User.objects.create_user(**self.credentials)
        user=User.objects.get(username="testuser")
        user.groups.set(['102'])
        self.assertTrue(user.is_active)


        self.credentials = {
            'username': 'testuser2',
            'password': 'decide1234',
            'email': 'testuse2r@gmail.com'}

        User.objects.create_user(**self.credentials)
        user=User.objects.get(username="testuser2")
        user.groups.set(['103'])
        self.assertTrue(user.is_active)

        self.driver.find_element_by_link_text('Votings').click()
        self.driver.find_element_by_class_name('object-tools').click()
        self.driver.find_element_by_id('id_name').send_keys('Votacion de prueba')
        self.driver.find_element_by_id('id_desc').send_keys('prueba')

        select = Select(self.driver.find_element_by_id('id_question'))
        select.select_by_visible_text('pregunta de prueba')

        self.driver.find_element_by_id('id_groups').send_keys('103')

        select = Select(self.driver.find_element_by_id('id_auths'))
        select.select_by_visible_text('http://localhost:8000')

        self.driver.find_element_by_name('_save').click()  
        self.driver.get(f'{self.live_server_url}/admin/voting/voting/')
        self.driver.find_element_by_name('_selected_action').click()
        self.driver.find_element_by_xpath("//select[@name='action']/option[text()='Start']").click()
        self.driver.find_element_by_name('index').click()
        self.driver.find_element_by_link_text('TERMINAR SESIÓN').click()    
      


        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Nueva votación creada')
        self.assertNotEqual(mail.outbox[0].to, ['testuser@gmail.com'])   #Se envía un correo pero no al usuario que no puede participar                                   

