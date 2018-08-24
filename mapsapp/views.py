import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from mapsapp.models import Rms, Image, Collection, Tag, VersionTag
from mapsapp.tokens import email_verification_token
from .forms import NewRmsForm, SignUpForm, SettingsForm, EditRmsForm

API_URL = "API_URL"


def index(request):
    context = {API_URL: reverse('api:maps')}
    return render(request, 'mapsapp/index.html', context)


def maps(request):
    context = {"rmss": Rms.objects.filter(newer_version=None).order_by('name')}
    return render(request, 'mapsapp/maps.html', context)


def rms(request, rms_id):
    rms_instance = get_object_or_404(Rms, pk=rms_id)
    context = {
        API_URL: reverse('api:rms', kwargs={'rms_id': rms_id}),
        "rms": rms_instance}
    return render(request, 'mapsapp/map.html', context)


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


def collection(request, collection_id):
    c = get_object_or_404(Collection, pk=collection_id)
    context = {
        API_URL: reverse('api:collection', kwargs={'collection_id': collection_id}),
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
            if form.cleaned_data['email'] != "":
                send_verification_email(request, user)
                return redirect('email_verification_sent')
            else:
                login(request, user)
                return redirect('mymaps')
    else:
        form = SignUpForm()
    context['form'] = form
    return render(request, 'mapsapp/register.html', context=context)


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
    current_site = get_current_site(request)
    subject = 'Verify Your Email Address'
    message = render_to_string('email_verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
        'token': email_verification_token.make_token(user),
    })
    user.email_user(subject, message)


def verify_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
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
    context = {"rmss": Rms.objects.filter(owner=request.user).order_by('-updated')}
    return render(request, 'mapsapp/mymaps.html', context)


def get_tags(tagstring):
    tags = []
    items = tagstring.split(',')
    for item in items:
        (tag, created) = Tag.objects.get_or_create(name=item)
        tags.append(tag)
    return tags


@login_required
def newmap(request, rms_id=None):
    context = {'messages': []}
    old_rms = None
    if rms_id:
        old_rms = get_object_or_404(Rms, pk=rms_id)
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewRmsForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            new_rms = Rms()
            new_rms.name = form.cleaned_data['name']
            new_rms.owner = request.user
            new_rms.version = form.cleaned_data['version']
            new_rms.authors = form.cleaned_data['authors']
            new_rms.description = form.cleaned_data['description']
            new_rms.url = form.cleaned_data['url']

            fs = FileSystemStorage()
            filename = fs.save(os.path.join(str(new_rms.uuid), form.cleaned_data['file'].name),
                               form.cleaned_data['file'])
            new_rms.file = filename
            new_rms.save()

            if old_rms:
                old_rms.newer_version = new_rms
                old_rms.save()

                for related_collection in old_rms.collection_set.all():
                    related_collection.rms.add(new_rms)
                    related_collection.rms.remove(old_rms)
                    related_collection.save()

            new_rms.versiontags.set(form.cleaned_data['versiontags'])
            tags = get_tags(form.cleaned_data['tags'])
            new_rms.tags.add(*tags)

            imagefiles = request.FILES.getlist('images')
            for image in imagefiles:
                img = Image()
                img.file = image
                img.rms = new_rms
                img.save()
            form = NewRmsForm()
            context['messages'].append({'class': 'success', 'text': 'Rms created successfully'})
        else:
            context['messages'].append({'class': 'danger', 'text': 'That did not work…'})
        # if a GET (or any other method) we'll create a blank form
    else:
        initial = {}
        if old_rms:
            for key in ('name', 'authors', 'description', 'url'):
                initial[key] = getattr(old_rms, key)
        form = NewRmsForm(initial=initial)
    context["form"] = form
    return render(request, 'mapsapp/newmap.html', context=context)


def get_tagstring(tags):
    names = []
    for tag in tags:
        names.append(tag.name)
    return ','.join(names)


@login_required
def editmap(request, rms_id):
    context = {'messages': []}
    rms = get_object_or_404(Rms, pk=rms_id)
    if rms.owner != request.user:
        raise Http404
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EditRmsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            rms.name = form.cleaned_data['name']
            rms.version = form.cleaned_data['version']
            rms.authors = form.cleaned_data['authors']
            rms.description = form.cleaned_data['description']
            rms.url = form.cleaned_data['url']

            rms.versiontags.set(form.cleaned_data['versiontags'])
            rms.tags.clear()
            tags = get_tags(form.cleaned_data['tags'])
            rms.tags.add(*tags)

            rms.save()

            tagstring = get_tagstring(rms.tags.all())
            form = EditRmsForm(instance=rms, initial={'tags': tagstring})
            context['messages'].append({'class': 'success', 'text': 'Rms updated successfully'})
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
