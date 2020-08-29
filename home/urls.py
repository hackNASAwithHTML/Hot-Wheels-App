from django.urls import path

from . import views


urlpatterns = [
    path('home/',views.home,name='home'),
    path('home/car_culture',views.car_culture,name='car_culture'),
    path('home/red_line_club',views.red_line_club,name='red_line_club'),
    path('home/super_treasure_hunt',views.super_treasure_hunt,name='super_treasure_hunt')
]