from random import random

from django.shortcuts import render
from django.http import HttpResponse
from .models import Gosha
import random


def index(request):
    goshas = Gosha.objects.all()
    name = "Артём"
    auth = True
    id = 5
    url_avatar = 'main/img/art.jpg'
    return render(request, 'main/index.html', {"name": name, "url_avatar": url_avatar, "id": id, "auth": auth})


def profile(request):
    games = []
    for i in range(10):
        res = random.randint(-1, 1)
        game = {"name": "Тёмыч", "avatar": "main/img/art.jpg", "res": res, "date": "23.02.2022", "game_id": "2",
                "history_id": "2"}
        games.append(game)
    id = request.GET.get("id")
    name = "Артём"
    email = "ArtemSurov@gmail.com"
    reg = "11.09.2001"
    url_avatar = 'main/img/art.jpg'
    return render(request, 'main/profile.html',
                  {"games": games, "id": id, "name": name, "url_avatar": url_avatar, "email": email, "reg": reg})


def servers(request):
    url_avatar = 'main/img/art.jpg'
    return render(request, 'main/servers.html', {"url_avatar": url_avatar})

