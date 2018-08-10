from django.test import TestCase
from django.urls import resolve

from mapsapp.views import index
from mapsapp.models import *


class HomePageTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)


class ModelTest(TestCase):

    def test_simple_rms(self):
        tag = Tag(name="sample tag")
        tag.save()

        versiontag = VersionTag(name="sample version tag")
        versiontag.save()

        name = "Random Everything Deluxe"
        version = "v2"
        description = "Random Everything Deluxe is a random map that contains everything and is deluxe"
        url = "https://random.everything.deluxe"
        filename = "REDv2.rms"
        file = "map.rms"

        rms = Rms(
            name=name,
            version=version,
            description=description,
            url=url,
            filename=filename,
            file=file
        )
        rms.save()

        rms.tags.add(tag)
        rms.versiontags.add(versiontag)

        assert rms.tags.count() == 1
        assert rms.versiontags.count() == 1

        assert rms.tags.get(id=tag.id).name == "sample tag"
        assert rms.versiontags.get(id=versiontag.id).name == "sample version tag"
        assert rms.file == file
        assert rms.name == name
        assert rms.version == version
        assert rms.description == description
        assert rms.url == url
        assert rms.filename == filename
        assert rms.file == file
