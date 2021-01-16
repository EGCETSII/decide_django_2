# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        options.headless = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get(f'{self.live_server_url}/')
        driver.find_element_by_id("welcome").click()
        self.assertEqual("Welcome to Decide, an online voting platform. This is the main page. Here, you can login to your account and press booth to vote or press visualizer to see the results.", driver.find_element_by_id("welcome").text)
        driver.find_element_by_xpath("//div[@id='app-decide']/nav/button/span").click()
        driver.find_element_by_id("es").click()
        driver.find_element_by_id("welcome").click()
        self.assertEqual(u"Bienvenido a Decide, una plataforma de votación online. Esta es la página principal. Aquí, puede iniciar sesión en su cuenta y presionar cabina para votar o presionar visualizador para ver los resultados.", driver.find_element_by_id("welcome").text)
        driver.find_element_by_id("en").click()
        driver.find_element_by_id("welcome").click()
        self.assertEqual("Welcome to Decide, an online voting platform. This is the main page. Here, you can login to your account and press booth to vote or press visualizer to see the results.", driver.find_element_by_id("welcome").text)
        driver.find_element_by_xpath("//div[@id='app-decide']/nav/button/span").click()
    
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
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
