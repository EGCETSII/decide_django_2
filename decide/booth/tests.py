from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


from base import mods
from base.tests import BaseTestCase
from census.models import Census
from .models import PeticionCenso

# Create your tests here.
class PeticionTestCase(BaseTestCase):
    def setUp(self):
      
        self.p = PeticionCenso(id=1,desc="Votacion 1", user_id=1)
        self.p.save()
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
        self.p = None

    def test_peticion_exists(self):
        p = PeticionCenso.objects.get(id=1)
        self.assertEquals(p.desc,"Votacion 1")
        self.assertEquals(p.user_id,1)

    def test_peticion_notExists(self):
        p = PeticionCenso.objects.get(id=1)
        self.assertNotEquals(p.desc,"Votacion 2")
        self.assertNotEquals(p.user_id,2)

    def test_peticion_toString(self):
        p = PeticionCenso.objects.get(id=1)
        self.assertEquals(str(p),"Votacion 1")
    
    def test_bad_form_peticion(self):
        self.login(user='admin', password='qwerty')
        data = {'desc': ''}
        peticiones = PeticionCenso.objects.all().count()
        response = self.client.post('/booth/peticionCenso/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        peticionesDespues = PeticionCenso.objects.all().count()
        self.assertEqual(peticionesDespues, peticiones)

#..................................Test de Interfaz............................................

class InterfazLogin(StaticLiveServerTestCase):
    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_login_success(self):
        self.driver.get(f'{self.live_server_url}/booth/login/')
        self.driver.find_element(By.CSS_SELECTOR, ".container > .d-flex").click()
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys("qwerty")
        self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/')

    def test_login_wrong(self):
        self.driver.get(f'{self.live_server_url}/booth/login/')
        self.driver.find_element(By.CSS_SELECTOR, ".container > .d-flex").click()
        self.driver.find_element(By.NAME, "username").send_keys("admin")
        self.driver.find_element(By.NAME, "password").send_keys("no es la contraseña")
        self.driver.find_element(By.NAME, "password").send_keys(Keys.ENTER)
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/login/')