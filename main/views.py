from random import random

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.GameLogic.create_basic_matrix import *
from main.bd_logic import *
from .models import *
import random
import json


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
            for u in user:
                print(u.nickname, u.password)
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

            request.session['botColor'] = request.POST['chosenColor']
            if len(Users.objects.filter(nickname='mainBot')) == 0:
                bot = Users.objects.create(nickname='mainBot', role='bot', rating_elo=250)
                bot.save()
            print("size : ", len(GameParticipants.objects.filter(user_id=request.session['id'], game__result="active")))
            if len(GameParticipants.objects.filter(user_id=request.session['id'], game__result="active")) == 0:
                bot_data = Users.objects.get(nickname='mainBot')
                user_data = Users.objects.get(id=request.session['id'])
                new_game = Games.objects.create(result=GAME_RES.ACTIVE)
                new_game.save()
                print(request.POST['chosenColor'])
                participant1 = GameParticipants.objects.create(game_id=new_game.id, user_id=user_data.id,
                                                               user_color=request.POST['chosenColor'])
                participant2 = GameParticipants.objects.create(game_id=new_game.id, user_id=bot_data.id,
                                                               user_color=request.POST['chosenColor'])
                if request.POST['chosenColor'] == 'B':
                    participant2.user_color = "W"
                else:
                    participant2.user_color = "B"
                participant1.save()
                participant2.save()

            return redirect(field)

        elif len(request.POST) < 2:
            request.session['auth'] = False
            request.session['name'] = ""
            request.session['password'] = ""
            request.session['id'] = ""
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
            print(request.session['id'])
            user_data = find_user_data_by_id(request.session['id'])

        id = user_data.id
        rating = user_data.rating_elo
        name = user_data.nickname
        url_avatar = 'main/img/person.svg'  # заглушка
        email = user_data.email
        reg = "11.09.2001"  # заглушка

        games = []
        collected_games_data = GameParticipants.objects.filter(user_id=id).select_related(
            'user').select_related('game').filter(~Q(game__result="active"))

        for item in collected_games_data:
            print(item.game.result)
        enemy_guy = ""
        for games_data in collected_games_data:
            game_id = games_data.game_id
            enemy_guy = GameParticipants.objects.get(Q(game_id=game_id) & ~Q(user_id=id))
            # guys_data = Users.objects.filter(Q(id=games_data.game.white_player) | Q(id=games_data.game.black_player))
            #
            # for i in range(2):
            #     if guys_data[i].nickname != name:
            #         enemy_guy = guys_data[i].nickname
            print("Result:", games_data.game.result)
            print("MainUserNickName", name + " VS " + enemy_guy.user.nickname)
            versus = name + "VS" + enemy_guy.user.nickname
            print(versus)
            left_part = games_data.user_color
            left_result = games_data.game.result
            if left_result == '-1':
                if left_part == "W":
                    left_result = -1
                    right_result = 1
                else:
                    left_result = 1
                    right_result = -1
            elif left_result == '1':
                if left_part == "B":
                    left_result = -1
                    right_result = 1
                else:
                    left_result = 1
                    right_result = -1
            else:
                left_result = 0
                right_result = 0

            games.append(
                {
                    "name": name,
                    "enemy": enemy_guy.user.nickname,
                    "res": games_data.game.result,
                    "date": "23.02.2022",
                    "game_id": games_data.game_id,
                    "side": left_part,
                    "fr": left_result,
                    "sr": right_result,
                }
            )
        # if id == games_data.game.white_player:
        #     side = 1
        # else:
        #     side = -1
        # if (games_data.game.result == 1 and side == 1) or (games_data.game.result == -1 and side == -1):
        #     fr = 1
        #     sr = 0
        # else:
        #     fr = 0
        #     sr = 1

        # for i in range(min(10, len(collected_games_data))):
        #     games_data = collected_games_data[i]
        #     game = {"name": name,
        #             "enemy": enemy_guy,
        #             "avatar": "main/img/person.svg",
        #             "res": games_data.game.result,
        #             "date": "23.02.2022",
        #             "game_id": games_data.game_id,
        #             "side": side,
        #             "fr": fr,
        #             "sr": sr,
        #             }
        #     # print(games_data.game.result)
        #     # print(side)
        #     games.append(game)
        # id = request.GET.get("id")
        # name = request.session["name"]
        # if "email" not in request.session:
        #     request.session["email"] = Users.objects.get(nickname=name).email
        # email = request.session["email"]

        # rating = random.randint(500, 1200)

        return render(request, 'main/profile.html',
                      {"games": games, "id": id, "rating": rating, "name": name,
                       "url_avatar": url_avatar,
                       "email": email,
                       "reg": reg})

    if request.method == "POST":
        if "username" in request.POST:
            print(1)
            pos = Users.objects.get(nickname=request.session["name"])
            pos.nickname = request.POST["username"]
            pos.save()
            request.session["name"] = request.POST["username"]
            return redirect(profile)

        if "deletion" in request.POST:
            print(1)
            pos = Users.objects.get(nickname=request.session["name"])
            pos.delete()
            request.session["name"] = ""
            request.session["id"] = ""
            request.session['auth'] = False
            return redirect(index)
        print(request.POST)


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
    if "type" in request.POST:
        print(request.POST)
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
            print(retard.user_id, retard.user.nickname, retard.game_id, retard.participant_id, retard.user_color)

    if request.method == "POST" and is_ajax(request=request):
        print(request.POST["type"])
        print(request.POST)
        game_data = GameParticipants.objects.get(user_id=request.session['id'], game__result="active")

        print(game_data.game.chessboard_position)
        print(game_data.game_id)
        print(game_data.user.nickname)
        turn_type = "Empty"
        a = game_data.game.chessboard_position
        mtrx = Matrix(a)
        mtrx.current_move = game_data.game.turn
        print(game_data.game.white_player_chosen_square)

        if request.POST['type'] == 'pressSquare':
            turn_type = "Selected"
            print("here")
            chess_map = ""
            if game_data.game.turn % 2 == 1:
                if game_data.game.white_player_chosen_square == "-1":
                    # choosing given figure and returning possible places to go
                    mtrx.get_figure_moves(int(request.POST['y']), int(request.POST['x']), "W")
                    chess_map = mtrx.matrix_to_string_conversion(include_pos_moves=True)
                    if len(mtrx.pos_moves) > 0:
                        game_data.game.white_player_chosen_square = str(request.POST['y']) + str(request.POST['x'])
                        game_data.game.chessboard_position = chess_map
                        game_data.game.save()
                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)

                else:
                    chosen_y = int(request.POST['y'])
                    chosen_x = int(request.POST['x'])
                    prev_chosen_y = int(game_data.game.white_player_chosen_square[0])
                    prev_chosen_x = int(game_data.game.white_player_chosen_square[1])
                    if game_data.game.chessboard_position[64 + chosen_y * 8 + chosen_x] == '2':
                        turn_type = "Correct"
                        mtrx.pieces_on_board[chosen_y][chosen_x] = mtrx.pieces_on_board[prev_chosen_y][prev_chosen_x]
                        mtrx.pieces_on_board[prev_chosen_y][prev_chosen_x] = EmptyPiece()
                        chess_map = mtrx.matrix_to_string_conversion()
                        game_data.game.chessboard_position = chess_map
                        game_data.game.white_player_chosen_square = "-1"
                        game_data.game.turn += 1
                        game_data.game.save()
                    else:
                        mtrx.pos_moves.clear()
                        mtrx.get_figure_moves(chosen_y, chosen_x, "W")
                        chess_map = mtrx.matrix_to_string_conversion(include_pos_moves=True)
                        game_data.game.chessboard_position = chess_map
                        if len(mtrx.pos_moves) > 0:
                            game_data.game.white_player_chosen_square = str(request.POST['y']) + str(request.POST['x'])
                        else:
                            game_data.game.white_player_chosen_square = -1
                        game_data.game.save()

                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)
                    # выбрать фигуру которая была нажата до этого, и если нажатая координата находится в сете доступных ходов, сходить, сбросить выделение

            else:
                if game_data.game.black_player_chosen_square == "-1":
                    mtrx.get_figure_moves(int(request.POST['y']), int(request.POST['x']), "B")
                    chess_map = mtrx.matrix_to_string_conversion(include_pos_moves=True)

                    if len(mtrx.pos_moves) > 0:
                        game_data.game.black_player_chosen_square = str(request.POST['y']) + str(request.POST['x'])
                        game_data.game.chessboard_position = chess_map
                        game_data.game.save()
                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)
                else:
                    chosen_y = int(request.POST['y'])
                    chosen_x = int(request.POST['x'])
                    prev_chosen_y = int(game_data.game.black_player_chosen_square[0])
                    prev_chosen_x = int(game_data.game.black_player_chosen_square[1])
                    if game_data.game.chessboard_position[64 + chosen_y * 8 + chosen_x] == '2':
                        turn_type = "Correct"

                        mtrx.pieces_on_board[chosen_y][chosen_x] = mtrx.pieces_on_board[prev_chosen_y][prev_chosen_x]
                        mtrx.pieces_on_board[prev_chosen_y][prev_chosen_x] = EmptyPiece()
                        chess_map = mtrx.matrix_to_string_conversion()

                        game_data.game.chessboard_position = chess_map
                        game_data.game.black_player_chosen_square = "-1"
                        game_data.game.turn += 1
                        game_data.game.save()
                    else:
                        mtrx.pos_moves.clear()
                        mtrx.get_figure_moves(chosen_y, chosen_x, "B")
                        chess_map = mtrx.matrix_to_string_conversion(include_pos_moves=True)
                        game_data.game.chessboard_position = chess_map
                        if len(mtrx.pos_moves) > 0:
                            game_data.game.black_player_chosen_square = str(request.POST['y']) + str(request.POST['x'])
                        else:
                            game_data.game.black_player_chosen_square = -1
                        game_data.game.save()

                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)
                    # выбрать фигуру которая была нажата до этого, и если нажатая координата находится в сете доступных ходов, сходить, сбросить выделение

        # mtrx.collect_all_possible_moves(request.session["botColor"])
        # mtrx.make_a_move(mtrx.pick_a_move())
        # a = mtrx.matrix_to_string_conversion()
        return JsonResponse(json.dumps({"turnType": turn_type,
                                        "map": "rnbkqbnrpppppppp1111111111r111111111111111111111PPPPPPPPRNBQKBNR1112200000000000000000000000000000000000000000000000000000000000"}),
                            safe=False)
    else:
        cur_game = GameParticipants.objects.filter(user_id=request.session['id'], game__result="active").select_related(
            "user").select_related(
            "game")

        pos_str = basic_matrix2D
        player1 = {"name": name, "avatar": "main/img/person.svg", "rating": random.randint(200, 1600)}
        botArtem = {"name": "Bot Artem v0.1", "avatar": "main/img/robot.svg", "rating": '200'}
        botColor = request.session['botColor']
        for item in cur_game:
            pos_str = item.game.chessboard_position
            player1 = {"name": item.user.nickname, "avatar": "main/img/person.svg", "rating": item.user.rating_elo}
            break
        return render(request, 'main/field.html', {'player1': player1, 'player2': botArtem, 'startMap': pos_str,'botColor': botColor, 'enemyType': "bot"})


def rules(request):
    name = ""
    if "auth" in request.session:
        if request.session["auth"]:
            name = request.session["name"]
    return render(request, 'main/rules.html', {'name': name, "url_avatar": "main/img/person.svg"})
