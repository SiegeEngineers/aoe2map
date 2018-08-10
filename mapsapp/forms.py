from django import forms
from django.core.validators import FileExtensionValidator
from django.forms import Textarea

from mapsapp.models import VersionTag, Tag


def get_version_tag_choices():
    versiontags = []
    for vt in VersionTag.objects.all():
        versiontags.append((vt.id, vt.name))
    return versiontags


def get_tag_choices():
    tags = []
    for t in Tag.objects.all():
        tags.append((t.id, t.name))
    return tags


class NewRmsForm(forms.Form):
    name = forms.CharField(max_length=255, help_text="The name of the map")
    version = forms.CharField(max_length=255, required=False, help_text="Optional version indicator like '1.1' or 'v2'")
    authors = forms.CharField(max_length=255, help_text="Who made this map?")
    description = forms.CharField(widget=Textarea,
                                  help_text="Describe the map layout, the setting and/or the idea behind the map")
    url = forms.CharField(max_length=255, required=False, help_text="An (optional) url for this map")
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['rms'])],
                           help_text="Choose the .rms script you want to share")
    tags = forms.MultipleChoiceField(label='Tags', choices=get_tag_choices(),
                                     help_text="Tag your map with up to seven suitable keywords")
    versiontags = forms.MultipleChoiceField(label="Versions", choices=get_version_tag_choices(),
                                            help_text="The versions that this map works in")
    images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False,
                             help_text="Images get resized to 600x315 px, so you probably want to upload only pictures of that size or aspect ratio")
