from django.test import Client
from django.urls import reverse
from django.utils.encoding import smart_str

from mapsapp.tests.aoe2maptest import AbstractAoe2mapTest


class ChangelogTest(AbstractAoe2mapTest):

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
        response = c.get(reverse('map', kwargs={'rms_id': rms3.id, 'slug': rms3.slug}))
        self.assertEquals(rms3.newer_version, rms2)
        self.assertIn('A newer version of this map is available!', smart_str(response.content))
        self.assertIn(f'<a href="/map/{rms1.id}/map-name-0" class="alert-link">Check it out!</a>',
                      smart_str(response.content))
