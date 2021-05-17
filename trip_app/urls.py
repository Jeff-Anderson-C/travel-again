from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('dash', views.dash),
    path('new', views.new),
    path('create', views.create),
    path('logout', views.logout),
    path('remove/<int:trip_id>', views.remove),
    path('join/<int:trip_id>', views.join),
    path('trips/<int:trip_id>', views.info),
    path('trips/edit/<int:trip_id>', views.edit),
    path('trips/update/<int:trip_id>', views.update),
]