from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from practica.models import *
from practica.serializers import *
from rest_framework.decorators import api_view
from datetime import datetime
import json
from dateutil.relativedelta import relativedelta

import urllib.request
import urllib.response
import requests
from django.shortcuts import render

def getUsuarios(request):
    usuarios = requests.get("http://localhost:8080/api/usuarios").json()
    print(len(usuarios[0]["seguidos"]))
    context = {"users":usuarios}
    return render(request, 'usuarios.html', context)