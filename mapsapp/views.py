import logging
import os

from django.conf import settings as djangosettings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from aoe2map import imagestorage
from mapsapp.helpers import count_voters, has_self_voted
from mapsapp.models import Rms, Image, Collection, Tag, VersionTag, SiteSettings, RmsCollection
from mapsapp.tokens import email_verification_token
from .forms import NewRmsForm, SignUpForm, SettingsForm, EditRmsForm, CollectionForm

API_URL = "API_URL"
LATEST_MAPS_URL = "LATEST_MAPS_URL"
LATEST_UPDATED_MAPS_URL = "LATEST_UPDATED_MAPS_URL"

logger = logging.getLogger(__name__)


def index(request):
    context = {
        API_URL: reverse('api:maps'),
        LATEST_MAPS_URL: reverse('api:latest_rms', kwargs={'amount': 3}),
        LATEST_UPDATED_MAPS_URL: reverse('api:latest_updated_rms', kwargs={'amount': 3})
    }
    return render(request, 'mapsapp/index.html', context)


def maps(request):
    context = {"rmss": Rms.objects.filter(newer_version=None, archived=False).order_by('name')}
    return render(request, 'mapsapp/maps.html', context)


def rms_redirect(request, rms_id):
    rms_object = Rms.objects.get(uuid=rms_id)
    return redirect('map', rms_id=rms_object.id, slug=rms_object.slug)


def rms(request, rms_id, slug):
    rms_instance = get_object_or_404(Rms, id=rms_id)
    collections_for_user = []
    self_voted = False
    if request.user.is_authenticated:
        collections_for_user = Collection.objects.filter(owner=request.user).order_by('name')
        self_voted = has_self_voted(rms_instance, request.user.id)
    de_map = rms_instance.versiontags.filter(name="DE")
    context = {
        API_URL: reverse('api:rms', kwargs={'rms_id': rms_instance.uuid}),
        "rms": rms_instance,
        "top_url": djangosettings.DJANGO_TOP_URL,
        "page_url": reverse('map', kwargs={'rms_id': rms_instance.id, 'slug': rms_instance.slug}),
        "collections": collections_for_user,
        "votes": count_voters(rms_instance),
        "self_voted": self_voted,
        "de_map": len(de_map)
    }
    return render(request, 'mapsapp/map.html', context)


@login_required
def rms_archive(request, rms_id):
    rms_instance = get_object_or_404(Rms, pk=rms_id, owner=request.user, archived=False)
    context = {"rms": rms_instance}
    if request.POST and 'confirm_archive' in request.POST:
        rms_instance.archived = True
        rms_instance.save()
        return redirect('map', rms_id=rms_instance.uuid)
    return render(request, 'mapsapp/map_archive.html', context)


def map_search(request, name=None):
    if name is None and request.method == "POST" and "searchterm" in request.POST:
        name = request.POST["searchterm"]
    context = {
        "term": name,
        API_URL: reverse('api:rms_by_name', kwargs={'name': name})
    }
    return render(request, 'mapsapp/search.html', context)


def collections(request):
    context = {"collections": Collection.objects.order_by('name')}
    return render(request, 'mapsapp/collections.html', context)


def collection_redirect(request, collection_id):
    collection_object = Collection.objects.get(uuid=collection_id)
    return redirect('collection', collection_id=collection_object.id, slug=collection_object.slug)


def collection(request, collection_id, slug):
    c = get_object_or_404(Collection, id=collection_id)
    context = {
        API_URL: reverse('api:collection', kwargs={'collection_id': c.uuid}),
        "collection": c}
    return render(request, 'mapsapp/collection.html', context)


def mappack(request):
    context = {}
    return render(request, 'mapsapp/mappack.html', context)


def loginpage(request):
    context = {"messages": []}
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        context["username"] = username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mymaps')
        else:
            context['messages'].append({
                'class': 'danger',
                'text': 'Login failed – maybe a wrong username or password?'
            })
    return render(request, 'mapsapp/login.html', context=context)


def registerpage(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if form.cleaned_data['email'] != "":
                send_verification_email(request, user)
                return redirect('email_verification_sent')
            else:
                return redirect('mymaps')
    else:
        form = SignUpForm()
    context['form'] = form
    return render(request, 'mapsapp/register.html', context=context)


@login_required
def settings(request):
    context = {'messages': []}
    if request.method == 'POST':
        form = SettingsForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            if form.cleaned_data['new_password']:
                user.password = make_password(form.cleaned_data['new_password'])
                user.save()
                login(request, user)
                context['messages'].append({'class': 'success', 'text': 'Your password has been changed.'})
            if form.cleaned_data['email'] != user.email:
                user.email = form.cleaned_data['email']
                user.profile.email_confirmed = False
                user.save()
                if form.cleaned_data['email'] == '':
                    context['messages'].append({'class': 'warning', 'text': 'Your email address has been removed.'})
                else:
                    send_verification_email(request, user)
                    return redirect('email_verification_sent')

    else:
        form = SettingsForm(initial={'email': request.user.email})
    context['form'] = form
    return render(request, 'mapsapp/settings.html', context=context)


def send_verification_email(request, user):
    subject = 'Verify Your Email Address'
    message = render_to_string('email_verification_email.html', {
        'user': user,
        'django_top_url': djangosettings.DJANGO_TOP_URL,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': email_verification_token.make_token(user),
    })
    user.email_user(subject, message)


class PasswordResetViewWithCustomDomain(PasswordResetView):
    extra_email_context = {'django_top_url': djangosettings.DJANGO_TOP_URL}


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, 'mapsapp/email_verification_valid.html')
    else:
        return render(request, 'mapsapp/email_verification_invalid.html')


def logoutpage(request):
    logout(request)
    return redirect('index')


@login_required
def mymaps(request):
    context = {"rmss": Rms.objects.filter(owner=request.user, archived=False).order_by('-updated')}
    return render(request, 'mapsapp/mymaps.html', context)


@login_required
def mycollections(request):
    context = {"collections": Collection.objects.filter(owner=request.user).order_by('name')}
    return render(request, 'mapsapp/mycollections.html', context)


def get_tags(tagstring):
    tags = []
    items = tagstring.split(',')
    for item in items:
        item = item.strip()
        (tag, created) = Tag.objects.get_or_create(name=item)
        tags.append(tag)
    return tags


class InvalidImageError(Exception):
    pass


def get_images_to_copy_or_throw(input_paths):
    retval = []
    for path in input_paths:
        if imagestorage.IMAGE_STORAGE.exists(path):
            retval.append(path)
        else:
            raise InvalidImageError
    return retval


@login_required
def newmap(request, rms_id=None, created_rms_id=None):
    context = {'messages': [], 'old_rms': None}
    old_rms = None
    initial = {}
    if rms_id:
        old_rms = get_object_or_404(Rms, pk=rms_id, archived=False)
        context['old_rms'] = old_rms
        if old_rms.newer_version:
            raise Http404
        for key in ('name', 'authors', 'description', 'url', 'mod_id', 'information'):
            initial[key] = getattr(old_rms, key)
        initial['images_to_copy'] = [(img.file, img) for img in Image.objects.filter(rms=old_rms)]
        initial['tags'] = get_tagstring(old_rms.tags.all())
    if created_rms_id:
        context['messages'].append({'class': 'success',
                                    'text': '''Your Map has been created! Click 
                                    <a href="{}" id="a-goto-created-map">here</a> to view it, or 
                                    <a href="{}" id="a-goto-edit-created-map">here</a> to edit it further.'''.format(
                                        reverse('map_uuid', kwargs={'rms_id': created_rms_id}),
                                        reverse('editmap', kwargs={'rms_id': created_rms_id})
                                    )})
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewRmsForm(request.POST, request.FILES, initial=initial)
        # check whether it's valid:
        if form.is_valid():
            try:
                images_to_copy = get_images_to_copy_or_throw(form.cleaned_data['images_to_copy'])
            except InvalidImageError:
                return HttpResponseBadRequest('Error: Images not found.')
            new_rms = Rms()
            new_rms.name = form.cleaned_data['name']
            new_rms.owner = request.user
            new_rms.version = form.cleaned_data['version']
            new_rms.authors = form.cleaned_data['authors']
            new_rms.description = form.cleaned_data['description']
            new_rms.information = form.cleaned_data['information']
            new_rms.changelog = form.cleaned_data['changelog']
            new_rms.url = form.cleaned_data['url']
            new_rms.mod_id = form.cleaned_data['mod_id']
            new_rms.original_filename = form.cleaned_data['file'].name

            fs = FileSystemStorage()
            filename = fs.save(os.path.join(str(new_rms.uuid), form.cleaned_data['file'].name),
                               form.cleaned_data['file'])
            new_rms.file = filename
            new_rms.save()

            if old_rms:
                old_rms.newer_version = new_rms
                old_rms.save()

                for related_collection in old_rms.collection_set.all():
                    RmsCollection.objects.create(rms=new_rms, collection=related_collection)
                    RmsCollection.objects.filter(rms=old_rms, collection=related_collection).delete()

            new_rms.versiontags.set(form.cleaned_data['versiontags'])
            tags = get_tags(form.cleaned_data['tags'])
            new_rms.tags.add(*tags)

            imagefiles = request.FILES.getlist('images')
            imagefiles.extend(images_to_copy)
            for image in imagefiles:
                if str(image)[-4:].lower() in ['.png', '.jpg', 'jpeg', '.bmp']:
                    img = Image()
                    img.file = image
                    img.rms = new_rms
                    img.save()
            return redirect('newmap_created', created_rms_id=new_rms.uuid)
        else:
            context['messages'].append({'class': 'danger', 'text': 'That did not work…'})
        # if a GET (or any other method) we'll create a blank form
    else:
        form = NewRmsForm(initial=initial)
    context["form"] = form
    return render(request, 'mapsapp/newmap.html', context=context)


@login_required
def editcollection(request, collection_id=None, rms_id=None):
    context = {'messages': [], 'action': 'Create', 'rms_initial_data': []}
    verb = 'created'
    if collection_id:
        verb = 'updated'
        context['action'] = 'Edit'
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        if collection_id:
            collection_instance = get_object_or_404(Collection, pk=collection_id)
            form = CollectionForm(request.POST, instance=collection_instance)
        else:
            form = CollectionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            RmsCollection.objects.filter(collection=instance).delete()
            for rms_instance in form.cleaned_data['rms']:
                RmsCollection.objects.create(rms=rms_instance, collection=instance)
            if collection_id:
                rms_initial_data = []
                for rms_instance in instance.rms.order_by('name'):
                    rms_initial_data.append(
                        {'name': rms_instance.name, 'authors': rms_instance.authors, 'uuid': str(rms_instance.uuid)}
                    )
                context['rms_initial_data'] = rms_initial_data
                context['messages'].append({
                    'class': 'success',
                    'text': '''Collection {} successfully –  
                               <a class="alert-link" href="{}">Show collection</a>'''
                        .format(verb,
                                reverse('collection_uuid', kwargs={'collection_id': instance.uuid}),
                                reverse('editcollection', kwargs={'collection_id': instance.uuid}))
                })

            else:
                form = CollectionForm()
                context['messages'].append({
                    'class': 'success',
                    'text': '''Collection {} successfully –  
                               <a class="alert-link" href="{}">Show collection</a> 
                               – <a class="alert-link" href="{}">Edit collection</a>'''
                        .format(verb,
                                reverse('collection_uuid', kwargs={'collection_id': instance.uuid}),
                                reverse('editcollection', kwargs={'collection_id': instance.uuid}))
                })
        else:
            context['messages'].append({'class': 'danger', 'text': 'That did not work…'})
    else:
        initial = {}
        if collection_id or rms_id:
            rms_ids = []
            rms_initial_data = []
            if rms_id:
                initial_rms_instance = Rms.objects.filter(pk=rms_id, archived=False).first()
                if initial_rms_instance:
                    rms_ids.append(str(initial_rms_instance.uuid))
                    rms_initial_data.append(
                        {'name': initial_rms_instance.name, 'authors': initial_rms_instance.authors,
                         'uuid': str(initial_rms_instance.uuid)}
                    )
            if collection_id:
                collection_instance = get_object_or_404(Collection, pk=collection_id)
                for rms_instance in collection_instance.rms.order_by('name'):
                    rms_ids.append(str(rms_instance.uuid))
                    rms_initial_data.append(
                        {'name': rms_instance.name, 'authors': rms_instance.authors, 'uuid': str(rms_instance.uuid)}
                    )
                initial['rms'] = ','.join(rms_ids)
                context['rms_initial_data'] = rms_initial_data
                form = CollectionForm(initial=initial, instance=collection_instance)
            else:
                initial['rms'] = ','.join(rms_ids)
                context['rms_initial_data'] = rms_initial_data
                form = CollectionForm(initial=initial)
        else:
            form = CollectionForm(initial=initial)
    context["form"] = form
    return render(request, 'mapsapp/templates/mapsapp/editcollection.html', context=context)


def get_tagstring(tags):
    names = []
    for tag in tags:
        names.append(tag.name)
    return ','.join(names)


@login_required
def editmap(request, rms_id):
    context = {'messages': []}
    rms = get_object_or_404(Rms, pk=rms_id, archived=False)
    if rms.owner != request.user:
        raise Http404
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditRmsForm(request.POST, request.FILES, instance=rms)
        # check whether it's valid:
        if form.is_valid():
            rms.name = form.cleaned_data['name']
            rms.version = form.cleaned_data['version']
            rms.authors = form.cleaned_data['authors']
            rms.description = form.cleaned_data['description']
            rms.information = form.cleaned_data['information']
            rms.url = form.cleaned_data['url']

            rms.versiontags.set(form.cleaned_data['versiontags'])
            rms.tags.clear()
            tags = get_tags(form.cleaned_data['tags'])
            rms.tags.add(*tags)

            rms.save()

            tagstring = get_tagstring(rms.tags.all())

            for image_instance in form.cleaned_data['remove_images']:
                image_instance.delete()

            imagefiles = request.FILES.getlist('images')
            for image in imagefiles:
                img = Image()
                img.file = image
                img.rms = rms
                img.save()

            form = EditRmsForm(instance=rms, initial={'tags': tagstring})
            context['messages'].append({
                'class': 'success',
                'text': '''Your Map was updated! Click <a href="{}">here</a> to view it, or continue editing it 
                right here on this page.'''.format(
                    reverse('map_uuid', kwargs={'rms_id': rms.uuid})
                )})
        else:
            context['messages'].append({'class': 'danger', 'text': 'That did not work…'})
    else:
        tagstring = get_tagstring(rms.tags.all())
        form = EditRmsForm(instance=rms, initial={'tags': tagstring})
    context['rms'] = rms
    context['form'] = form
    return render(request, 'mapsapp/editmap.html', context=context)


def email_verification_sent(request):
    context = {'email': request.user.email}
    return render(request, 'mapsapp/email_verification_sent.html', context=context)


def tags(request, url_fragment):
    items = url_fragment.split('/')
    tagset = set()
    for item in items:
        if item.isnumeric():
            tagset.add(get_object_or_404(Tag, pk=int(item)))
    context = {
        "tagset": tagset,
        "alltags": Tag.objects.all(),
        API_URL: reverse('api:tags', kwargs={'url_fragment': url_fragment})
    }
    return render(request, 'mapsapp/tags.html', context)


def version(request, version_name):
    context = {
        "version_name": version_name,
        "allversions": VersionTag.objects.all(),
        API_URL: reverse('api:version', kwargs={'version_name': version_name})
    }
    return render(request, 'mapsapp/version.html', context)


def tags_remove(request, url_fragment, id_to_remove):
    items = url_fragment.split('/')
    tag_id_set = set()
    for item in items:
        if item != "":
            tag_id_set.add(item)
    tag_id_set.remove(id_to_remove)
    new_url_fragment = '/'.join(tag_id_set)
    if new_url_fragment != '':
        new_url_fragment += '/'
    return redirect('tags', url_fragment=new_url_fragment)


def info(request):
    context = {'contact': SiteSettings.load().contact}
    return render(request, 'mapsapp/info.html', context)
