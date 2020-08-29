from django.urls import path

from . import views


urlpatterns = [
    path('signup/',views.signup_function,name='sign_in'),
    path('login/',views.login_function,name='log_in'),
    path('logout/',views.logout_session,name='log_out'),
]