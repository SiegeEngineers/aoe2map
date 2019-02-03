import math
import sys
import uuid as uuid
import os
from io import BytesIO
from PIL import Image as PilImage
from django.contrib.auth.models import User

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from aoe2map import settings

MAX_IMAGE_WIDTH = 4200
MAX_IMAGE_HEIGHT = 4200
PREVIEW_WIDTH = 600
PREVIEW_HEIGHT = 311


def rms_image_path(instance, filename):
    return os.path.join(str(instance.rms.uuid), filename)


def rms_path(instance, filename):
    return os.path.join(str(instance.uuid), filename)


class VersionTag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Rms(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=255, blank=True)
    changelog = models.TextField(blank=True, default='')
    authors = models.CharField(max_length=255)
    description = models.TextField()
    information = models.TextField(blank=True, default='')
    url = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=rms_path)
    original_filename = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    versiontags = models.ManyToManyField(VersionTag)
    newer_version = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, default=None,
                                      related_name='predecessors')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.version)


class Image(models.Model):
    rms = models.ForeignKey(Rms, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=rms_image_path)
    preview = models.ImageField(upload_to=rms_image_path, null=True, blank=True)

    def save(self):
        # Opening the uploaded image
        uploaded_image = PilImage.open(self.file)
        uploaded_image = uploaded_image.convert('RGBA')

        factor = 1
        if uploaded_image.width > MAX_IMAGE_WIDTH:
            factor = min(factor, MAX_IMAGE_WIDTH / uploaded_image.width)
        if uploaded_image.height > MAX_IMAGE_HEIGHT:
            factor = min(factor, MAX_IMAGE_HEIGHT / uploaded_image.height)

        output = BytesIO()

        new_width = math.floor(factor * uploaded_image.width)
        new_height = math.floor(factor * uploaded_image.height)

        # Resize/modify the image
        resized_image = uploaded_image.resize((new_width, new_height), resample=PilImage.LINEAR)

        # after modifications, save it to the output
        resized_image.save(output, format='PNG', quality=100)
        output.seek(0)

        # change the image field value to be the newly modifed image value
        self.file = InMemoryUploadedFile(output, 'ImageField', "{}.png".format(os.path.splitext(self.file.name)[0]),
                                         'image/png', sys.getsizeof(output), None)

        if uploaded_image.width != PREVIEW_WIDTH or uploaded_image.height != PREVIEW_HEIGHT:
            width_factor = min(factor, PREVIEW_WIDTH / uploaded_image.width)
            height_factor = min(factor, PREVIEW_HEIGHT / uploaded_image.height)
            preview_factor = max(width_factor, height_factor)

            preview_width = math.floor(preview_factor * uploaded_image.width)
            preview_height = math.floor(preview_factor * uploaded_image.height)

            uncropped_preview = uploaded_image.resize((preview_width, preview_height), resample=PilImage.LINEAR)
            crop_left = math.floor((preview_width - PREVIEW_WIDTH) / 2)
            crop_upper = math.floor((preview_height - PREVIEW_HEIGHT) / 2)
            crop_right = crop_left + PREVIEW_WIDTH
            crop_lower = crop_upper + PREVIEW_HEIGHT
            preview = uncropped_preview.crop((crop_left, crop_upper, crop_right, crop_lower))
            preview_output = BytesIO()
            preview.save(preview_output, format='PNG', quality=100)
            preview_output.seek(0)
            self.preview = InMemoryUploadedFile(preview_output, 'ImageField', "{}.preview.png".format(
                os.path.splitext(self.file.name)[0]), 'image/png', sys.getsizeof(output), None)

        super(Image, self).save()

    def __str__(self):
        items = self.file.name.split('/')
        return "{}".format(items[-1])


@receiver(post_delete, sender=Image)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)
    if instance.preview:
        instance.preview.delete(False)


class Collection(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    description = models.TextField()
    rms = models.ManyToManyField(Rms, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class SiteSettings(models.Model):
    contact = models.TextField(default='')

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteSettings, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Vote(models.Model):
    rms = models.ForeignKey(Rms, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rms', 'user',)
