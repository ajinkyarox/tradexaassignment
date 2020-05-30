# pages/views.py
import os
import base64
from django.http import HttpResponse
from .models import LoginCredentials,Message
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


@csrf_exempt
def post(request):

    response={"status":"Failure:Default"}
    try:
        if request.method=="GET":
            if 'Access-Token' in request.headers:
                if 'Refresh-Token' in request.headers:
                    print("GET Method")
                    access_token = request.headers['Access-Token']

                    secret_key = SECRET_KEY
                    payload = None
                    try:
                        payload = jwt.decode(access_token, secret_key)
                    except Exception as e:
                        print(str(e))
                        response = {'status': 'Failure:Exception-' + str(e)}
                    username = payload.get("username")

                    received_expire_time = payload.get("expire_time")

                    if int(time.time()) > received_expire_time:
                        response = {'status': 'Failure:Token Expired'}

                    else:
                        user = None
                        try:
                            user = LoginCredentials.objects.get(username=username, password=payload.get("password"))
                        except LoginCredentials.DoesNotExist:
                            user = None
                            response = {'status': 'Failure:Exception-' + str(e)}
                        if user!=None:
                            msgList = Message.objects.all()
                            rsList = []
                            print(msgList)
                            for mg in msgList:
                                rsList.append({"id": mg.id, "text": mg.message,
                                               "created_by": {"first_name": mg.lid.firstname, "last_name": mg.lid.lastname,
                                                              "username": mg.lid.username},
                                               "created_at": mg.created_at, "updated_at": mg.updated_at})

                            response = rsList
                        else:
                            response={'status':'Failure:User Does Not Exist'}
                else:
                    response = {"status": "Failure:No Refresh Token"}
            else:
                response = {'status': 'Failure:No Access Token'}


        elif request.method=="POST":

            if 'Access-Token' in request.headers:
                if 'Refresh-Token' in request.headers:
                    access_token = request.headers['Access-Token']

                    secret_key = SECRET_KEY
                    payload=None
                    try:
                        payload = jwt.decode(access_token, secret_key)
                    except Exception as e:
                        print(str(e))
                        response = {'status': 'Failure:Exception-' + str(e)}
                    username = payload.get("username")

                    received_expire_time = payload.get("expire_time")

                    if int(time.time()) > received_expire_time:
                        response={'status':'Failure:Token Expired'}

                    else:
                        user = None
                        try:
                            user = LoginCredentials.objects.get(username=username, password=payload.get("password"))
                        except LoginCredentials.DoesNotExist:
                            user = None
                        if user!=None:
                            body_unicode = request.body.decode('utf-8')
                            body_data = json.loads(body_unicode)
                            msgobj=None
                            try:
                                Message.objects.filter(lid=user).update(message=body_data['text'],updated_at=datetime.datetime.now())
                                msgobj=Message.objects.get(lid=user)
                                print(msgobj)

                                response = {'id': str(msgobj.id), "text": msgobj.message,
                                                "created_by": {"first_name": msgobj.lid.firstname,
                                                               "last_name": msgobj.lid.lastname,
                                                               "username": msgobj.lid.username},
                                                "created_at": msgobj.created_at, "updated_at": msgobj.updated_at}


                            except Message.DoesNotExist:
                                msgobj = None
                                response = {'status': 'Failure:Exception-' + str(e)}
                            if msgobj==None:

                                msg=Message()
                                msg.lid=user
                                msg.message=body_data['text']
                                dtnow=datetime.datetime.now()
                                msg.created_at=dtnow
                                msg.updated_at=dtnow
                                msg.save()
                                msg=Message.objects.get(lid=user,message=body_data['text'],created_at=dtnow,updated_at=dtnow)
                                response={'id':msg.id,"text":msg.message,"created_by":{"first_name":msg.lid.firstname,"last_name":msg.lid.lastname,
                                                                                       "username":msg.lid.username},
                                          "created_at":msg.created_at,"updated_at":msg.updated_at}
                        else:
                            response={'status':'Failure:User does not exist.'}
                else:
                    response = {"status": "Failure:No Refresh Token"}
            else:
                response={'status':'Failure:No Access Token'}
        else:
            response = {"status": "Failure:The requested method only supports GET and POST."}
    except Exception as e:
        response = {"status": "Failure:Exception-"+str(e)}
    return JsonResponse(response,safe=False)