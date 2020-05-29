# pages/urls.py
from django.urls import path
from .views import addLoginCredentials,login,helloWorld
from facerecog import views

urlpatterns = [
    path('',helloWorld,name='helloWorld'),
    path('login',login,name='login'),
    path('addLoginCredentials',addLoginCredentials,name='addLoginCredentials')
]

