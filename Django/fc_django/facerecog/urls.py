# pages/urls.py
from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from .views import addLoginCredentials,login,helloWorld
from rest_framework_jwt.views import obtain_jwt_token
from facerecog import views

urlpatterns = [
    path('',helloWorld,name='helloWorld'),
    path('login',login,name='login'),
    path('addLoginCredentials',addLoginCredentials,name='addLoginCredentials'),
    path('api-token-auth', obtain_jwt_token),
]

