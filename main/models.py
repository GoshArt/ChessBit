from django.db import models
from main.GameLogic.create_basic_matrix import basic_matrix2D
from main.model_choises import *

class GameParticipants(models.Model):
    participant_id = models.BigAutoField(primary_key=True)
    user_color = models.CharField(default='W')
    user = models.ForeignKey('Users', models.SET_NULL, blank=True, null=True)
    game = models.ForeignKey('Games', models.SET_NULL, blank=True, null=True)


class Games(models.Model):
    id = models.BigAutoField(primary_key=True)
    result = models.CharField(choices=GAME_RES.GAME_RESULT_CHOISES, default=GAME_RES.ACTIVE)
    turn = models.BigIntegerField(default=1)
    white_player_chosen_square = models.CharField(default="-1")
    black_player_chosen_square = models.CharField(default="-1")
    chessboard_position = models.CharField(default=basic_matrix2D)


class MoveHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    move = models.CharField(blank=True, null=True)
    match = models.ForeignKey(Games, models.SET_NULL, db_column='match_Id', blank=True,
                              null=True)  # Field name made lowercase.


class PuzzleProgress(models.Model):
    id = models.BigAutoField(primary_key=True)
    current_move = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey('Users', models.SET_NULL, blank=True, null=True)
    puzzle = models.ForeignKey('Puzzles', models.SET_NULL, blank=True, null=True)


class PuzzleSolutions(models.Model):
    id = models.BigAutoField(primary_key=True)
    puzzle = models.ForeignKey('Puzzles', models.SET_NULL, blank=True, null=True)
    move = models.CharField(blank=True, null=True)


class Puzzles(models.Model):
    id = models.BigAutoField(primary_key=True)
    starting_position = models.CharField(blank=True, null=True)
    difficulty = models.BigIntegerField(blank=True, null=True)


class SolvedPuzzles(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.SET_NULL, blank=True, null=True)
    puzzle = models.ForeignKey(Puzzles, models.SET_NULL, blank=True, null=True)


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField()
    email = models.CharField(blank=True, null=True)
    year_of_birth = models.BigIntegerField(blank=True, null=True)
    rating_elo = models.BigIntegerField(blank=True, null=True, default=1200)
    rating_puzzles = models.BigIntegerField(blank=True, null=True, default=1200)
    password = models.CharField(blank=True, null=True)
    role = models.CharField(choices=USER_ROLES.USER_ROLE_CHOISES, default=USER_ROLES.USER)  # This field type is a guess.
