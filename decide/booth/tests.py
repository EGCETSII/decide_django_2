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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from .models import PeticionCenso

from django.urls import reverse
from voting.models import Voting
from voting.serializers import VotingSerializer
from .views import BoothView


# Create your tests here.
class PeticionTestCase(BaseTestCase):

    def setUp(self):
      
        self.p = PeticionCenso(id=1, desc="Votacion 1", user_id=1)
        self.p.save()
        super().setUp()
    
    def tearDown(self):
        super().tearDown()
        self.p = None

    def test_peticion_exists(self):
        p = PeticionCenso.objects.get(id=1)
        self.assertEquals(p.desc, "Votacion 1")
        self.assertEquals(p.user_id, 1)

    def test_peticion_notExists(self):
        p = PeticionCenso.objects.get(id=1)
        self.assertNotEquals(p.desc, "Votacion 2")
        self.assertNotEquals(p.user_id, 2)

    def test_peticion_toString(self):
        p = PeticionCenso.objects.get(id=1)
        self.assertEquals(str(p), "Votacion 1")
    
    def test_bad_form_peticion(self):
        self.login(user='admin', password='qwerty')
        data = {'desc': ''}
        peticiones = PeticionCenso.objects.all().count()
        response = self.client.post('/booth/peticionCenso/', data, follow=True)
        self.assertEqual(response.status_code, 200)
        peticionesDespues = PeticionCenso.objects.all().count()
        self.assertEqual(peticionesDespues, peticiones)

        
'''class VotingTestCase(BaseTestCase):
  
    def test_get_votings(self, mocker):
        expected_results = [Voting(
            voting_id=4,
            name="EGC",
            desc="Aprobar EGC no es fácil",
            question(
                yesorno="¿Vamos a aprobar EGC?",
                options(
                    y="Yes",
                    n="No")),
            start_date="2021-01-08T15:29:52.040435",
            end_date=None,
            url="http://localhost:8000/booth/4",
            pubkey="a1s2d3f4g5h6j7k8l9",
            voted=False
            )]
    qs = MockSet(expected_results[0])
    mocker.patch.object(Voting.objects, 'get_queryset', return_value=qs)

    result = list(Voting.objects.get_id(4))

    assert result == expected_results
    assert str(result[0]) == expected_results[0].code
    
    def test_get_votings_fail(self, mocker):
        expected_results = [Voting(
            voting_id=4,
            name="PGPI",
            desc="Aprobar PGPI no es fácil",
            question(
                yesorno="¿Vamos a aprobar PGPI?",
                options(
                    y="Yes",
                    n="No")),
            start_date="2021-01-08T15:29:52.040435",
            end_date=None,
            url="http://localhost:8000/booth/4",
            pubkey="a1s2d3f4g5h3j7k8l9",
            voted=False
            )]

        qs = MockSet(expected_results[0])
        mocker.patch.object(Voting.objects, 'get_queryset', return_value=qs)

        result = list(Voting.objects.get_id(4))

        assert result != expected_results
        assert str(result[0]) != expected_results[0].code

    
    def test_expected_serialized_json(self):
        expected_results = {
            "voting_id": 4,
            "name": "EGC",
            "desc": "Aprobar EGC no es fácil",
            "question": {
                "yesorno": "¿Vamos a aprobar EGC?",
                "options": {
                    "y": "Yes",
                    "n": "No"}},
            "start_date":"2021-01-08T15:29:52.040435",
            "end_date":None,
            "url":"http://localhost:8000/booth/4",
            "pub-key": "a1s2d3f4g5h6j7k8l9",
            "voted": False
            }
        voting = Voting(**expected_results)
        results = VotingSerializer(voting).data
    
        assert results == expected_results
    

    def test_raise_error_when_missing_required_field(self):
        incomplete_data = {
            "voting_id": 4,
            "desc": "Aprobar EGC no es fácil",
            "question": {
                "yesorno": "¿Vamos a aprobar EGC?",
                "options": {
                    "y": "Yes",
                    "n": "No"}},
            "start_date":"2021-01-08T15:29:52.040435",
            "end_date":None,
            "pub-key": "a1s2d3f4g5h6j7k8l9",
            "voted": False
            }

        serializer = VotingSerializer(data=incomplete_data)

        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)    

            
    def test_list(self, rf, mocker):
        url = self.client.get('/booth/', follow=True) 
        request = rf.get(url)

        queryset = MockSet(
                Voting(
                    voting_id=4,
                    name="EGC",
                    desc="Aprobar EGC no es fácil",
                    question(
                        yesorno="¿Vamos a aprobar EGC?",
                        options(
                            y="Yes",
                            n="No")),
                    start_date="2021-01-08T15:29:52.040435",
                    end_date=None,
                    url="http://localhost:8000/booth/4",
                    pubkey="a1s2d3f4g5h6j7k8l9",
                    voted=False
                    )
                )

        mocker.patch.object(BoothView, 'get_queryset', return_value=queryset)
        response = BoothView.as_view({'get': 'list'})(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 1'''

# ..................................Test de Interfaz............................................


class InterfazLogin(StaticLiveServerTestCase):

    def setUp(self):
        # Load base test functionality for decide
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
        
    '''def test_call_view_votings_authenticated(self):
        response = self.client.get('/booth/', follow=True) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booth/booth.html')

    def test_call_view_voted_authenticated(self):
        response = self.client.get(reverse('hasVotado')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booth/hasVotado.html')  '''
    
    def test_wrongPassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("ale")
        self.driver.find_element_by_id('id_password2').send_keys("ale")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.\')]")

    def test_wrongExistingUser(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("passtest")
        self.driver.find_element_by_id('id_password2').send_keys("passtest")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Ya existe un usuario con ese nombre.\')]")

    def test_wrongConfirmPassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("alegonmar")
        self.driver.find_element_by_id('id_password2').send_keys("alegonmar2")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Los dos campos de contraseña no coinciden.\')]")

    def test_wrongCommonPassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("123456789")
        self.driver.find_element_by_id('id_password2').send_keys("123456789")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Esta contraseña es demasiado común.\')]")

    def test_wrongSimilarUsernamePassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("alejandrogm")
        self.driver.find_element_by_id('id_password2').send_keys("alejandrogm")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'La contraseña es demasiado similar a la de nombre de usuario.\')]")

    def test_correctRegister(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("passtest")
        self.driver.find_element_by_id('id_password2').send_keys("passtest")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url, f'{self.live_server_url}/booth/login/')
        self.driver.find_element_by_name('username').send_keys("Alejandrogm1")
        self.driver.find_element_by_name('password').send_keys("passtest")
        self.driver.find_element_by_css_selector('.btn').click()

