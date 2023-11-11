from django.db import models


class GameParticipants(models.Model):
    participant_id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    game = models.ForeignKey('Games', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'game_participants'


class Games(models.Model):
    id = models.BigIntegerField(primary_key=True)
    white_player = models.CharField(blank=True, null=True)
    black_player = models.CharField(blank=True, null=True)
    finished = models.BooleanField(blank=True, null=True)
    result = models.BigIntegerField(blank=True, null=True)
    white_player_chosen_square = models.CharField(blank=True, null=True)
    black_player_chosen_square = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'games'


class MoveHistory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    move = models.CharField(blank=True, null=True)
    match = models.ForeignKey(Games, models.DO_NOTHING, db_column='match_Id', blank=True,
                              null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'move_history'


class PuzzleProgress(models.Model):
    id = models.BigIntegerField(primary_key=True)
    current_move = models.BigIntegerField(blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    puzzle = models.ForeignKey('Puzzles', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puzzle_progress'


class PuzzleSolutions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    puzzle = models.ForeignKey('Puzzles', models.DO_NOTHING, blank=True, null=True)
    move = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puzzle_solutions'


class Puzzles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    starting_position = models.CharField(blank=True, null=True)
    difficulty = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puzzles'


class SolvedPuzzles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    puzzle = models.ForeignKey(Puzzles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solved_puzzles'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    nickname = models.CharField()
    email = models.CharField(blank=True, null=True)
    year_of_birth = models.BigIntegerField(blank=True, null=True)
    rating_elo = models.BigIntegerField(blank=True, null=True)
    rating_puzzles = models.BigIntegerField(blank=True, null=True)
    password = models.CharField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'users'
