from django.test import TestCase
from django.urls import resolve

from mapsapp.views import index


class HomePageTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)


