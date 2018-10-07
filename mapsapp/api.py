from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import escape, format_html

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


@login_required
def modifycollection(request):
    if 'action' not in request.POST:
        return JsonResponse({"status": "ERROR", "message": "'action' is missing", "class": "danger"})

    if request.POST['action'] not in ['add']:
        return JsonResponse({"status": "ERROR", "message": "Invalid action", "class": "danger"})

    if request.POST['action'] == 'add':
        missing_properties = []
        for prop in ['rms_id', 'collection_id']:
            if prop not in request.POST:
                missing_properties.append(prop)
        if len(missing_properties) > 0:
            return JsonResponse({
                "status": "ERROR",
                "message": "The following mandatory properties are missing: {}".format(missing_properties),
                "class": "danger"
            })

        rms_id = request.POST['rms_id']
        collection_id = request.POST['collection_id']
        rms_instance = Rms.objects.filter(pk=rms_id).first()
        collection_instance = Collection.objects.filter(pk=collection_id).first()

        if rms_instance is None:
            return JsonResponse({"status": "ERROR", "message": "Map not found", "class": "warning"})

        if collection_instance is None:
            return JsonResponse({"status": "ERROR", "message": "Collection not found", "class": "warning"})

        if rms_instance.newer_version is not None:
            return JsonResponse({
                "status": "ERROR",
                "message": "You can only add the latest version of a map to a collection",
                "class": "warning"
            })

        collection_instance.rms.add(rms_instance)

        return JsonResponse({
            "status": "OK",
            "message": format_html(
                """The map <i>{mapname}</i> has been added
                to your collection <a href='{collectionurl}'>{collectionname}</a>.""",
                mapname=rms_instance.name, collectionname=collection_instance.name,
                collectionurl=reverse('collection', kwargs={"collection_id": collection_instance.uuid})),
            "class": "success"
        })

    return JsonResponse({"status": "ERROR", "message": "Unknown action", "class": "danger"})


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
        newer_version = None
        if o.newer_version:
            newer_version = reverse('map', kwargs={'rms_id': o.newer_version.uuid})
        objects.append({
            "uuid": o.uuid,
            "name": escape(o.name),
            "version": escape(o.version),
            "authors": escape(o.authors),
            "description": escape(o.description),
            "pageurl": reverse('map', kwargs={'rms_id': o.uuid}),
            "newer_version": newer_version,
            "url": escape(o.url),
            "file": o.file.name,
            "fileurl": o.file.url,
            "tags": tags,
            "versiontags": versiontags,
            "images": images,
        })
    return objects


def tags(request, url_fragment):
    if url_fragment == '':
        return JsonResponse({"maps": []})

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


def versiontag(request, version_name):
    versiontag_instance = get_object_or_404(VersionTag, name=version_name)
    resultset = Rms.objects.filter(newer_version=None).filter(versiontags=versiontag_instance)
    objects = maps2json(resultset)

    return JsonResponse({"maps": objects})


def alltags(request):
    tags = []
    for tag in Tag.objects.order_by('name'):
        tags.append(tag.name)
    return JsonResponse({"tags": tags})


def mapsbyname(request, searchstring=None):
    maps = []
    if not searchstring:
        rms_objects = Rms.objects.filter(newer_version=None).filter(owner=request.user).order_by('name')
    else:
        rms_objects = Rms.objects.filter(newer_version=None).filter(name__icontains=searchstring)
    for rms_object in rms_objects:
        maps.append({
            'name': '{name} by {authors}'.format(name=rms_object.name, authors=rms_object.authors),
            'uuid': rms_object.uuid
        })
    return JsonResponse({"maps": maps})


def namebyid(request, rms_id):
    rms_instance = get_object_or_404(Rms, pk=rms_id)
    return JsonResponse({"name": rms_instance.name, "authors": rms_instance.authors})
