from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver


class AuthenticationTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.browser = WebDriver(options=options)
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_index_works(self):
        self.browser.get(self.live_server_url)

        self.assertIn('aoe2map', self.browser.title)

    def test_login(self):
        self.create_test_user('hscmi', 'password')
        self.browser.get(self.live_server_url + reverse('login'))

        username = self.browser.find_element(By.ID, 'username')
        password = self.browser.find_element(By.ID, 'password')
        loginbutton = self.browser.find_element(By.ID, 'login')

        username.send_keys("hscmi")
        password.send_keys("password")

        loginbutton.click()

        self.assertIn('My Maps', self.browser.page_source)

    @staticmethod
    def create_test_user(username, password):
        testuser = User()
        testuser.username = username
        testuser.password = make_password(password)
        testuser.save()
