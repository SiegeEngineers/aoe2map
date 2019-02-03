import datetime

import pytz
from django.test import Client
from django.urls import reverse

from mapsapp.tests.aoe2maptest import AbstractAoe2mapTest


class ApiTest(AbstractAoe2mapTest):

    def test_latest_rms(self):
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

        c = Client()

        response = c.get(reverse('api:latest_rms', kwargs={'amount': 3}))
        self.compareJsonWithValidationFile(response.json(), masking=masking)
