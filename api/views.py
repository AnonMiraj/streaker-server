from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Trainee, TraineeRecord
from .serializers import TraineeSerializer, TraineeRecordSerializer
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class TraineeListCreateView(generics.ListCreateAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer


class TraineeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer


class TraineeRecordListCreateView(generics.ListCreateAPIView):
    queryset = TraineeRecord.objects.all()
    serializer_class = TraineeRecordSerializer

    def perform_create(self, serializer):
        try:
            discord_id = self.request.data['discord_id']
            trainee = Trainee.objects.get(discord_id=discord_id)
        except (KeyError, Trainee.DoesNotExist):
            return Response({"error": "Invalid or missing 'discord_id'."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(trainee=trainee)


class TraineeRecordDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TraineeRecord.objects.all()
    serializer_class = TraineeRecordSerializer

#########################

auth_url_discord = "https://discord.com/api/oauth2/authorize?client_id=1208615497973899315&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Foauth2%2Flogin%2Fredirect&scope=identify"

def home(request: HttpRequest) -> HttpResponse:
    return JsonResponse({ "msg": "nigga" })

def discord_login(request: HttpRequest) -> HttpResponse:
    return redirect(auth_url_discord)

def discord_login_redirect(request: HttpRequest) -> HttpResponse:
    code = request.GET.get('code')
    #print(code)
    #exchange_code(code)
    #return JsonResponse({ "msg": "Redirected."})
    return JsonResponse(exchange_code(code))

def exchange_code(code: str):
    data = {
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('CLIENT_SECRET'),
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri":os.environ.get('REDIRECT_URI'),
            "scope": "identify"
    }

    headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    jsonData = response.json()
    access_token = jsonData['access_token']
    #print ("this is the fucking access token: ", access_token)

    response = requests.get("https://discord.com/api/v6/users/@me", headers = {
        'Authorization': 'Bearer %s' % access_token
    })

    user = response.json()
    print(user)
    print("------------")
    #print(os.environ.get('CLIENT_SECRET'))

    return user
