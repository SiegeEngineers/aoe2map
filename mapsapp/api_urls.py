from django.urls import path, re_path

from . import views, api

app_name = 'api'
urlpatterns = [
    path('version', api.version, name='version'),
    path('status', api.status, name='status'),
    path('maps', api.maps, name='maps'),
    path('allmaps', api.allmaps, name='allmaps'),
    path('mymaps', api.mymaps, name='mymaps'),
    path('alltags', api.alltags, name='alltags'),
    path('mapsbyname', api.mapsbyname, name='mapsbyname'),
    path('mapsbyname/<searchstring>', api.mapsbyname, name='mapsbyname'),
    path('rms/<uuid:rms_id>', api.rms, name='rms'),
    path('rms/s/<name>', api.rms_by_name, name='rms_by_name'),
    path('rms/file/<filename>', api.rms_by_file, name='rms_by_file'),
    path('collection/<uuid:collection_id>', api.collection, name='collection'),
    path('modifycollection/', api.modifycollection, name='modifycollection'),
    path('version/<version_name>', api.versiontag, name='version'),
    re_path(r'^tags/(?P<url_fragment>(\d+/)*)$', api.tags, name='tags'),
]
