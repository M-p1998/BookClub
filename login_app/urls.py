from django.urls import path
from . import views


urlpatterns = [

    path('', views.index),
    path("register/user",views.register),
    path("login/user",views.login),
    path("Logout",views.logout),

    
]
