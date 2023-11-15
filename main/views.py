from random import random

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.GameLogic.create_basic_matrix import *
from main.bd_logic import *
from .models import *
from django.utils.html import escape
import random
import json


def index(request):
    auth = False
    name = "Гость"
    url_avatar = 'main/img/person.svg'
    error = ""

    best_players = []
    best_players_db = Users.objects.order_by('rating_elo').reverse().all()
    p = 1
    for player in best_players_db:
        best_players.append({"name": player.nickname, "res": player.rating_elo})
        if p == 10:
            break
        p += 1
    if request.method == "GET":
        pass
    elif request.method == "POST":
        if "username" in request.POST:

            username = request.POST["username"]
            username = escape(username)
            password = request.POST["password"]
            password = escape(password)
            user = Users.objects.filter(nickname=username, password=password).first()
            if user:
                request.session['auth'] = True
                request.session['name'] = username
                request.session['password'] = password
                request.session['id'] = user.id
            else:
                return render(request, 'main/index.html',
                              {"name": "Гость", "url_avatar": url_avatar, "auth": False, "error": error,
                               "best_players": best_players, "loginError": "Данные введены неверно",
                               "register_error": ""})

        elif "re_password" in request.POST:
            name = escape(request.POST["name"])
            email = escape(request.POST["email"])
            f_password = escape(request.POST["f_password"])
            re_password = escape(request.POST["re_password"])
            register_error = ""
            if len(name) < 3:
                register_error = "Слишком короткое имя пользователя"
            elif len(name) > 20:
                register_error = "Слишком длинное имя пользователя"
            elif len(f_password) < 3:
                register_error = "Слишком короткий пароль"
            elif len(f_password) > 20:
                register_error = "Слишком длинный пароль"
            elif len(Users.objects.filter(nickname=name)) > 0:
                register_error = "Такой пользователь уже существует"
            elif len(Users.objects.filter(email=email)) > 0:
                register_error = "Данный email уже занят"
            elif f_password != re_password:
                register_error = "Пароли не сходятся, как и мои ряды"
            print(register_error)
            if register_error != "":
                return render(request, 'main/index.html',
                              {"name": "Гость", "url_avatar": url_avatar, "auth": False, "error": error,
                               "best_players": best_players, "loginError": "",
                               "registerError": register_error})
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
            if len(Users.objects.filter(nickname='Bot Artem v0.1')) == 0:
                bot = Users.objects.create(nickname='Bot Artem v0.1', role='bot', rating_elo=2000)
                bot.save()
            print("size : ", len(GameParticipants.objects.filter(user_id=request.session['id'], game__result="active")))
            if len(GameParticipants.objects.filter(user_id=request.session['id'], game__result="active")) == 0:
                bot_data = Users.objects.get(nickname='Bot Artem v0.1')
                user_data = Users.objects.get(id=request.session['id'])
                new_game = Games.objects.create(result=GAME_RES.ACTIVE)
                new_game.save()
                print(request.POST['chosenColor'])
                participant1 = GameParticipants.objects.create(game_id=new_game.id, user_id=user_data.id,
                                                               user_color=request.POST['chosenColor'])
                participant2 = GameParticipants.objects.create(game_id=new_game.id, user_id=bot_data.id,
                                                               user_color=request.POST['chosenColor'])
                print(request.POST['chosenColor'])
                if request.POST['chosenColor'] == 'B':
                    participant1.user_color = "W"
                else:
                    participant1.user_color = "B"
                participant1.save()
                participant2.save()

            return redirect(field)

        elif len(request.POST) < 2:
            request.session['auth'] = False
            request.session['name'] = ""
            request.session['password'] = ""
            request.session['id'] = ""
            print("done")

    print(name)
    if "auth" in request.session:
        if request.session["auth"] == True:
            auth = True
            name = request.session["name"]
    print(name)
    # best_players = sorted(best_players, key=lambda x: x['res'], reverse=True)
    return render(request, 'main/index.html',
                  {"name": name, "url_avatar": url_avatar, "auth": auth, "error": error, "best_players": best_players,
                   "loginError": "", "register_error": ""})


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
            print("Result:", games_data.game.result)
            print("MainUserNickName", name + " VS " + enemy_guy.user.nickname)
            versus = name + "VS" + enemy_guy.user.nickname
            print(versus)
            left_part = games_data.user_color
            left_result = games_data.game.result
            print("wildsexwildsexwildsex")
            print(left_part)
            print(left_result)
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
        return render(request, 'main/profile.html',
                      {"games": games, "id": id, "rating": rating, "name": name,
                       "url_avatar": url_avatar,
                       "email": email,
                       "reg": reg})

    if request.method == "POST":
        if "username" in request.POST:
            print(1)
            pos = Users.objects.get(nickname=request.session["name"])
            name = request.POST['username']
            renaming_error = ""
            if len(name) < 3:
                renaming_error = "Слишком короткое имя пользователя"
            elif len(name) > 20:
                renaming_error = "Слишком длинное имя пользователя"
            elif len(Users.objects.filter(nickname=name)) > 0:
                renaming_error = "Такой пользователь уже существует"
            if renaming_error == "":
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
        if request.POST['type'] == 'gaveUp':
            game_finished = -1
            if game_data.game.turn % 2 == 0:
                game_finished = 1

            game_players = GameParticipants.objects.filter(game_id=game_data.game_id).select_related('user')
            for player in game_players:
                if player.user.id == request.session['id']:
                    player.user.rating_elo -= 20
                else:
                    player.user.rating_elo += 20
                player.user.save()
            game_data.game.result = game_finished
            game_data.game.save()
            chess_map = mtrx.matrix_to_string_conversion()
            return JsonResponse(json.dumps({"turnType": 'gameFinished', "map": chess_map, "res": "Lose"}), safe=False)

        elif request.POST['type'] == 'pressSquare':
            turn_type = "Selected"
            print("here")
            chess_map = ""
            if game_data.game.turn % 2 == 1:
                if game_data.game.white_player_chosen_square == "-1":
                    print("selecting")
                    # choosing given figure and returning possible places to go
                    mtrx.get_figure_moves(int(request.POST['y']), int(request.POST['x']), "W")
                    chess_map = mtrx.matrix_to_string_conversion(include_pos_moves=True)
                    if len(mtrx.pos_moves) > 0:
                        game_data.game.white_player_chosen_square = str(request.POST['y']) + str(request.POST['x'])
                        game_data.game.chessboard_position = chess_map
                        game_data.game.save()
                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)

                else:
                    print("moving2")
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

                    game_finished = mtrx.is_victory()
                    print("dude_move ", game_finished)
                    if game_finished != 2:
                        game_players = GameParticipants.objects.filter(game_id=game_data.game_id).select_related('user')
                        for player in game_players:
                            if player.user.id == request.session['id']:
                                player.user.rating_elo += 20
                            else:
                                player.user.rating_elo -= 20
                            player.user.save()
                        game_data.game.result = game_finished
                        game_data.game.save()
                        return JsonResponse(
                            json.dumps({"turnType": 'gameFinished', "map": chess_map, "res": "Win"}), safe=False)

                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)
                    # выбрать фигуру которая была нажата до этого, и если нажатая координата находится в сете доступных ходов, сходить, сбросить выделение

            else:
                if game_data.game.black_player_chosen_square == "-1":
                    print("selecting")
                    mtrx.get_figure_moves(int(request.POST['y']), int(request.POST['x']), "B")
                    chess_map = mtrx.matrix_to_string_conversion(include_pos_moves=True)

                    if len(mtrx.pos_moves) > 0:
                        game_data.game.black_player_chosen_square = str(request.POST['y']) + str(request.POST['x'])
                        game_data.game.chessboard_position = chess_map
                        game_data.game.save()
                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)
                else:
                    print("moving")
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

                    game_finished = mtrx.is_victory()
                    print("dude_move ", game_finished)
                    if game_finished != 2:
                        game_players = GameParticipants.objects.filter(game_id=game_data.game_id).select_related('user')
                        for player in game_players:
                            if player.user.id == request.session['id']:
                                player.user.rating_elo += 20
                            else:
                                player.user.rating_elo -= 20
                            player.user.save()
                        game_data.game.result = game_finished
                        game_data.game.save()

                        return JsonResponse(json.dumps({"turnType": 'gameFinished', "map": chess_map, "res": "Win"}),
                                            safe=False)

                    return JsonResponse(json.dumps({"turnType": turn_type, "map": chess_map}), safe=False)
                    # выбрать фигуру, которая была нажата до этого, и если нажатая координата находится в сете доступных ходов, сходить, сбросить выделение
        elif request.POST['type'] == 'goMoveBot':
            if game_data.game.turn % 2 == 1:
                mtrx.collect_all_possible_moves('W')
            else:
                mtrx.collect_all_possible_moves('B')

            move = mtrx.pick_a_move()

            mtrx.make_a_move(move)

            map = mtrx.matrix_to_string_conversion()
            game_data.game.chessboard_position = map
            game_data.game.turn += 1
            game_data.game.save()

            game_finished = mtrx.is_victory()
            print("bot_move ", game_finished)
            if game_finished != 2:
                game_players = GameParticipants.objects.filter(game_id=game_data.game_id).select_related('user')
                for player in game_players:
                    if player.user.id == request.session['id']:
                        player.user.rating_elo -= 20
                    else:
                        player.user.rating_elo += 20
                    player.user.save()
                game_data.game.result = game_finished
                game_data.game.save()

                return JsonResponse(json.dumps({"turnType": 'gameFinished', "map": map, "res": "Lose"}), safe=False)

            return JsonResponse(json.dumps({"turnType": 'botMove', "map": map}), safe=False)
        else:
            print("какого черта это сюда попало")
    else:
        cur_game = GameParticipants.objects.filter(user_id=request.session['id'], game__result="active").select_related(
            "user").select_related(
            "game")

        pos_str = basic_matrix2D
        player1 = {"name": name, "avatar": "main/img/person.svg", "rating": random.randint(200, 1600)}
        if len(Users.objects.filter(nickname='Bot Artem v0.1')) == 0:
            bot = Users.objects.create(nickname='Bot Artem v0.1', role='bot', rating_elo=2000)
            bot.save()
        bot = Users.objects.get(nickname='Bot Artem v0.1')
        botArtem = {"name": bot.nickname, "avatar": "main/img/robot.svg", "rating": bot.rating_elo}
        botColor = request.session['botColor']
        for item in cur_game:
            pos_str = item.game.chessboard_position
            player1 = {"name": item.user.nickname, "avatar": "main/img/person.svg", "rating": item.user.rating_elo}
            break

        return render(request, 'main/field.html', {'player1': player1, 'player2': botArtem, 'startMap': pos_str,
                                                   'botColor': botColor, 'enemyType': "Bot",
                                                   "currentTurnIndex": 1})  # currentTurnIndex изменить единичку на чётность хода в бд


def rules(request):
    name = "Гость"
    if "auth" in request.session:
        if request.session["auth"]:
            name = request.session["name"]
    return render(request, 'main/rules.html', {'name': name, "url_avatar": "main/img/person.svg"})
