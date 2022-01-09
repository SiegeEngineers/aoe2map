from django.urls import reverse

from mapsapp.models import Collection
from mapsapp.tests.aoe2maptest import AbstractAoe2mapTest


class HomePageTest(AbstractAoe2mapTest):

    def test_rms_id_calculation(self):
        rms = self.create_sample_map(name='Sample Map', authors='Test Author')
        assert str(rms.uuid).startswith(rms.id)

    def test_collection_id_calculation(self):
        collection = Collection()
        collection.name = 'My Collection'
        collection.authors = 'Some Authors'
        collection.owner = self.aUser
        collection.save()
        assert str(collection.uuid).startswith(collection.id)
