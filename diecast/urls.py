from django.urls import path

from . import views


urlpatterns = [
    path('home/add_diecast/',views.add_diecast,name='add_diecast')
]