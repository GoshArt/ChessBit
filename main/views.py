from random import random

from django.shortcuts import render
from django.http import HttpResponse
from .models import Gosha
import random


def index(request):
    goshas = Gosha.objects.all()
    name = "Артём"
    auth = True
    url_avatar = 'main/img/art.jpg'
    return render(request, 'main/index.html', {"name": name, "url_avatar": url_avatar, "auth": auth})


def waiting(request):
    name = "Артём"
    auth = True
    url_avatar = 'main/img/art.jpg'
    return render(request, 'main/waiting.html', {"name": name, "url_avatar": url_avatar, "auth": auth})


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
    lobbys = []
    for i in range(10):
        res = random.randint(200, 1600)
        lobby = {"name": "Тёмыч", "rating": res, "avatar": "main/img/art.jpg", "type": "Classic", "game_id": "2"}
        lobbys.append(lobby)
    url_avatar = 'main/img/art.jpg'
    return render(request, 'main/servers.html', {"lobbys": lobbys, "url_avatar": url_avatar})


def field(request):
    ser = []
    pos_str = "rnbqkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR "
    for i in range(64):
        b = ""
        if int(i / 8) % 2 == 0:
            if (i + 2) % 2 == 0:
                a = "sq_w"
            else:
                a = "sq_b"
        else:
            if (i + 2) % 2 == 0:
                a = "sq_b"
            else:
                a = "sq_w"
        match pos_str[i]:
            case 'K':
                b = '♔'
            case 'Q':
                b = '♕'
            case 'R':
                b = '♖'
            case 'B':
                b = '♗'
            case 'N':
                b = '♘'
            case 'P':
                b = '♙'
            case 'k':
                b = '♚'
            case 'q':
                b = '♛'
            case 'r':
                b = '♜'
            case 'b':
                b = '♝'
            case 'n':
                b = '♞'
            case 'p':
                b = '♟'
            case '1':
                b = ''
        ser.append({"sq_c": a, 'pos_f': b})
    player1 = {"name": "Тёмыч1", "avatar": "main/img/art.jpg", "rating": random.randint(200, 1600)}
    player2 = {"name": "Тёмыч2", "avatar": "main/img/art.jpg", "rating": random.randint(200, 1600)}
    return render(request, 'main/field.html', {"ser": ser, 'player1': player1, 'player2': player2})
