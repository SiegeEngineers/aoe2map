import subprocess

from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.html import escape, format_html
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST

from mapsapp.decorators import ajax_login_required
from mapsapp.helpers import count_voters, get_all_rms_instances, get_latest_version
from mapsapp.models import Rms, VersionTag, Tag, Image, Collection, Vote


@cache_page(60 * 60 * 24)
def version(request):
    try:
        label = subprocess.check_output(["git", "describe", "--tags"]).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        label = 'undefined'
    return JsonResponse({"version": label})


def status(request):
    return JsonResponse({
        "population": {
            "rms": Rms.objects.count(),
            "tag": Tag.objects.count(),
            "versiontag": VersionTag.objects.count(),
            "image": Image.objects.count(),
        }
    })


def allmaps(request):
    retval = []
    map_objects = Rms.objects.filter(newer_version=None, archived=False)
    for map_object in map_objects:
        retval.append({
            'uuid': map_object.uuid,
            'name': map_object.name,
            'authors': map_object.authors,
            'version': map_object.version
        })

    return JsonResponse({"allmaps": retval})


def maps(request):
    objects = maps2json(Rms.objects.filter(newer_version=None, archived=False).order_by('?')[0:12])

    return JsonResponse({"maps": objects})


def rms(request, rms_id):
    rms_instance = get_object_or_404(Rms, pk=rms_id)
    objects = maps2json([rms_instance])

    return JsonResponse({"maps": objects})


def rms_by_name(request, name):
    items = name.split(' ')
    query = Q(name__icontains=items[0]) | Q(authors__icontains=items[0])
    for item in items[1:]:
        query &= (Q(name__icontains=item) | Q(authors__icontains=item))
    rms_objects = Rms.objects.filter(query, newer_version=None, archived=False)
    objects = maps2json(rms_objects)

    return JsonResponse({"maps": objects})


def rms_by_file(request, filename):
    rms = Rms.objects.filter(original_filename=filename, archived=False)
    objects = maps2json(rms)

    return JsonResponse({"maps": objects})


def mymaps(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('You must be logged in to access this url')

    objects = maps2json(Rms.objects.filter(owner=request.user, archived=False))

    return JsonResponse({"maps": objects})


def collection(request, collection_id):
    c = get_object_or_404(Collection, pk=collection_id)
    objects = maps2json(c.rms.order_by('rmscollection__order', 'rmscollection__rms__name'))

    return JsonResponse({
        "maps": objects,
        "uuid": c.uuid,
        "name": escape(c.name),
        "description": escape(c.description),
        "authors": escape(c.authors)
    })


@ajax_login_required
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
        rms_instance = Rms.objects.filter(pk=rms_id, archived=False).first()
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
        map_tags = []
        version_tags = []
        collections = []
        for i in o.image_set.all():
            preview_name = None
            preview_url = None
            if i.preview:
                preview_name = i.preview.name
                preview_url = i.preview.url
            images.append({
                "name": i.file.name,
                "url": i.file.url,
                "preview_name": preview_name,
                "preview_url": preview_url
            })
        for t in o.tags.all():
            map_tags.append({"name": escape(t.name), "id": t.id})
        for vt in o.versiontags.all():
            version_tags.append(vt.name)
        for c in o.collection_set.all():
            collections.append(c.uuid)
        newer_version = None
        latest_version = None
        if o.newer_version:
            newer_version = reverse('map', kwargs={'rms_id': o.newer_version.uuid})
            latest_version = reverse('map', kwargs={'rms_id': get_latest_version(o.newer_version).uuid})
        objects.append({
            "uuid": o.uuid,
            "name": escape(o.name),
            "version": escape(o.version),
            "authors": escape(o.authors),
            "description": escape(o.description),
            "pageurl": reverse('map', kwargs={'rms_id': o.uuid}),
            "newer_version": newer_version,
            "latest_version": latest_version,
            "url": escape(o.url),
            "file": o.file.name,
            "original_filename": o.original_filename,
            "fileurl": o.file.url,
            "tags": map_tags,
            "versiontags": version_tags,
            "collections": collections,
            "images": images,
            "votes": count_voters(o)
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
    resultset = Rms.objects.filter(newer_version=None, archived=False)
    for tag in taglist:
        resultset = resultset.filter(tags=tag)
    objects = maps2json(resultset)

    return JsonResponse({"maps": objects})


def versiontag(request, version_name):
    versiontag_instance = get_object_or_404(VersionTag, name=version_name)
    resultset = Rms.objects.filter(newer_version=None, archived=False, versiontags=versiontag_instance)
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
        rms_objects = Rms.objects.filter(newer_version=None, archived=False, owner=request.user).order_by('name')
    else:
        rms_objects = Rms.objects.filter(newer_version=None, archived=False, name__icontains=searchstring)
    for rms_object in rms_objects:
        maps.append({
            'name': '{name} by {authors}'.format(name=rms_object.name, authors=rms_object.authors),
            'uuid': rms_object.uuid
        })
    return JsonResponse({"maps": maps})


def namebyid(request, rms_id):
    rms_instance = get_object_or_404(Rms, pk=rms_id)
    return JsonResponse({"name": rms_instance.name, "authors": rms_instance.authors})


def latest_rms(request, amount):
    if amount < 0:
        raise Http404
    objects = Rms.objects.filter(newer_version=None, archived=False, predecessors=None).order_by('-created')[:amount]
    return JsonResponse({"maps": maps2json(objects)})


def latest_updated_rms(request, amount):
    if amount < 0:
        raise Http404
    objects = Rms.objects.filter(newer_version=None, archived=False).exclude(predecessors=None).order_by('-updated')[:amount]
    return JsonResponse({"maps": maps2json(objects)})


@ajax_login_required
@require_POST
def add_vote(request, rms_id):
    rms_instance = get_object_or_404(Rms, pk=rms_id, archived=False)
    Vote.objects.get_or_create(rms=rms_instance, user=request.user)
    return JsonResponse({"votes": count_voters(rms_instance), "self_voted": True})


@ajax_login_required
@require_POST
def remove_vote(request, rms_id):
    rms_instance = get_object_or_404(Rms, pk=rms_id, archived=False)
    all_instances = get_all_rms_instances(rms_instance)
    for instance in all_instances:
        Vote.objects.filter(rms=instance, user=request.user).delete()
    return JsonResponse({"votes": count_voters(rms_instance), "self_voted": False})

