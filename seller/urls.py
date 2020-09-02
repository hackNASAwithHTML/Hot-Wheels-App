from django.urls import path

from . import views


urlpatterns = [
    path('seller/',views.seller_page,name='seller'),
    path('en_mode/',views.en_mode,name='encrypt'),
    path('de_mode/',views.de_mode,name='decrypt'),
    path('add_seller/',views.add_seller,name='add_seller')
]