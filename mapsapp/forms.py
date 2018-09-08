from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import OperationalError
from django.forms import Textarea, ModelForm, CheckboxSelectMultiple

from mapsapp.models import VersionTag, Rms, Collection


def get_version_tag_choices():
    versiontags = []
    try:
        for vt in VersionTag.objects.all():
            versiontags.append((vt.id, vt.name))
    except OperationalError:
        pass
    return versiontags


class NewRmsForm(forms.Form):
    name = forms.CharField(max_length=255, help_text="The name of the map")
    version = forms.CharField(max_length=255, required=False, help_text="Optional version indicator like '1.1' or 'v2'")
    authors = forms.CharField(max_length=255, help_text="Who made this map?")
    description = forms.CharField(widget=Textarea,
                                  help_text="Briefly describe the map layout, the setting and/or the idea behind the map. This will appear on the map cards.")
    information = forms.CharField(widget=Textarea, required=False,
                                  help_text="""All the information about the map. This will appear only on the single 
                                  map page. You can use some Markdown syntax in this field, like <b>**bold**</b>, 
                                  <i>_italic_</i> or ~~<del>strikethrough</del>~~""")
    url = forms.CharField(max_length=255, required=False, help_text="An (optional) url for this map")
    file = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['rms'])],
                           help_text="Choose the .rms script you want to share")
    tags = forms.CharField(max_length=255,
                           help_text="Tag your map with up to seven suitable keywords, for example ›4v4‹, ›FFA‹, or ›Nothing‹")
    versiontags = forms.MultipleChoiceField(label="Versions", choices=get_version_tag_choices(),
                                            help_text="The versions that this map works in",
                                            widget=CheckboxSelectMultiple)
    images = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False,
                             help_text="Images get resized to 600x315 px, so you probably want to upload only pictures of that size or aspect ratio")

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags.split(',')) > 8:
            raise ValidationError("You may add at most 7 tags!")
        return tags


class EditRmsForm(ModelForm):
    tags = forms.CharField(max_length=255, required=True, help_text="Tags tags tags!")

    class Meta:
        model = Rms
        fields = ['name', 'version', 'authors', 'description', 'information', 'url', 'tags', 'versiontags']
        widgets = {'versiontags': CheckboxSelectMultiple}

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if len(tags.split(',')) > 8:
            raise ValidationError("You may add at most 7 tags!")
        return tags


class CollectionForm(ModelForm):
    rms = forms.CharField(required=True,
                          help_text="Type the names of the maps you want to add and select the desire map from proposed values!")

    class Meta:
        model = Collection
        fields = ['name', 'authors', 'description', 'rms']

    def clean_rms(self):
        uuidstring = self.cleaned_data['rms']
        uuids = uuidstring.split(',')
        for uuid in uuids:
            if not Rms.objects.filter(pk=uuid).exists():
                raise ValidationError('No map exists for value: %(value)s', params={'value': uuid}, code='invalid_uuid')
        return Rms.objects.filter(uuid__in=uuids)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='A valid email address.', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class SettingsForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='A valid email address.', required=False)
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
