import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import escape

from mapsapp.models import Rms, Image, Collection
from .forms import NewRmsForm

API_URL = "API_URL"


def index(request):
    context = {API_URL: reverse('api:maps')}
    return render(request, 'mapsapp/index.html', context)


def maps(request):
    context = {"rmss": Rms.objects.order_by('name')}
    return render(request, 'mapsapp/maps.html', context)


def map(request, rms_id):
    rms = get_object_or_404(Rms, pk=rms_id)
    context = {
        API_URL: reverse('api:rms', kwargs={'rms_id': rms_id}),
        "rms": rms}
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
    user = None
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
    return HttpResponse("register")


def logoutpage(request):
    logout(request)
    return redirect('index')


@login_required
def mymaps(request):
    context = {"rmss": Rms.objects.filter(owner=request.user).order_by('-updated')}
    return render(request, 'mapsapp/mymaps.html', context)


@login_required
def newmap(request):
    context = {'messages': []}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewRmsForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            rms = Rms()
            rms.name = escape(form.cleaned_data['name'])
            rms.owner = request.user
            rms.version = escape(form.cleaned_data['version'])
            rms.authors = escape(form.cleaned_data['authors'])
            rms.description = escape(form.cleaned_data['description'])
            rms.url = escape(form.cleaned_data['url'])

            fs = FileSystemStorage()
            filename = fs.save(os.path.join(str(rms.uuid), form.cleaned_data['file'].name), form.cleaned_data['file'])
            rms.file = filename
            rms.save()

            rms.tags.set(form.cleaned_data['tags'])
            rms.versiontags.set(form.cleaned_data['versiontags'])

            imagefiles = request.FILES.getlist('images')
            for image in imagefiles:
                img = Image()
                img.file = image
                img.rms = rms
                img.save()
            form = NewRmsForm()
            context['messages'].append({'class': 'success', 'text': 'Rms created successfully'})
        else:
            context['messages'].append({'class': 'danger', 'text': 'That did not work…'})
        # if a GET (or any other method) we'll create a blank form
    else:
        form = NewRmsForm()
    context["form"] = form
    return render(request, 'mapsapp/newmap.html', context=context)
