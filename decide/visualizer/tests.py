from django.test import TestCase

import unittest, time, re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException



class TestEmail():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def test_email(self):
    self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
    self.driver.find_element_by_id('id_username').send_keys("admin")
    self.driver.find_element_by_id('id_password').send_keys("picarodecide")
    self.driver.find_element_by_id('login-form').click()
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1552, 840)
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary:nth-child(2)").click()
    self.driver.find_element(By.NAME, "name").click()
    self.driver.find_element(By.NAME, "name").send_keys("test test")
    self.driver.find_element(By.NAME, "subject").click()
    self.driver.find_element(By.NAME, "subject").send_keys("test")
    self.driver.find_element(By.NAME, "mail").click()
    self.driver.find_element(By.NAME, "mail").send_keys("test@gmail.com")
    self.driver.find_element(By.NAME, "Comment").click()
    self.driver.find_element(By.NAME, "Comment").send_keys("test")
    self.driver.find_element(By.CSS_SELECTOR, ".inputBox:nth-child(5) > input").click()

class TestTraduccionFrances():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def test_traduccionFrances(self):
    self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
    self.driver.find_element_by_id('id_username').send_keys("admin")
    self.driver.find_element_by_id('id_password').send_keys("picarodecide")
    self.driver.find_element_by_id('login-form').click()
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1552, 840)
    element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(3) img").click()
    assert self.driver.find_element(By.ID, "text").text == "Résultats"

class TestTraduccionContactUs():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def test_traduccionContactUs(self):
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1552, 840)
    element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(3) img").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary:nth-child(2)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".contactForm > h2").text == "Envoyer en méssage"

class TestQuestion():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def test_question(self):
    self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
    self.driver.find_element_by_id('id_username').send_keys("admin")
    self.driver.find_element_by_id('id_password').send_keys("picarodecide")
    self.driver.find_element_by_id('login-form').click()
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1552, 840)
    elements = self.driver.find_elements(By.ID, "question")
    assert len(elements) > 0

class TestMaps():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def test_maps(self):
    self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
    self.driver.find_element_by_id('id_username').send_keys("admin")
    self.driver.find_element_by_id('id_password').send_keys("picarodecide")
    self.driver.find_element_by_id('login-form').click()
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1552, 840)
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary:nth-child(2)").click()
    elements = self.driver.find_elements(By.CSS_SELECTOR, "a > img")
    assert len(elements) > 0
  
class TestContactUs():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_contactUs(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary:nth-child(2)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > h2").text == "Contact Info"

    def tearDown(self):
        self.driver.quit()

class TestContactUsBack():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_contactUsBack(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary:nth-child(2)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "div:nth-child(1) > h2").text == "Contact Info"
        self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
        assert self.driver.find_element(By.ID, "saveAsPNG1").text == "Save as PNG"

    def tearDown(self):
        self.driver.quit()

class TestDarkMode():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_darkMode(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        self.driver.find_element(By.ID, "darkButton").click()
        assert self.driver.find_element_by_tag_name('body').get_attribute("class") == "bg-dark"
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        assert self.driver.find_element(By.ID, "lightButton").text == "Light mode" 

    def tearDown(self):
        self.driver.quit()

class TestLightMode():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_lightMode(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        self.driver.find_element(By.ID, "darkButton").click()
        self.driver.find_element(By.ID, "lightButton").click()
        assert self.driver.find_element_by_tag_name('body').get_attribute("class") == "bg-light"
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        assert self.driver.find_element(By.ID, "darkButton").text == "Dark mode" 

    def tearDown(self):
        self.driver.quit()
        
class TestTraduccionEspanyol():
    def setup(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_traduccionEspanyol(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) img").click()
        assert self.driver.find_element(By.ID, "text").text == "Resultados"

    def teardown(self):
        self.driver.quit()
        
class TestTraduccionIngles():
    def setup(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_traduccionIngles(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) img").click()
        assert self.driver.find_element(By.ID, "text").text == "Resultados"
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        assert self.driver.find_element(By.ID, "text").text == "Results"

    def teardown(self):
        self.driver.quit()

class TestAboutUs():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_aboutUs(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-group > .btn:nth-child(3)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(2) > .card-title").text == "Abraham"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(3) > .card-title").text == "Martín Arturo"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(4) > .card-title").text == "Gabriel"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(5) > .card-title").text == "Thibaut"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(6) > .card-title").text == "David"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(1) > .card-title").text == "Pablo"

    def tearDown(self):
        self.driver.quit()

class TestAboutUsBack():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_aboutUsBack(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-group > .btn:nth-child(3)").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(2) > .card-title").text == "Abraham"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(3) > .card-title").text == "Martín Arturo"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(4) > .card-title").text == "Gabriel"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(5) > .card-title").text == "Thibaut"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(6) > .card-title").text == "David"
        assert self.driver.find_element(By.CSS_SELECTOR, ".columna:nth-child(1) > .card-title").text == "Pablo"
        self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
        assert self.driver.find_element(By.ID, "saveAsPNG1").text == "Save as PNG"

    def tearDown(self):
        self.driver.quit()

class TestPNG1PNG2PDF():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
 
    def testPNG1PNG2PDF(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        #self.driver.find_element(By.CSS_SELECTOR, "#saveAsPDF").click()
        assert self.driver.find_element(By.ID, "saveAsPNG1").text == "Save as PNG"
        assert self.driver.find_element(By.ID, "saveAsPNG2").text == "Save as PNG"
        assert self.driver.find_element(By.ID, "saveAsPDF").text == "Save as PDF"
    def tearDown(self):
        self.driver.quit()

class TestDarkModeCookies():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_darkModeCookies(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        self.driver.find_element(By.ID, "darkButton").click()
        assert self.driver.find_element_by_tag_name('body').get_attribute("class") == "bg-dark"
        assert self.driver.find_element(By.ID, "lightButton").text == "Light mode" 
        self.driver.find_element(By.CSS_SELECTOR, ".btn-group > .btn:nth-child(3)").click()
        assert self.driver.find_element_by_tag_name('body').get_attribute("class") == "bg-dark"

    def tearDown(self):
        self.driver.quit()

class TestLightModeCookies():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        
    def test_lightModeCookies(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        self.driver.find_element(By.ID, "darkButton").click()
        assert self.driver.find_element_by_tag_name('body').get_attribute("class") == "bg-dark"
        assert self.driver.find_element(By.ID, "lightButton").text == "Light mode"
        self.driver.find_element(By.ID, "lightButton").click()
        assert self.driver.find_element_by_tag_name('body').get_attribute("class") == "bg-light"
        assert self.driver.find_element(By.ID, "darkButton").text == "Dark mode" 
        self.driver.find_element(By.CSS_SELECTOR, ".btn-group > .btn:nth-child(3)").click()
        #Si esta en modo claro, al ser el modo por defecto, el backgraund es blanco, sin la necesidad de aplicar ningún cambio de CSS.
        assert self.driver.find_element_by_tag_name('body').get_attribute("class") == ""

    def tearDown(self):
        self.driver.quit()

class TestGraficaBarras():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        
    def test_graficaBarras(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        assert self.driver.find_element(By.CSS_SELECTOR, "th:nth-child(2) > .heading").text == "Bar Chart"
        #Sacamos una captura de pantalla de la gráfica de barras para comprobar que esta existe, dentro de la imagen screenshotgraficabarras.png aparece esta gráfica, solo que aparece algo distosionada
        #las barras miden 1/5 menos de lo que miden en realidad, pero podemos comprobar que existe la gráfica y que tiene el número correcto de opciones.
        self.driver.find_element_by_id('myChart2').screenshot('screenshotgraficabarras.png')
        
    def tearDown(self):
        self.driver.quit()

class TestPodium():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
    
    def test_podium(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > .pmd-floating-action-btn > img").click()
        assert self.driver.find_element(By.CSS_SELECTOR, ".podio:nth-child(2) > #winner").text == "WINNER"
        assert self.driver.find_element(By.ID, "winner").text == "2nd place"
        assert self.driver.find_element(By.CSS_SELECTOR, ".podio:nth-child(3) > #winner").text == "3rd place"
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.driver.quit()

class TestTraduccionAleman():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def test_traduccionAleman(self):
    self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
    self.driver.find_element_by_id('id_username').send_keys("admin")
    self.driver.find_element_by_id('id_password').send_keys("picarodecide")
    self.driver.find_element_by_id('login-form').click()
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1552, 840)
    element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(4) img").click()
    assert self.driver.find_element(By.ID, "text").text == "Ergebnisse"

class TestPodiumTraduccionEspanol():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def test_podiumTraduccionEspañol(self):
    self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
    self.driver.find_element_by_id('id_username').send_keys("admin")
    self.driver.find_element_by_id('id_password').send_keys("picarodecide")
    self.driver.find_element_by_id('login-form').click()
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1552, 840)
    element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) img").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".podio:nth-child(2) > #winner").text == "GANADOR"
    assert self.driver.find_element(By.ID, "winner").text == "2º puesto"
    assert self.driver.find_element(By.CSS_SELECTOR, ".podio:nth-child(3) > #winner").text == "3º puesto"
    
    
class TestGraficaDonut():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        
    def test_graficaDonut(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) img").click()
        #Aquí se comprueba que se encuentra la gráfica circular
        assert self.driver.find_element(By.CSS_SELECTOR, "section > #table th:nth-child(1) > .heading").text == "Gráfico Circular"
        elements = self.driver.find_elements(By.ID, "myChart")
        assert len(elements) > 0

    def tearDown(self):
        self.driver.quit()


class TestTablaResultados():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        
    def test_graficaDonut(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) img").click()
        assert self.driver.find_element(By.CLASS_NAME, "theTable")
        assert self.driver.find_element(By.ID, "exportarTab")
        #Aquí se comprueba que aparecen los resultados de la votación (se comprueba que aparecen 2 opciones de la votación
        #se supone que una votación tiene al menos 2 opciones)
        opcion1 = self.driver.find_elements(By.CSS_SELECTOR, "tbody > tr:nth-child(1) > th")
        assert len(opcion1) > 0
        opcion2 = self.driver.find_elements(By.CSS_SELECTOR, "tbody > tr:nth-child(1) > th")
        assert len(opcion2) > 0
        

    def tearDown(self):
        self.driver.quit()


class TestBotonReturn():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        
    def test_graficaDonut(self):
        #Aqui se comprueba que si le das al botón return vuelve a la página anterior
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/contactUs")
        assert self.driver.current_url == "https://picaro-decide.herokuapp.com/visualizer/contactUs/"
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
        assert self.driver.current_url == "https://picaro-decide.herokuapp.com/visualizer/5/"
        self.driver.find_element(By.CSS_SELECTOR, "#app-visualizer > .btn").click()
        assert self.driver.current_url == "https://picaro-decide.herokuapp.com/visualizer/contactUs/"
        

    def tearDown(self):
        self.driver.quit()


class TestVotacionNoEmpezada():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        
    def test_graficaDonut(self):
        
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/6/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) img").click()
        #Comprueba que efectivamente es una votación que no ha empezado, ya que la página de visualización de una votación no empezada, solo contiene ese texto
        assert self.driver.find_element(By.ID, "text").text == "Votación no comenzada"
        

    def tearDown(self):
        self.driver.quit()


class TestVotacionNoFinalizada():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
        
    def test_votacionEnCurso(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/7/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) img").click()
        #Comprueba que efectivamente es una votación que no ha empezado, ya que la página de visualización de una votación no empezada, solo contiene ese texto
        assert self.driver.find_element(By.ID, "text").text == "Votación en curso"

    def test_tabla(self):
        
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/7/")
        element = self.driver.find_element(By.CSS_SELECTOR, ".fa-language")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) img").click()
        #Aquí se comprueba que la tabla con el número de votos existe y tiene la fila con el número de votos que hay
        elements = self.driver.find_elements(By.CSS_SELECTOR, "tbody > tr > th")
        assert len(elements) > 0

    def tearDown(self):
        self.driver.quit()


#class TestNumeroVotos():
#    def setUp(self):
#        self.driver = webdriver.Chrome()
#        
#    def test_aumentaNumeroVotos(self):
#        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
#        self.driver.find_element_by_id('id_username').send_keys("admin")
#        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
#        self.driver.find_element_by_id('login-form').click()
#        self.driver.get("https://picaro-decide.herokuapp.com/admin")
#        
#        time.sleep(5)
#        
#       
#        self.driver.find_element(By.ID, "id_voting_id").send_keys("7")
#        self.driver.find_element(By.ID, "id_voter_id").send_keys("1")
#        self.driver.find_element(By.ID, "id_a").send_keys("1")
#        self.driver.find_element(By.ID, "id_b").send_keys("1")
#        self.driver.find_element(By.NAME, "_addanother").click()
#        self.driver.find_element(By.ID, "id_voting_id").send_keys("7")
#        self.driver.find_element(By.ID, "id_voter_id").send_keys("2")
#        self.driver.find_element(By.ID, "id_a").send_keys("1")
#        self.driver.find_element(By.ID, "id_b").send_keys("3")
#        self.driver.find_element(By.NAME, "_save").click()
#        self.driver.get("https://picaro-decide.herokuapp.com/visualizer/7/")
#        assert self.driver.find_element(By.CSS_SELECTOR, "tbody > tr > th").text =="4"

#    def tearDown(self):
#        self.driver.quit()
        

# if __name__ == '__main__':
#     unittest.main()

class TestTestBotonTelegram():
  def setup(self):
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    self.driver = webdriver.Chrome(options=options)
  
  def teardown(self):
    self.driver.quit()
  
  def testBotonTelegram(self):
    self.driver.get("https://picaro-decide.herokuapp.com/visualizer/5/")
    self.driver.set_window_size(1295, 726)
    self.driver.find_element(By.LINK_TEXT, "Telegram").click()
    assert self.driver.find_element(By.CSS_SELECTOR, "span").text == "decide"
""" Comentado porque estos cambios no estan todavia en heroku
class TestHomeVisualizer():
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.driver.fullscreen_window()
  
    def test_home_visualizer(self):
        self.driver.get("https://picaro-decide.herokuapp.com/admin/login/?next=/admin/")
        self.driver.find_element_by_id('id_username').send_keys("admin")
        self.driver.find_element_by_id('id_password').send_keys("picarodecide")
        self.driver.find_element_by_id('login-form').click()
        self.driver.get("https://picaro-decide.herokuapp.com/visualizer")
        try: self.assertEqual("Votings", self.driver.find_element_by_id("question").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
"""

# if __name__ == '__main__':
#     unittest.main()
