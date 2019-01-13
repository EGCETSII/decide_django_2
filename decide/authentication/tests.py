from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

import urllib
from random import sample

from base import mods


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('1234abcd')
        u.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '1234abcd'}
        response = self.client.post('/rest-auth/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('key'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/rest-auth/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '1234abcd'}
        response = self.client.post('/rest-auth/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json() #The attribute name here obtained here is "key" instead of "token"
        key_token = {'token': token.get('key')}

        response = self.client.post('/authentication/getuser/', key_token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '1234abcd'}
        response = self.client.post('/rest-auth/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('key'))

        response = self.client.post('/rest-auth/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')

        self.assertEqual(response.data.get(id), None)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '1234abcd'}
        response = self.client.post('/rest-auth/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json() #The attribute name here obtained here is "key" instead of "token"
        key = token['key']
        self.assertTrue(key)

        response = self.client.post('/rest-auth/logout/', **{'HTTP_AUTHORIZATION':'Token {}'.format(key)})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_signup(self):
        data = {'username': 'newvoter', 'password1': '1234abcd', 'password2': '1234abcd','gender':'Male','birthdate':'2018-12-08T02:03'}
        response = self.client.post('/authentication/signup/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.filter(username='newvoter').count(), 1)
        self.assertEqual(User.objects.get(username='newvoter').userprofile.gender, 'Male')

    def test_signup_duplicated_username(self):
        data = {'username': 'newvoter', 'password1': '1234abcd', 'password2': '1234abcd','gender':'Male','birthdate':'2018-12-08T02:03'}
        response = self.client.post('/authentication/signup/', data, format='json')

        data2 = {'username': 'newvoter', 'password1': '1234abcd', 'password2': '1234abcd','gender':'Male','birthdate':'2018-12-08T02:03'}
        response2 = self.client.post('/authentication/signup/', data, format='json')

        self.assertEqual(response2.status_code, 400)
        self.assertEqual(User.objects.filter(username='voter1').count(), 1)

    def test_request_google_correct(self):
        request = urllib.request.urlopen('https://accounts.google.com/signin/oauth/oauthchooseaccount?client_id=479028502719-ums97b8c1dmn9hmdugmuibcrbma4eq9i.apps.googleusercontent.com&as=TpLMUFh-0ltXx3GkVrDr4g&destination=http%3A%2F%2Flocalhost%3A8000&approval_state=!ChRtblVrV010VXBNUW1fdExLWDZyYhIfMDVTRWJFUDFPU3NSMEVBN1JaNXdOM09kLXJ2b2Z4WQ%E2%88%99APNbktkAAAAAXCnn9kXUYpEVfktV84uqPHmUQ-y16QsT&oauthgdpr=1&xsrfsig=AHgIfE9v5HryxFZmiqcR-oPZ2lhKs65LxA&flowName=GeneralOAuthFlow', data=None, cafile=None, capath=None, cadefault=False, context=None)
        self.assertEqual(request.getcode(), 200)
