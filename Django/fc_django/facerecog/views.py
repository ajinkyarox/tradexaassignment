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
from datetime import date

def helloWorld(request):
    return HttpResponse('Hello from Django!')

@csrf_exempt
def addLoginCredentials(request):
    response={'status': 'Failure', 'responseObject': None}
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
            loginCred.firstname=body_data['firstname']
            loginCred.lastname=body_data['lastname']
            loginCred.save()
            response = {'status': 'Success', 'responseObject': None}
        else:
            response = {'status': 'Failure:UserName already exists', 'responseObject': None}
    except Exception as e:
        print(str(e))
        response = {'status': 'Failure:There is some problem', 'responseObject': None}
    return JsonResponse(response,safe=False)

@csrf_exempt
def login(request):
    response = {'status': 'Failure', 'responseObject': None}
    try:
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        user = None
        try:
            user =LoginCredentials.objects.get(username=body_data['username'],password=body_data['password'])
        except LoginCredentials.DoesNotExist:
            user = None
        if  user!= None:
            response = {'status': 'Success', 'responseObject': None}
        else:
            response = {'status': 'Failure:Invalid username/password', 'responseObject': None}
    except Exception as e:
        print(str(e))
        response = {'status': 'Failure', 'responseObject': None}
    return JsonResponse(response,safe=False)

#Given a directory below function returns part of gray_img which is face alongwith its label/ID
