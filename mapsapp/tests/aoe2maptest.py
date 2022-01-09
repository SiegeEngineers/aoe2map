import itertools
import json
import os

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from mapsapp.models import Tag, VersionTag, Rms


class AbstractAoe2mapTest(TestCase):

    def setUp(self):
        self.failures = []

    def tearDown(self):
        self.assertEqual([], self.failures)

    @classmethod
    def setUpTestData(cls):
        cls.aTag = Tag.objects.create(name='tag-name')
        cls.aVersion = VersionTag.objects.create(name='version-name')
        cls.aUser = User.objects.create_user(username='username', password='password')
        cls.counter = itertools.count()

    def create_sample_map(self, changelog='', newer_version=None, name=None, authors=None):
        rms = Rms()
        rms.owner = self.aUser
        rms.name = f"map-name-{next(self.counter)}" if name is None else name
        rms.changelog = changelog
        rms.authors = 'rms-authors' if authors is None else authors
        rms.description = 'rms-description'
        rms.file = SimpleUploadedFile('file-name', b'file-contents')
        rms.newer_version = newer_version
        rms.save()
        rms.tags.add(self.aTag)
        rms.versiontags.add(self.aVersion)
        rms.save()
        return rms

    def assert_map_has_changelog(self, rms):
        response = self.client.get(reverse('map', kwargs={'rms_id': rms.id, 'slug': rms.slug}))
        self.assertIn(b'Changelog', response.content)

    def assert_map_does_not_have_changelog(self, rms):
        response = self.client.get(reverse('map', kwargs={'rms_id': rms.id, 'slug': rms.slug}))
        self.assertNotIn(b'Changelog', response.content)

    def compareJsonWithValidationFile(self, output, suffix="", masking=None):
        output = json.dumps(output, indent=4)
        self.compareWithValidationFile(output, suffix, masking)

    def compareWithValidationFile(self, output, suffix="", masking=None):
        if masking is None:
            masking = []

        for func in masking:
            output = func(output)
        validation = f"=== new file ===\n{output}"
        filename = f"{self._testMethodName}_{suffix}.html"
        script_file_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(script_file_path, "../tests/snapshots", "output", filename), "w") as f:
            print(output, file=f)

        if not os.path.isfile(os.path.join(script_file_path, "../tests/snapshots", "validation", filename)):
            with open(os.path.join(script_file_path, "../tests/snapshots", "validation", filename), "w") as f:
                print(validation, file=f)
        else:
            with open(os.path.join(script_file_path, "../tests/snapshots", "validation", filename), "r") as f:
                validation = f.read()

        if output.strip() != validation.strip():
            self.failures.append("{} does not match {}!".format(
                os.path.join("output", filename),
                os.path.join("validation", filename)
            ))

    @staticmethod
    def mask_uuid(rms):
        return lambda x: x.replace(str(rms.uuid), f'[{rms.name}_UUID]')

    @staticmethod
    def mask_id(rms):
        return lambda x: x.replace(str(rms.id), f'[{rms.name}_ID]')
