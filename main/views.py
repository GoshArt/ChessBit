from random import random
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
import random


def index(request):
    auth = False
    name = ""
    url_avatar = 'main/img/person.svg'
    error = ""

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
        elif "re_password" in request.POST:
            name = request.POST["name"]
            email = request.POST["email"]
            f_password = request.POST["f_password"]
            re_password = request.POST["re_password"]

            if f_password != re_password:
                error = "Неверный пароль"
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
    name = "Георгий"
    auth = True
    url_avatar = 'main/img/person.svg'
    return render(request, 'main/waiting.html', {"name": name, "url_avatar": url_avatar, "auth": auth})


def profile(request):
    games = []
    for i in range(10):
        res = random.randint(-1, 1)
        game = {"name": "Георгий", "avatar": "main/img/person.svg", "res": res, "date": "23.02.2022", "game_id": "2",
                "history_id": "2"}
        games.append(game)
    id = request.GET.get("id")
    name = "Георгий"
    email = "NechGeorg@gmail.com"
    reg = "11.09.2001"
    rating = random.randint(500, 1200)
    url_avatar = 'main/img/person.svg'
    return render(request, 'main/profile.html',
                  {"games": games, "id": id, "rating": rating, "name": name, "url_avatar": url_avatar, "email": email, "reg": reg})


def servers(request):
    lobbys = []
    for i in range(10):
        res = random.randint(200, 1600)
        lobby = {"name": "Георгий", "rating": res, "avatar": "main/img/art.jpg", "type": "Classic", "game_id": "2"}
        lobbys.append(lobby)
    url_avatar = 'main/img/person.svg'
    return render(request, 'main/servers.html', {"lobbys": lobbys, "url_avatar": url_avatar})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def field(request):
    if request.method == "POST" and is_ajax(request=request):
        a = request.POST["map"]
        return HttpResponse(a)
    else:
        ser = []
        pos_str = "111qkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR0000000000000000000000000000000000000000000000000000000000000000"
        player1 = {"name": "Георгий1", "avatar": "main/img/person.svg", "rating": random.randint(200, 1600)}
        player2 = {"name": "Георгий2", "avatar": "main/img/person.svg", "rating": random.randint(200, 1600)}
        return render(request, 'main/field.html', {"ser": ser, 'player1': player1, 'player2': player2, 'line': pos_str})
