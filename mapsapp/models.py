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
    authors = models.CharField(max_length=255)
    description = models.TextField()
    information = models.TextField(blank=True, default=None)
    url = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=rms_path)
    tags = models.ManyToManyField(Tag)
    versiontags = models.ManyToManyField(VersionTag)
    newer_version = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} ({})".format(self.name, self.version)


class Image(models.Model):
    rms = models.ForeignKey(Rms, on_delete=models.CASCADE)
    file = models.ImageField(upload_to=rms_image_path)

    def save(self):
        # Opening the uploaded image
        im = PilImage.open(self.file)

        output = BytesIO()

        # Resize/modify the image
        im = im.resize((600, 311))

        # after modifications, save it to the output
        im.save(output, format='PNG', quality=100)
        output.seek(0)

        # change the imagefield value to be the newly modifed image value
        self.file = InMemoryUploadedFile(output, 'ImageField', "{}.png".format(os.path.splitext(self.file.name)[0]),
                                         'image/png', sys.getsizeof(output), None)

        super(Image, self).save()

    def __str__(self):
        items = self.file.name.split('/')
        return "{}".format(items[-1])


@receiver(post_delete, sender=Image)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)


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
