from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys

import os
os.environ['DJANGO_LIVE_TEST_SERVER_ADDRESS'] = '0.0.0.0:8081'

DOCKER_TEST_SERVER_URL = 'http://192.168.99.100:8081'

class FunctionalTest(StaticLiveServerTestCase):
        
    @classmethod
    def setUpClass(cls):  #1
        print (sys.argv)
        for arg in sys.argv:  #2
            if 'liveserver' in arg:  #3
                cls.server_url = 'http://' + arg.split('=')[1]  #4
                print (cls.server_url)
                return  #5
        super().setUpClass()  #6
        cls.server_url = cls.live_server_url
        cls.server_url = DOCKER_TEST_SERVER_URL     
        print (cls.server_url)

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == DOCKER_TEST_SERVER_URL:
            super().tearDownClass()

    def setUp(self):
        # open firefox browser on selenium hub
        selenium_hub_url = 'http://192.168.99.100:4444/wd/hub'
        self.browser = webdriver.Remote(
                                   command_executor=selenium_hub_url,
                                   desired_capabilities={"browserName": "firefox"}
                                   )
        #self.django_url = 'http://192.168.99.100:8081'
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')