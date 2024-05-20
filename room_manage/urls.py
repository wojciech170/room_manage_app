"""
URL configuration for room_manage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from management.views import (
    AddRoomView,
    index,
    RoomsView,
    DeleteRoomView,
    EditRoomView,
    RoomReservationView,
    RoomDetailsView,
    SearchView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('room/new/', AddRoomView.as_view()),
    path('all-rooms/', RoomsView.as_view()),
    re_path(r'^room/delete/(?P<room_id>[0-9]+)', DeleteRoomView.as_view()),
    re_path(r'^room/modify/(?P<room_id>[0-9]+)', EditRoomView.as_view()),
    re_path(r'^room/reserve/(?P<room_id>[0-9]+)', RoomReservationView.as_view()),
    re_path(r'^room/(?P<room_id>[0-9]+)', RoomDetailsView.as_view()),
    re_path(r'^search/$', csrf_exempt(SearchView.as_view())),
]
