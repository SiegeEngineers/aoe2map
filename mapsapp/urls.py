from django.urls import path

from . import views, api


urlpatterns = [
    path('', views.index, name='index'),
    path('maps', views.maps, name='maps'),
    path('map/<uuid:rms_id>', views.map, name='map'),
    path('map/s/<name>', views.map_search, name='map_search'),
    path('map/s/', views.map_search, name='map_search_post'),
    path('collections', views.collections, name='collections'),
    path('collection/<uuid:collection_id>', views.collection, name='collection'),
    path('mappack', views.mappack, name='mappack'),
    path('login', views.loginpage, name='login'),
    path('register', views.registerpage, name='register'),
    path('logout', views.logoutpage, name='logout'),
    path('mymaps', views.mymaps, name='mymaps'),
    path('newmap', views.newmap, name='newmap'),
]