from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from base import mods

from urllib.parse import urlparse

from .models import Profile


class AuthTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)
        u = User(username='voter1')
        u.set_password('123')
        u.save()

        u2 = User(username='admin')
        u2.set_password('admin')
        u2.is_superuser = True
        u2.save()

    def tearDown(self):
        self.client = None

    def test_login(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)

        token = response.json()
        self.assertTrue(token.get('token'))

    def test_login_fail(self):
        data = {'username': 'voter1', 'password': '321'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_getuser(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 200)

        user = response.json()
        self.assertEqual(user['id'], 1)
        self.assertEqual(user['username'], 'voter1')

    def test_getuser_invented_token(self):
        token = {'token': 'invented'}
        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_getuser_invalid_token(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/authentication/getuser/', token, format='json')
        self.assertEqual(response.status_code, 404)

    def test_logout(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 1)

        token = response.json()
        self.assertTrue(token.get('token'))

        response = self.client.post('/authentication/logout/', token, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Token.objects.filter(user__username='voter1').count(), 0)

    def test_register_bad_permissions(self):
        data = {'username': 'voter1', 'password': '123'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 401)

    def test_register_bad_request(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register_user_already_exist(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update(data)
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 400)

    def test_register(self):
        data = {'username': 'admin', 'password': 'admin'}
        response = self.client.post('/authentication/login/', data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.json()

        token.update({'username': 'user1', 'password': 'pwd1'})
        response = self.client.post('/authentication/register/', token, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            sorted(list(response.json().keys())),
            ['token', 'user_pk']
        )
class RegisterGuiTests(TestCase):
#Tests for the Register Form

    #Load up some data for easy access
    def setUp(self) -> None:
        self.username = 'epicTestUser'
        self.email = 'epicTestUser@gmail.com'
        self.first_name = 'Epic'
        self.last_name = 'Test User'

    #Testing the Get Access for the Register Form
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_page_access(self):
        response = self.client.get("/authentication/registergui/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')

    #Testing the Get Access for the Register Form
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_page_access_logged(self):
        usertest = User.objects.create_user(username='testuser')
        usertest.set_password('ganma231')
        usertest.save()
        login = self.client.force_login(usertest)

        response = self.client.get("/authentication/registergui/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.url).path, "/")
        self.client.logout()

    #Testing a post request with an invalid password
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_register_form_bad_pass(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : self.email,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : '123',
            'password2' : '123'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request with no username given
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
    def test_register_form_no_user(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : '',
            'email' : self.email,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : '123',
            'password2' : '123'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')

    #Testing a succesful post request
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : self.email,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : 'ganma421',
            'password2' : 'ganma421'
        })
        #When the form is properly fulfilled it will redirect the users towards the page that ask checking their email
        self.assertEqual(response.status_code, 302)
        
        #We check if the user has been registered to the database
        user = User.objects.get(username=self.username)
        #We use asserts different to the username and check if they correspond to what we have registered with the post request
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.first_name, self.first_name)

    #Testing a post request with bad pass confirmation (not the same password1 that password2)
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_bad_pass_confirmation(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : self.email,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : 'ganma421',
            'password2' : 'ganma422'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request with empty mail
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_no_email(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : '',
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : 'ganma421',
            'password2' : 'ganma421'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request with bad email format
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_bad_email(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : 'email$dominio.net',
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : 'ganma421',
            'password2' : 'ganma421'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request with empty passwords
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_no_passwords(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : 'email$dominio.net',
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : '',
            'password2' : ''
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request without password confirmation
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_no_pass_confirmation(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : self.email,
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : 'ganma421',
            'password2' : ''
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request with bad first_name characters length
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_bad_firstname_length(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : self.email,
            'first_name': 'TESTNAMETESTNAMETESTNAMETESTNAMETESTNAME',
            'last_name' : self.last_name,
            'password1' : 'ganma421',
            'password2' : 'ganma421'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request with bad lastname characters length
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_bad_lastname_length(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : self.email,
            'first_name': self.first_name,
            'last_name' : 'TESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAMETESTNAME',
            'password1' : 'ganma421',
            'password2' : 'ganma421'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

    #Testing a post request with bad email characters length
    @override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage') 
    def test_register_form_bad_email_length(self):
        response = self.client.post("/authentication/registergui/", data={
            'username' : self.username,
            'email' : 'TESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAILTESTEMAIL@gmail.com',
            'first_name': self.first_name,
            'last_name' : self.last_name,
            'password1' : 'ganma421',
            'password2' : 'ganma421'
        })
        #The form returns the user to the form in case of a failure
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'register.html')
        
        #Checking that the user hasn't been created
        self.assertFalse(User.objects.filter(username=self.username).exists())

class ProfileModelTest(TestCase):
    #Test for the Profile model
    def setUp(self):
        super().setUp()
    
    def tearDown(self):
        super().tearDown()


    def test_create_and_delete_profile(self):
        #El modelo Profile se crea junto al usuario debido al metodo "update_user_profile" presente en models.py
        #Es una relación one-to-one, basicamente uno extiende del otro
        usertest = User(username="testnewuser", password="ganma231", first_name= "TestNew", last_name= "User", email="TestUser@gmail.com")
        usertest.save()

        dbuser = User.objects.get(username = "testnewuser")
        #Comprobamos si se ha añadido uno de los campos correctamente
        self.assertEqual(dbuser.email , usertest.email)
        #Comprobamos el campo de Email Confirmed que es exclusivo de Profile
        self.assertEqual(dbuser.profile.email_confirmed, False)

        prof = Profile.objects.get(user = usertest)
        #Comprobamos si existe un modelo Profile en el usuario
        self.assertTrue(Profile.objects.filter(user = dbuser).exists())
        us = User.objects.get(username = "testnewuser")
        #Borramos el Profile del usuario
        prof.delete()
        #Comprobamos si se ha borrado el Profile del usuario correctamente
        self.assertFalse(Profile.objects.filter(user = dbuser).exists())
        us.delete()

    def test_profile_tostring(self):
        usertest = User(username="testnewuser", password="ganma231", first_name= "TestNew", last_name= "User", email="TestUser@gmail.com")
        usertest.save()

        dbuser = User.objects.get(username = "testnewuser")
        #Probamos los strings de profile
        self.assertEqual(str(dbuser.email), "TestUser@gmail.com")
        self.assertEqual(str(dbuser.first_name), "TestNew")
        self.assertEqual(str(dbuser.last_name), "User")
        self.assertEqual(str(dbuser.profile.email_confirmed), "False")

        prof = Profile.objects.get(user = usertest)
        us = User.objects.get(username = "testnewuser")
        prof.delete()
        us.delete()

