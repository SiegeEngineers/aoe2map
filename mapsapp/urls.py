from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from mapsapp.views import PasswordResetViewWithCustomDomain
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info', views.info, name='info'),
    path('maps', views.maps, name='maps'),
    path('map/<uuid:rms_id>', views.rms, name='map'),
    path('map/<uuid:rms_id>/archive', views.rms_archive, name='map_archive'),
    path('map/s/<name>', views.map_search, name='map_search'),
    path('map/s/', views.map_search, name='map_search_post'),
    path('collections', views.collections, name='collections'),
    path('collection/<uuid:collection_id>', views.collection, name='collection'),
    path('mappack', views.mappack, name='mappack'),
    path('login', views.loginpage, name='login'),
    path('register', views.registerpage, name='register'),
    path('settings', views.settings, name='settings'),
    path('logout', views.logoutpage, name='logout'),
    path('mymaps', views.mymaps, name='mymaps'),
    path('mycollection', views.mycollections, name='mycollections'),
    path('newmap/created/<uuid:created_rms_id>', views.newmap, name='newmap_created'),
    path('newmap/<uuid:rms_id>', views.newmap, name='newmap_newer_version'),
    path('newmap', views.newmap, name='newmap'),
    path('edit/<uuid:rms_id>', views.editmap, name='editmap'),
    path('editcollection/<uuid:collection_id>', views.editcollection, name='editcollection'),
    path('newcollection', views.editcollection, name='newcollection'),
    path('newcollection/<uuid:rms_id>', views.editcollection, name='newcollection'),
    path('version/<version_name>', views.version, name='version'),
    re_path(r'^tags/(?P<url_fragment>(\d+/)*)$', views.tags, name='tags'),
    re_path(r'^tags/(?P<url_fragment>(\d+/)+)remove/(?P<id_to_remove>\d+)/$', views.tags_remove, name='tags_remove'),
    path('email_verification_sent', views.email_verification_sent, name='email_verification_sent'),
    path('verify/<uidb64>/<token>', views.verify_email, name='verify_email'),
    path('password_reset', PasswordResetViewWithCustomDomain.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

