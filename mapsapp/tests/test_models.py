from django.urls import reverse

from mapsapp.tests.aoe2maptest import AbstractAoe2mapTest


class HomePageTest(AbstractAoe2mapTest):

    def test_rms_id_calculation(self):
        rms = self.create_sample_map(name='Sample Map', authors='Test Author')
        assert str(rms.uuid).startswith(rms.id)
