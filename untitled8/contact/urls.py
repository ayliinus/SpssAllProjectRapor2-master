from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'rooms/$', views.all_rooms, name="all_rooms"),
    url(r'token/$', views.token, name="token"),
    url(r'rooms/(?P<slug>[-\w]+)/$', views.room_detail, name="room_detail"),
]