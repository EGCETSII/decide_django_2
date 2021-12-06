from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from base.tests import BaseTestCase

class visualizerTestCase(StaticLiveServerTestCase):

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
		
	def test_facebook(self):
		self.driver.get("https://egc-guadalquivir-vis.herokuapp.com/visualizer/2/")		
		self.driver.set_window_size(1298, 863)
		self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > img").click()
		assert self.driver.find_element(By.ID, "homelink").text == "Facebook"																							
    


# Create your tests here.
