from random import random

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import random


def index(request):
    auth = False
    name = ""
    url_avatar = 'main/img/art.jpg'
    error = ""

    print(request.GET)
    print(request.POST)

    if request.method == "GET":
        print("GET")
        pass
        # if "re_password" in request.GET:
        #     print(request.GET)

    elif request.method == "POST":
        print("POST")
        if "username" in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = User.objects.filter(UserNickname=username, UserPassword=password)

            if user:
                request.session['auth'] = True
                request.session['name'] = username
                request.session['password'] = password
            else:
                error = "Данные введены неверно"
                print("Вы рофлите")
        elif "re_password" in request.POST:
            name = request.POST["name"]
            email = request.POST["email"]
            f_password = request.POST["f_password"]
            re_password = request.POST["re_password"]

            if f_password != re_password:
                error = "Пароль хуйня"
            else:
                new_user = User()
                new_user.UserNickname = name
                new_user.UserPassword = f_password
                new_user.UserEmail = email
                new_user.save()
                request.session['auth'] = True
                request.session['name'] = name
                request.session['password'] = f_password
        elif len(request.POST) < 2:
            request.session['auth'] = False
            request.session['name'] = ""
            request.session['password'] = ""
            print("done")

    if "auth" in request.session:
        if request.session["auth"]:
            auth = True
            name = request.session["name"]

    print(auth)
    return render(request, 'main/index.html', {"name": name, "url_avatar": url_avatar, "auth": auth, "error": error})


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
