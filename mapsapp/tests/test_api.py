import datetime
import itertools

import pytz
from django.test import Client
from django.urls import reverse

from mapsapp.tests.aoe2maptest import AbstractAoe2mapTest


class ApiTest(AbstractAoe2mapTest):

    def setUp(self):
        self.failures = []
        self.counter = itertools.count()

    def test_latest_rms(self):
        masking = self.prepare_sample_rms_entities()

        c = Client()
        response = c.get(reverse('api:latest_rms', kwargs={'amount': 3}))
        self.compareJsonWithValidationFile(response.json(), masking=masking)

    def test_latest_updated_rms(self):
        masking = self.prepare_sample_rms_entities()

        c = Client()
        response = c.get(reverse('api:latest_updated_rms', kwargs={'amount': 3}))
        self.compareJsonWithValidationFile(response.json(), masking=masking)

    def test_archived_rms(self):
        rms = self.create_sample_map()
        self.assertFalse(rms.archived)

        c = Client()

        response = c.get(reverse('api:latest_rms', kwargs={'amount': 1}))
        self.assertEquals(1, len(response.json()['maps']))

        rms.archived = True
        rms.save()

        response = c.get(reverse('api:latest_rms', kwargs={'amount': 1}))
        self.assertEquals(0, len(response.json()['maps']))

        response = c.get(reverse('api:rms', kwargs={'rms_id': rms.uuid}))
        self.assertEquals(1, len(response.json()['maps']))

    def test_rms_by_name(self):
        self.create_sample_map(name='Bamboo_Arabia', authors='T-West')
        self.create_sample_map(name='Bamboo Arabia', authors='T-West')
        self.create_sample_map(name='Bamboo', authors='T West')
        self.create_sample_map(name='Arabia', authors='Arabia')
        self.create_sample_map(name='Dark Forest', authors='Bamboo Arabia')

        c = Client()
        self.assert_rms_by_name_returns_number_of_maps(c, 'Bamboo Arabia', 3)
        self.assert_rms_by_name_returns_number_of_maps(c, 'Bamboo', 4)
        self.assert_rms_by_name_returns_number_of_maps(c, 'Arabia', 4)
        self.assert_rms_by_name_returns_number_of_maps(c, 'Arabia T-West', 2)
        self.assert_rms_by_name_returns_number_of_maps(c, 'T West Arabia', 2)

    def assert_rms_by_name_returns_number_of_maps(self, c, query, count):
        response = c.get(reverse('api:rms_by_name', kwargs={'name': query}))
        self.assertEquals(count, len(response.json()['maps']))

    def prepare_sample_rms_entities(self):
        masking = []
        first = self.create_sample_map()
        first.created = datetime.datetime(2018, 12, 1, 1, 1, 1, tzinfo=pytz.utc)
        masking.append(self.mask_uuid(first))
        second = self.create_sample_map()
        second.created = datetime.datetime(2018, 12, 2, 1, 1, 1, tzinfo=pytz.utc)
        masking.append(self.mask_uuid(second))
        third = self.create_sample_map()
        third.created = datetime.datetime(2018, 12, 3, 1, 1, 1, tzinfo=pytz.utc)
        masking.append(self.mask_uuid(third))
        third_predecessor = self.create_sample_map(newer_version=third)
        third_predecessor.created = datetime.datetime(2018, 12, 2, 2, 1, 1, tzinfo=pytz.utc)
        masking.append(self.mask_uuid(third_predecessor))
        return masking




