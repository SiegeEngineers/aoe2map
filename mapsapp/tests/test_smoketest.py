import os
import re
from time import sleep

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import override_settings
from django.urls import reverse, re_path
from django.views.static import serve
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from aoe2map import imagestorage
from aoe2map.urls import urlpatterns as base_patterns
from mapsapp.models import VersionTag

urlpatterns = base_patterns + [re_path(r'^{}(?P<path>.*)$'.format(re.escape(settings.IMAGE_URL.lstrip('/'))),
                                       serve, kwargs={'document_root': imagestorage.IMAGE_ROOT})]


@override_settings(ROOT_URLCONF=__name__)
class SmokeTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.headless = True
        cls.browser = WebDriver(options=options)
        cls.browser.implicitly_wait(10)

        versiontag = VersionTag()
        versiontag.name = "Version Tag"
        versiontag.save()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_smoke_test(self):
        script_file_path = os.path.dirname(os.path.realpath(__file__))
        # 000_index_works

        self.open_index_page()

        # 001_open_login_page

        self.click_page_link('nav-link-login', 'Login')

        # 002_open_registration_page

        self.click_page_link('a-register', 'Register')

        # 003_register_without_email

        self.fill_fields({
            'id_username': "hscmi",
            'id_password1': "password",
            'id_password2': "password",
            'id_daut': "DauT"
        })

        self.click_to_login('register')

        # 004_logout

        self.click_to_logout('user-nav-logout')

        # 005_open_login_page

        self.click_page_link('nav-link-login', 'Login')

        # 006_login

        self.fill_fields({
            'username': "hscmi",
            'password': "password",
        })
        self.click_to_login('login')

        # 007_open_new_map_page

        self.click_page_link('user-nav-new-map', 'New Map')

        # 008_create_new_map

        self.fill_fields({
            'id_file': os.path.join(script_file_path, 'testdata', 'relic_nothing.rms'),
            'id_name': 'Map Name',
            'id_version': 'Map Version',
            'id_authors': 'Map Authors',
            'id_description': 'Map Description',
            'id_information': 'Map Information',
            'id_changelog': 'Changelog Information',
            'id_url': 'map_url',
            'id_mod_id': '1337',
            'id_tags': 'map,tags',
            'id_images': os.path.join(script_file_path, 'testdata', 'relic_nothing.png')
        })
        self.click('id_versiontags_0')
        self.click_page_link('upload', 'Your Map has been created!')
        new_map_uuid = self.get_new_map_uuid()

        # 009_open_mymaps_page_and_find_map

        self.click_page_link('user-nav-my-maps', 'My Maps')
        self.assertIn('Map Name', self.browser.page_source)

        # 010_open_maps_page_and_find_map

        self.click_page_link('nav-link-maps', '<img src="/static/mapsapp/images/map.svg" style="height:1em;"> Maps')
        self.assertIn('Map Name', self.browser.page_source)

        # 0101_open_map_page_and_find_changelog

        self.browser.get(self.live_server_url + reverse('map_uuid', kwargs={'rms_id': new_map_uuid}))
        self.assertIn('Changelog Information', self.browser.page_source)
        self.assertIn('https://mods.aoe2.se/1337', self.browser.page_source)
        self.assertIn('<span class="votes">0</span>', self.browser.page_source)

        # 0102_press_the_heart
        self.click('vote-button')
        self.assertIn('<span class="votes">1</span>', self.browser.page_source)

        # 0103_press_the_heart_again
        self.click('vote-button')
        self.assertIn('<span class="votes">0</span>', self.browser.page_source)

        # 011_open_create_collection_page

        self.click_page_link('user-nav-new-collection', 'Create Collection')

        # 012_create_new_collection

        self.fill_fields({
            'id_name': 'Collection Name',
            'id_authors': 'Collection Authors',
            'id_mod_id': '42',
            'id_description': 'Collection Description',
            'id_rms': new_map_uuid
        })
        self.click_page_link('save', 'Collection created successfully')

        # 013_open_collections_page_and_find_collection

        self.click_page_link('nav-link-map-collections',
                             '<img src="/static/mapsapp/images/maps.svg" style="height:1.1em;"> Map Collections')
        self.assertIn('Collection Name', self.browser.page_source)

        # 014_open_collection_page_and_find_map

        self.click_page_link_text('Collection Name', 'Collection Description')
        self.assertIn('https://mods.aoe2.se/42', self.browser.page_source)
        sleep(1)
        self.assertIn('Map Name', self.browser.page_source)

        # 015_open_map

        self.click_page_link_text('Map Name', 'Upload new version')

        # 016_click_upload_new_version

        self.click_page_link_text('Upload new version', 'You are currently uploading a new version of')

        # 017_fill_fields

        self.fill_fields({
            'id_file': os.path.join(script_file_path, 'testdata', 'relic_nothing.rms'),
            'id_changelog': 'Changelog Information: New Version'
        })
        self.click('id_versiontags_0')
        self.click('id_images_to_copy_0')
        self.click_page_link('upload', 'Your Map has been created!')

        # 018_open_mymaps_page_and_find_map

        self.click_page_link('a-goto-created-map', 'Map Name')
        self.assertIn('Changelog Information: New Version', self.browser.page_source)
        self.assertIn('relic_nothing.png', self.browser.page_source)
        self.assertIn('https://mods.aoe2.se/1337', self.browser.page_source)

        # 099_logout

        logout = self.browser.find_element(By.ID, 'user-nav-logout')

        logout.click()

        self.assertLoggedOut()

    def get_new_map_uuid(self):
        href = self.browser.find_element(By.ID, 'a-goto-created-map').get_attribute('href')
        return href.split('/')[-1]

    def open_index_page(self):
        self.browser.get(self.live_server_url)
        self.assertIn('aoe2map', self.browser.title)

    def click_to_logout(self, element_id):
        self.click(element_id)
        self.assertLoggedOut()

    def click_to_login(self, element_id):
        self.click(element_id)
        self.assertLoggedIn()

    def click(self, element_id):
        button = self.browser.find_element(By.ID, element_id)
        button.click()

    def fill_fields(self, content):
        for key, value in content.items():
            self.fill_field(key, value)

    def fill_field(self, element_id, content):
        field = self.browser.find_element(By.ID, element_id)
        field.send_keys(content)

    def click_page_link(self, element_id, content):
        link = self.browser.find_element(By.ID, element_id)
        self.scroll_to(link)
        link.click()
        self.assertIn(content, self.browser.page_source)

    def click_page_link_text(self, link_text, content):
        link = self.browser.find_element(By.PARTIAL_LINK_TEXT, link_text)
        self.scroll_to(link)
        link.click()
        self.assertIn(content, self.browser.page_source)

    def scroll_to(self, link):
        self.browser.execute_script("arguments[0].scrollIntoView();", link)

    def assertLoggedIn(self):
        self.browser.find_element(By.ID, 'user-nav-username')

    def assertLoggedOut(self):
        self.assertNotIn('user-nav-username', self.browser.page_source)
