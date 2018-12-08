import itertools
import os
from time import sleep

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings, Client
from django.urls import resolve, reverse
from django.utils.encoding import smart_text
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver

from mapsapp.models import VersionTag, Rms, Tag
from mapsapp.views import index


class HomePageTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)


class ChangelogTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.aTag = Tag.objects.create(name='tag-name')
        cls.aVersion = VersionTag.objects.create(name='version-name')
        cls.aUser = User.objects.create_user(username='username', password='password')
        cls.counter = itertools.count()

    def test_single_map_has_no_changelog(self):
        rms = self.create_sample_map()
        self.assertIn('map-name', rms.name)

        self.assert_map_does_not_have_changelog(rms)

    def test_single_map_with_changelog_text_has_changelog(self):
        rms = self.create_sample_map(changelog='changelog')
        self.assertIn('map-name', rms.name)
        self.assertEqual('changelog', rms.changelog)

        self.assert_map_has_changelog(rms)

    def test_three_maps_all_have_changelog(self):
        rms1 = self.create_sample_map()
        rms2 = self.create_sample_map(newer_version=rms1)
        rms3 = self.create_sample_map(newer_version=rms2)
        self.assertIn('map-name', rms1.name)
        self.assertIn('map-name', rms2.name)
        self.assertIn('map-name', rms3.name)

        self.assert_map_has_changelog(rms1)
        self.assert_map_has_changelog(rms2)
        self.assert_map_has_changelog(rms3)

    def test_three_maps_with_changelog_text_all_have_changelog(self):
        rms1 = self.create_sample_map(changelog='changelog')
        rms2 = self.create_sample_map(newer_version=rms1, changelog='changelog')
        rms3 = self.create_sample_map(newer_version=rms2, changelog='changelog')
        self.assertIn('map-name', rms1.name)
        self.assertIn('map-name', rms2.name)
        self.assertIn('map-name', rms3.name)

        self.assert_map_has_changelog(rms1)
        self.assert_map_has_changelog(rms2)
        self.assert_map_has_changelog(rms3)

    def test_new_version_link_from_third_map_leads_to_first_map(self):
        rms1 = self.create_sample_map()
        rms2 = self.create_sample_map(newer_version=rms1)
        rms3 = self.create_sample_map(newer_version=rms2)
        self.assertIn('map-name', rms1.name)
        self.assertIn('map-name', rms2.name)
        self.assertIn('map-name', rms3.name)

        c = Client()
        response = c.get(reverse('map', kwargs={'rms_id': rms3.uuid}))
        self.assertEquals(rms3.newer_version, rms2)
        self.assertIn('A newer version of this map is available!', smart_text(response.content))
        self.assertIn('<a href="/map/{uuid}" class="alert-link">Check it out!</a>'.format(uuid=rms1.uuid),
                      smart_text(response.content))

    def create_sample_map(self, changelog='', newer_version=None):
        rms = Rms()
        rms.owner = self.aUser
        rms.name = "map-name-{}".format(next(self.counter))
        rms.changelog = changelog
        rms.authors = 'rms-authors'
        rms.description = 'rms-description'
        rms.file = SimpleUploadedFile('file-name', b'file-contents')
        rms.newer_version = newer_version
        rms.save()
        rms.tags.add(self.aTag)
        rms.versiontags.add(self.aVersion)
        rms.save()
        return rms

    def assert_map_has_changelog(self, rms):
        response = self.client.get(reverse('map', kwargs={'rms_id': rms.uuid}))
        self.assertIn(b'Changelog', response.content)

    def assert_map_does_not_have_changelog(self, rms):
        response = self.client.get(reverse('map', kwargs={'rms_id': rms.uuid}))
        self.assertNotIn(b'Changelog', response.content)


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

        username = self.browser.find_element_by_id('username')
        password = self.browser.find_element_by_id('password')
        loginbutton = self.browser.find_element_by_id('login')

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


@override_settings(DEBUG=True)
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
            'id_password2': "password"
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
            'id_file': os.path.abspath("mapsapp/testdata/relic_nothing.rms"),
            'id_name': 'Map Name',
            'id_version': 'Map Version',
            'id_authors': 'Map Authors',
            'id_description': 'Map Description',
            'id_information': 'Map Information',
            'id_changelog': 'Changelog Information',
            'id_url': 'map_url',
            'id_tags': 'map,tags',
            'id_images': os.path.abspath("mapsapp/testdata/relic_nothing.png")
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

        self.browser.get(self.live_server_url + reverse('map', kwargs={'rms_id': new_map_uuid}))
        self.assertIn('Changelog Information', self.browser.page_source)

        # 011_open_create_collection_page

        self.click_page_link('user-nav-new-collection', 'Create Collection')

        # 012_create_new_collection

        self.fill_fields({
            'id_name': 'Collection Name',
            'id_authors': 'Collection Authors',
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
        sleep(1)
        self.assertIn('Map Name', self.browser.page_source)

        # 099_logout

        logout = self.browser.find_element_by_id('user-nav-logout')

        logout.click()

        self.assertLoggedOut()

    def get_new_map_uuid(self):
        href = self.browser.find_element_by_class_name('a-goto-created-map').get_attribute('href')
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
        button = self.browser.find_element_by_id(element_id)
        button.click()

    def fill_fields(self, content):
        for key, value in content.items():
            self.fill_field(key, value)

    def fill_field(self, element_id, content):
        field = self.browser.find_element_by_id(element_id)
        field.send_keys(content)

    def click_page_link(self, element_id, content):
        link = self.browser.find_element_by_id(element_id)
        self.scroll_to(link)
        link.click()
        self.assertIn(content, self.browser.page_source)

    def click_page_link_text(self, link_text, content):
        link = self.browser.find_element_by_partial_link_text(link_text)
        self.scroll_to(link)
        link.click()
        self.assertIn(content, self.browser.page_source)

    def scroll_to(self, link):
        self.browser.execute_script("arguments[0].scrollIntoView();", link)

    def assertLoggedIn(self):
        self.browser.find_element_by_id('user-nav-username')

    def assertLoggedOut(self):
        self.assertNotIn('user-nav-username', self.browser.page_source)
