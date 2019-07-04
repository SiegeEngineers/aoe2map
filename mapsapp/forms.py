from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import OperationalError
from django.forms import Textarea, ModelForm, CheckboxSelectMultiple

from mapsapp.models import VersionTag, Rms, Collection, Image

FORM_HELP_COLLECTION_RMS = "Type the names of the maps you want to add and select the desired map from proposed values!"

FORM_HELP_COLLECTION_NAME = "The name of the collection"

FORM_HELP_COLLECTION_AUTHORS = '''The author(s) of the collection - usually the names of the map author(s) 
or the name of this collection's curator'''

FORM_HELP_COLLECTION_DESCRIPTION = '''Describe this collection: What kind of maps are contained, 
                                   what is the overall theme of this collection, …'''

FORM_HELP_REMOVE_IMAGES = "Check all images that you want to <b>remove</b>"

FORM_HELP_VERSIONS = "The versions that this map works in"

FORM_HELP_TAGS = 'Tag your map with up to seven suitable keywords, for example ›4v4‹, ›FFA‹, or ›Nothing‹'

FORM_HELP_URL = "An (optional) url for this map"

FORM_HELP_MAP_INFORMATION = '''All the information about the map. This will appear only on the single 
map page. You can use some Markdown syntax in this field, like <b>**bold**</b>, 
<i>_italic_</i>, ~~<del>strikethrough</del>~~, <tt>[Link](https://example.org)</tt> or <b># Header</b>'''

FORM_HELP_MAP_DESCRIPTION = '''Briefly describe the map layout, the setting and/or the idea behind the 
                                  map. This will appear on the map cards.'''

FORM_HELP_MAP_AUTHORS = "Who made this map?"

FORM_HELP_MAP_VERSION = "Optional version indicator like '1.1' or 'v2'"

FORM_HELP_MAP_CHANGELOG = '''Optional text describing the changes in this version of the map 
compared to the previous version'''

FORM_HELP_MAP_NAME = "The name of the map"

FORM_HELP_IMAGES = '''<b>Preview Images will be 600x311 px</b>, so you should preferrably upload pictures of that size 
or aspect ratio. You can also drag+drop images in here.<br>
Maximum image size is 4200x4200 px.'''

FORM_HELP_FILE = "Choose the .rms file you want to share. You can also drag+drop it in here."

FORM_HELP_IMAGES_TO_COPY = "Select the image files you want to copy to your new map."


def get_version_tag_choices():
    versiontags = []
    try:
        for vt in VersionTag.objects.all():
            versiontags.append((vt.id, vt.name))
    except OperationalError:
        pass
    return versiontags


class NewRmsForm(forms.Form):
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['rms'])],
                           help_text=FORM_HELP_FILE)

    images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}),
                             required=False,
                             help_text=FORM_HELP_IMAGES)

    name = forms.CharField(max_length=255,
                           help_text=FORM_HELP_MAP_NAME)

    version = forms.CharField(max_length=255,
                              required=False,
                              help_text=FORM_HELP_MAP_VERSION)

    changelog = forms.CharField(widget=Textarea(attrs={'rows': 3}),
                                required=False,
                                help_text=FORM_HELP_MAP_CHANGELOG)

    authors = forms.CharField(max_length=255,
                              help_text=FORM_HELP_MAP_AUTHORS)

    description = forms.CharField(widget=Textarea,
                                  help_text=FORM_HELP_MAP_DESCRIPTION)

    url = forms.CharField(max_length=255,
                          required=False,
                          help_text=FORM_HELP_URL)

    information = forms.CharField(widget=Textarea,
                                  required=False,
                                  help_text=FORM_HELP_MAP_INFORMATION)

    tags = forms.CharField(max_length=255,
                           help_text=FORM_HELP_TAGS)

    versiontags = forms.MultipleChoiceField(label="Versions",
                                            choices=[],
                                            help_text=FORM_HELP_VERSIONS,
                                            widget=CheckboxSelectMultiple)

    images_to_copy = forms.MultipleChoiceField(label="Copy Images",
                                               help_text=FORM_HELP_IMAGES_TO_COPY,
                                               widget=CheckboxSelectMultiple)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags.split(',')) > 8:
            raise ValidationError("You may add at most 7 tags!")
        return tags

    def __init__(self, *args, **kwargs):
        super(NewRmsForm, self).__init__(*args, **kwargs)
        self.fields['versiontags'].choices = get_version_tag_choices()
        if 'initial' in kwargs and 'images_to_copy' in kwargs['initial']:
            self.fields['images_to_copy'].choices = kwargs['initial']['images_to_copy']


class EditRmsForm(ModelForm):
    tags = forms.CharField(max_length=255,
                           required=True)

    remove_images = forms.ModelMultipleChoiceField(queryset=None,
                                                   required=False,
                                                   widget=CheckboxSelectMultiple)

    images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}),
                             required=False,
                             label='Add images')

    class Meta:
        model = Rms
        fields = ['name', 'version', 'authors', 'description', 'url', 'changelog', 'information', 'tags', 'versiontags']
        widgets = {
            'versiontags': CheckboxSelectMultiple,
            'changelog': Textarea(attrs={'rows': 3}),
            'description': Textarea(attrs={'rows': 3})
        }
        help_texts = {
            'name': FORM_HELP_MAP_NAME,
            'version': FORM_HELP_MAP_VERSION,
            'changelog': FORM_HELP_MAP_CHANGELOG,
            'authors': FORM_HELP_MAP_AUTHORS,
            'description': FORM_HELP_MAP_DESCRIPTION,
            'url': FORM_HELP_URL,
            'information': FORM_HELP_MAP_INFORMATION,
            'tags': FORM_HELP_TAGS,
            'versiontags': FORM_HELP_VERSIONS,
            'remove_images': FORM_HELP_REMOVE_IMAGES,
            'images': FORM_HELP_IMAGES
        }

    def __init__(self, *args, **kwargs):
        super(EditRmsForm, self).__init__(*args, **kwargs)
        self.fields['remove_images'].queryset = Image.objects.filter(rms=self.instance)

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags.split(',')) > 8:
            raise ValidationError("You may add at most 7 tags!")
        return tags


class CollectionForm(ModelForm):
    rms = forms.CharField(required=True,
                          help_text=FORM_HELP_COLLECTION_RMS,
                          label='Maps')

    class Meta:
        model = Collection
        fields = ['name', 'authors', 'description', 'rms']
        help_texts = {
            'name': FORM_HELP_COLLECTION_NAME,
            'authors': FORM_HELP_COLLECTION_AUTHORS,
            'description': FORM_HELP_COLLECTION_DESCRIPTION
        }

    def clean_rms(self):
        uuidstring = self.cleaned_data['rms']
        uuids = uuidstring.split(',')
        for uuid in uuids:
            if not Rms.objects.filter(pk=uuid).exists():
                raise ValidationError('No map exists for value: %(value)s', params={'value': uuid}, code='invalid_uuid')
        return Rms.objects.filter(uuid__in=uuids)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,
                             help_text='A valid email address.',
                             required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class SettingsForm(forms.Form):
    email = forms.EmailField(max_length=254,
                             help_text='A valid email address.',
                             required=False)

    new_password = forms.CharField(widget=forms.PasswordInput,
                                   help_text="Enter a new password if you want to change it. " +
                                             "If you want to keep your old password, leave this field blank.",
                                   required=False)
    current_password = forms.CharField(widget=forms.PasswordInput,
                                       help_text="Enter your current password to confirm the changes")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SettingsForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()
        current_password = cleaned_data.get('current_password')
        if self.user and not check_password(current_password, self.user.password):
            self.add_error('current_password', 'Current password does not match.')
