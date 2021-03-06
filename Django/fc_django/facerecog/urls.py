# pages/urls.py
from rest_framework_simplejwt import views as jwt_views
from django.urls import path
from .views import addLoginCredentials,login,post,getNewAccessToken
from rest_framework_jwt.views import obtain_jwt_token
from facerecog import views

urlpatterns = [

    path('auth/login',login,name='login'),
    path('auth/signup',addLoginCredentials,name='addLoginCredentials'),
    path('getNewAccessToken',getNewAccessToken,name='getNewAccessToken'),
    path('posts',post,name='post'),
    path('api-token-auth', obtain_jwt_token),
]

