from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import escape

from mapsapp.models import Rms, VersionTag, Tag, Image, Collection


def version(request):
    return JsonResponse({"version": "0.1"})


def status(request):
    return JsonResponse({
        "population": {
            "rms": Rms.objects.count(),
            "tag": Tag.objects.count(),
            "versiontag": VersionTag.objects.count(),
            "image": Image.objects.count(),
        }
    })


def maps(request):
    objects = maps2json(Rms.objects.filter(newer_version=None).order_by('?')[0:12])

    return JsonResponse({"maps": objects})


def rms(request, rms_id):
    rms = get_object_or_404(Rms, pk=rms_id)
    objects = maps2json([rms])

    return JsonResponse({"maps": objects})


def rms_by_name(request, name):
    rms = Rms.objects.filter(newer_version=None).filter(name__icontains=name) | \
          Rms.objects.filter(newer_version=None).filter(authors__icontains=name)
    objects = maps2json(rms)

    return JsonResponse({"maps": objects})


def mymaps(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('You must be logged in to access this url')

    objects = maps2json(Rms.objects.filter(owner=request.user))

    return JsonResponse({"maps": objects})


def collection(request, collection_id):
    c = get_object_or_404(Collection, pk=collection_id)
    objects = maps2json(c.rms.all())

    return JsonResponse({"maps": objects})


def maps2json(maps):
    objects = []
    for o in maps:
        images = []
        tags = []
        versiontags = []
        for i in o.image_set.all():
            images.append({"name": i.file.name, "url": i.file.url})
        for t in o.tags.all():
            tags.append({"name": t.name, "id": t.id})
        for vt in o.versiontags.all():
            versiontags.append(vt.name)
        objects.append({
            "uuid": o.uuid,
            "name": escape(o.name),
            "version": escape(o.version),
            "authors": escape(o.authors),
            "description": escape(o.description),
            "pageurl": reverse('map', kwargs={'rms_id': o.uuid}),
            "url": escape(o.url),
            "file": o.file.name,
            "fileurl": o.file.url,
            "tags": tags,
            "versiontags": versiontags,
            "images": images,
        })
    return objects


def tags(request, url_fragment):
    items = url_fragment.split('/')
    taglist = []
    for item in items:
        if item.isnumeric():
            taglist.append(get_object_or_404(Tag, pk=int(item)))
    resultset = Rms.objects.filter(newer_version=None)
    for tag in taglist:
        resultset = resultset.filter(tags=tag)
    objects = maps2json(resultset)

    return JsonResponse({"maps": objects})


def version(request, version_name):
    version = get_object_or_404(VersionTag, name=version_name)
    resultset = Rms.objects.filter(newer_version=None).filter(versiontags=version)
    objects = maps2json(resultset)

    return JsonResponse({"maps": objects})
