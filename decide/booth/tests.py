from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

from base.tests import BaseTestCase

class InterfaceBoothTestCase(StaticLiveServerTestCase):


    def setUp(self):
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.FirefoxOptions()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

        super().setUp()

    def tearDown(self):
        super().tearDown()
        self.base.tearDown()
        self.driver.quit()

    def test_wrongPassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("ale")
        self.driver.find_element_by_id('id_password2').send_keys("ale")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.\')]")

    def test_wrongExistingUser(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("passtest")
        self.driver.find_element_by_id('id_password2').send_keys("passtest")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Ya existe un usuario con ese nombre.\')]")

    def test_wrongConfirmPassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("alegonmar")
        self.driver.find_element_by_id('id_password2').send_keys("alegonmar2")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Los dos campos de contraseña no coinciden.\')]")

    def test_wrongCommonPassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("123456789")
        self.driver.find_element_by_id('id_password2').send_keys("123456789")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'Esta contraseña es demasiado común.\')]")

    def test_wrongSimilarUsernamePassword(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("alejandrogm")
        self.driver.find_element_by_id('id_password2').send_keys("alejandrogm")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/register/')
        self.driver.find_elements(By.XPATH, "//p[contains(.,\'La contraseña es demasiado similar a la de nombre de usuario.\')]")

    def test_correctRegister(self):
        self.driver.get(f'{self.live_server_url}/booth/register')
        self.driver.find_element_by_id('id_username').send_keys("Alejandrogm1")
        self.driver.find_element_by_id('id_email').send_keys("alejandrogm@gmail.com")
        self.driver.find_element_by_id('id_password1').send_keys("passtest")
        self.driver.find_element_by_id('id_password2').send_keys("passtest")
        self.driver.find_element_by_css_selector('.botonLogin').click()
        self.assertEquals(self.driver.current_url,f'{self.live_server_url}/booth/login/')
        self.driver.find_element_by_name('username').send_keys("Alejandrogm1")
        self.driver.find_element_by_name('password').send_keys("passtest")
        self.driver.find_element_by_css_selector('.btn').click()