from django.db import models


class GameParticipants(models.Model):
    participant_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.SET_NULL, blank=True, null=True)
    game = models.ForeignKey('Games', models.SET_NULL, blank=True, null=True)


class Games(models.Model):
    id = models.BigIntegerField(primary_key=True)
    white_player = models.CharField(blank=True, null=True)
    black_player = models.CharField(blank=True, null=True)
    finished = models.BooleanField(blank=True, null=True)
    result = models.BigIntegerField(blank=True, null=True)
    white_player_chosen_square = models.CharField(blank=True, null=True)
    black_player_chosen_square = models.CharField(blank=True, null=True)


class MoveHistory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    move = models.CharField(blank=True, null=True)
    match = models.ForeignKey(Games, models.SET_NULL, db_column='match_Id', blank=True, null=True)  # Field name made lowercase.


class PuzzleProgress(models.Model):
    id = models.BigIntegerField(primary_key=True)
    current_move = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey('Users', models.SET_NULL, blank=True, null=True)
    puzzle = models.ForeignKey('Puzzles', models.SET_NULL, blank=True, null=True)


class PuzzleSolutions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    puzzle = models.ForeignKey('Puzzles', models.SET_NULL, blank=True, null=True)
    move = models.CharField(blank=True, null=True)


class Puzzles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    starting_position = models.CharField(blank=True, null=True)
    difficulty = models.BigIntegerField(blank=True, null=True)


class SolvedPuzzles(models.Model):
    id = models.BigIntegerField(primary_key=True)
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
    role = models.TextField(blank=True, null=True)  # This field type is a guess.

