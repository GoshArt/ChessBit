from random import random

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.GameLogic.create_basic_matrix import *
from main.bd_logic import *
from .models import *
import random


def index(request):
    auth = False
    # pos = Users.objects.get(nickname="noksyte2")
    # print(1)
    # Users.objects.create(nickname="ass", password="anal")
    # print(2)
    # pos.ratingelo = 1200
    # pos.save()
    # print(3)
    # v = Users.objects.get(nickname="ass")
    # v.delete()
    # print(4)

    name = ""
    url_avatar = 'main/img/person.svg'
    error = ""

    if request.method == "GET":
        pass
    elif request.method == "POST":
        if "username" in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]

            user = Users.objects.filter(nickname=username, password=password)
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
            if len(Users.objects.filter(nickname=name)) > 0:
                # по идее лучше просто выводить ошибку что такой пользователь уже существует
                return redirect(index)
            if f_password != re_password:
                error = "Неверный пароль"
            else:
                new_user = Users()
                new_user.nickname = name
                new_user.password = f_password
                new_user.email = email
                new_user.save()
                request.session['id'] = Users.objects.get(nickname=name).id
                request.session['auth'] = True
                request.session['name'] = name
                request.session['password'] = f_password
                request.session['email'] = email

        elif 'chosenColor' in request.POST:
            print(2)
            request.session['botColor'] = request.POST['chosenColor']
            return redirect(field)

        elif len(request.POST) < 2:
            request.session['auth'] = False
            request.session['name'] = ""
            request.session['password'] = ""
            print("done")

    if "auth" in request.session:
        if request.session["auth"]:
            auth = True
            name = request.session["name"]

    best_players = []
    best_players_db = Users.objects.order_by('rating_elo').reverse().all()
    p = 1
    for player in best_players_db:
        best_players.append({"name": player.nickname, "res": player.rating_elo})
        if p == 10:
            break
        p += 1
    # best_players = sorted(best_players, key=lambda x: x['res'], reverse=True)
    return render(request, 'main/index.html',
                  {"name": name, "url_avatar": url_avatar, "auth": auth, "error": error, "best_players": best_players,
                   "loginError": "", "registerError": ""})


def waiting(request):
    name = "Георгий"
    auth = True
    url_avatar = 'main/img/person.svg'
    return render(request, 'main/waiting.html', {"name": name, "url_avatar": url_avatar, "auth": auth})


def profile(request):
    if request.method == "GET":

        # Here we are getting required information about specified user.
        # User can be specified by id, name parameter or nothing(in that case user will get their own profile).
        # priority: name > id > nothing.
        user_data = ''
        if "name" in request.GET:
            user_data = find_user_data_by_name(request.GET["name"])
        elif "id" in request.GET:
            user_data = find_user_data_by_id(request.GET["id"])
        else:
            user_data = find_user_data_by_id(request.session['id'])

        id = user_data.id
        rating = user_data.rating_elo
        name = user_data.nickname
        url_avatar = 'main/img/person.svg'  # заглушка
        email = user_data.email
        reg = "11.09.2001"  # заглушка

        games = []
        collected_games_data = GameParticipants.objects.filter(user_id=id).select_related(
            'user').select_related('game')

        print(collected_games_data)
        enemy_guy = ""
        for games_data in collected_games_data:
            guys_data = Users.objects.filter(Q(id=games_data.game.white_player) | Q(id=games_data.game.black_player))
            for i in range(2):
                if guys_data[i].nickname != name:
                    enemy_guy = guys_data[i].nickname

            print("W player:", games_data.game.white_player)
            print("B player:", games_data.game.black_player)
            print("Result:", games_data.game.result)
            print("Finished", games_data.game.finished)
            print("MainUserNickName", name + " VS " + enemy_guy)

        versus = name + "VS" + enemy_guy

        for i in range(min(10, len(collected_games_data))):
            games_data = collected_games_data[i]
            game = {"name": versus,
                    "avatar": "main/img/person.svg",
                    "res": games_data.game.result,
                    "date": "23.02.2022",
                    "game_id": games_data.game_id,
                    }
            games.append(game)
        # id = request.GET.get("id")
        # name = request.session["name"]
        # if "email" not in request.session:
        #     request.session["email"] = Users.objects.get(nickname=name).email
        # email = request.session["email"]

        # rating = random.randint(500, 1200)
        print(games)
        return render(request, 'main/profile.html',
                      {"games": games, "id": id, "rating": rating, "name": name,
                       "url_avatar": url_avatar,
                       "email": email,
                       "reg": reg})

    if request.method == "POST":
        if "username" in request.POST:
            pos = Users.objects.get(nickname=request.session["name"])
            pos.nickname = request.POST["username"]
            pos.save()
            request.session["name"] = request.POST["username"]
            return redirect(profile)

        if "deletion" in request.POST:
            pos = Users.objects.get(nickname=request.session["name"])
            pos.delete()
            request.session["name"] = ""
            request.session['auth'] = False
            print("retard")
            return redirect(index)


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
    if "auth" not in request.session:
        return redirect(index)
    if not request.session["auth"]:
        return redirect(index)
    else:
        name = request.session["name"]

    # if 'botColor' in request.session:
    #     if 'currentPosition' not in request.session:
    #         request.session['currentPosition'] = basic_matrix2D
    if request.method == "GET":
        # current_games = Games.objects.filter(
        #     (Q(white_player=request.session['id']) | Q(black_player=request.session['id']))).exclude(result=1)
        # current_games1 = GameParticipants.objects.get(user_id=1).game.white_player
        # print(current_games1.white_player)
        # print(current_games1.black_player)
        # print(current_games1.game.objects.all())
        # u = Users.objects.get(id=1).gameparticipants_set.all() # collecting all the data from gameparticipants table where user_id == 1
        # for item in u:
        #     print(item.user_id, item.game_id)
        # current_games1.get
        current_active_games = GameParticipants.objects.filter(participant_id=1).select_related("user").select_related(
            "game")
        for retard in current_active_games:
            print(retard.user_id, retard.user.nickname, retard.game_id, retard.participant_id, retard.game.white_player)

    if request.method == "POST" and is_ajax(request=request):
        a = request.POST["map"]
        mtrx = Matrix(a)
        mtrx.collect_all_possible_moves(request.session["botColor"])
        mtrx.make_a_move(mtrx.pick_a_move())
        a = mtrx.matrix_to_string_conversion()
        return JsonResponse({"map": a})
    else:
        pos_str = "111qkbnrpppppppp11111111111111111111111111111111PPPPPPPPRNBQKBNR0000000000000000000000000000000000000000000000000000000000000000"
        player1 = {"name": name, "avatar": "main/img/person.svg", "rating": random.randint(200, 1600)}

        botArtem = {"name": "Bot Artem v0.1", "avatar": "main/img/robot.svg", "rating": '200'}
        botColor = request.session['botColor']
        return render(request, 'main/field.html', {'player1': player1, 'player2': botArtem, 'line': pos_str,
                                                   'botColor': botColor})
