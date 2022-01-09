from django.urls import resolve, reverse

from mapsapp.tests.aoe2maptest import AbstractAoe2mapTest
from mapsapp.views import index


class HomePageTest(AbstractAoe2mapTest):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_map_url(self):
        rms = self.create_sample_map(name='Sample Map', authors='Test Author')
        response = self.client.get(reverse('map_uuid', kwargs={'rms_id': rms.uuid}))
        assert response.status_code == 302
        assert response.url == f'/map/{rms.id}/sample-map'
