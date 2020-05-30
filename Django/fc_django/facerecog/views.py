# pages/views.py
import os
import base64
from django.http import HttpResponse
from .models import LoginCredentials
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import QueryDict
from os import path
import json
import re
from re import search
import datetime,calendar
import time
from datetime import date
from rest_framework_jwt.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import sys
sys.path.append('..')
from fc_django.settings import SECRET_KEY
import jwt

@csrf_exempt
def helloWorld(request):
    body_unicode = request.body.decode('utf-8')
    body_data = json.loads(body_unicode)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



   # payload = jwt_payload_handler(user)
    refresh_token_content = {
        "username":body_data['username'],
        "password": body_data['password']
    }
    refresh_Token = {'refreshToken': jwt.encode(refresh_token_content, SECRET_KEY)}
    temp = refresh_Token.get('refreshToken')
    actual_refresh_token = temp.decode("utf-8")
    ts = int(time.time())  # adding issual_time and expire_time
    access_token_content = {
        "username": body_data['username'],
        "password": body_data['password'],
        "issual_time": ts,
        "expire_time": ts + 60
    }
    jwt_token = {'token': jwt.encode(access_token_content, SECRET_KEY)}
    u = jwt_token.get('token')
    actual_access_token = u.decode("utf-8")
    ts = float(time.time())
    final_payload_x = {"user":
        {
            "username": body_data['username'],
            "password":  body_data['password'],
            "issual_time": int(ts),
            "expire_time": int(ts + 60)
        },

        "jwtToken": actual_access_token,
        "refreshToken": actual_refresh_token
    }
    return JsonResponse(final_payload_x)

@csrf_exempt
def addLoginCredentials(request):
    response={'status': 'Failure'}
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user=None
            try:
                user = LoginCredentials.objects.get(username=body_data['username'])
            except LoginCredentials.DoesNotExist:
                user = None
            if user==None:
                loginCred=LoginCredentials()
                loginCred.username=body_data['username']

                loginCred.password=body_data['password']
                loginCred.firstname=body_data['first_name']
                loginCred.lastname=body_data['last_name']
                loginCred.save()
                refresh_token_content = {
                    "username": body_data['username'],
                    "password": body_data['password'],
                    "firstname":body_data['first_name'],
                    "lastname":body_data['last_name']
                }
                refresh_Token = {'refreshToken': jwt.encode(refresh_token_content, SECRET_KEY)}
                temp = refresh_Token.get('refreshToken')
                actual_refresh_token = temp.decode("utf-8")
                ts = int(time.time())  # adding issual_time and expire_time
                access_token_content = {
                    "username": body_data['username'],
                    "password": body_data['password'],
                    "firstname": body_data['first_name'],
                    "lastname": body_data['last_name'],
                    "issual_time": ts,
                    "expire_time": ts + 300
                }
                jwt_token = {'token': jwt.encode(access_token_content, SECRET_KEY)}
                u = jwt_token.get('token')
                actual_access_token = u.decode("utf-8")
                ts = float(time.time())
                final_payload_x = {

                    "access_token": actual_access_token,
                    "refresh_token": actual_refresh_token
                }

                response = final_payload_x
            else:
                response = {'status': 'Failure:UserName already exists'}
        except Exception as e:
            print(str(e))
            response = {'status': 'Failure:Exception-'+str(e) }
    else:
        response = {'status': 'Failure:Given method is POST method.' }
    return JsonResponse(response,safe=False)

@csrf_exempt
def login(request):
    response = {'status': 'Failure'}
    if request.method == "POST":
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            user = None
            try:
                user =LoginCredentials.objects.get(username=body_data['username'],password=body_data['password'])
            except LoginCredentials.DoesNotExist:
                user = None
            if  user!= None:
                refresh_token_content = {
                    "username": body_data['username'],
                    "password": body_data['password']
                }
                refresh_Token = {'refreshToken': jwt.encode(refresh_token_content, SECRET_KEY)}
                temp = refresh_Token.get('refreshToken')
                actual_refresh_token = temp.decode("utf-8")
                ts = int(time.time())  # adding issual_time and expire_time
                access_token_content = {
                    "username": body_data['username'],
                    "password": body_data['password'],
                    "issual_time": ts,
                    "expire_time": ts + 300
                }
                jwt_token = {'token': jwt.encode(access_token_content, SECRET_KEY)}
                u = jwt_token.get('token')
                actual_access_token = u.decode("utf-8")
                ts = float(time.time())
                final_payload_x = {

                    "access_token": actual_access_token,
                    "refresh_token": actual_refresh_token
                }

                response = final_payload_x
            else:
                response = {'status': 'Failure:Invalid username/password'}
        except Exception as e:
            print(str(e))
            response = {'status': 'Failure:Exception-'+str(e)}
    else:
        response = {'status': 'Failure:Given method is POST method.'}
    return JsonResponse(response,safe=False)

#Given a directory below function returns part of gray_img which is face alongwith its label/ID
@csrf_exempt
def post(request):
    print(request.headers)
    response={"status":"Failure:Default"}
    if request.method=="GET":
        print("GET Method")
    elif request.method=="POST":

        if 'Access-Token' in request.headers:
            if 'Refresh-Token' in request.headers:
                access_token = request.headers['Access-Token']
                print(access_token)
                secret_key = SECRET_KEY
                payload=None
                try:
                    payload = jwt.decode(access_token, secret_key)
                except Exception as e:
                    print(str(e))
                username = payload.get("username")
                first_name = payload.get("first_name")
                last_name=payload.get("last_name")
                received_expire_time = payload.get("expire_time")
                received_issual_time = payload.get("issual_time")
                if int(time.time()) > received_expire_time:
                    response={'status':'Failure:Token Expired'}
                else:
                    response={'status':'Success'}
            else:
                response = {"status": "Failure:No Refresh Token"}
        else:
            response={'status':'Failure:No Access Token'}
    else:
        response = {"status": "Failure:The requested method only supports GET and POST."}
    return JsonResponse(response,safe=False)