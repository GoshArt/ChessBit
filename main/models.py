import datetime

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Gameparticipants(models.Model):
    participantid = models.BigIntegerField(db_column='ParticipantID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserID', blank=True,
                               null=True)  # Field name made lowercase.
    gameid = models.ForeignKey('Games', models.DO_NOTHING, db_column='GameID', blank=True,
                               null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GameParticipants'


class Games(models.Model):
    id = models.BigIntegerField(primary_key=True)
    whiteplayer = models.TextField(db_column='WhitePlayer', blank=True,
                                   null=True)  # Field name made lowercase. This field type is a guess.
    blackplayer = models.TextField(db_column='BlackPlayer', blank=True,
                                   null=True)  # Field name made lowercase. This field type is a guess.
    finished = models.BooleanField(db_column='Finished', blank=True, null=True)  # Field name made lowercase.
    result = models.BigIntegerField(db_column='Result', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Games'


class Movehistory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    move = models.TextField(db_column='Move', blank=True,
                            null=True)  # Field name made lowercase. This field type is a guess.
    matchid = models.ForeignKey(Games, models.DO_NOTHING, db_column='MatchId', blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MoveHistory'


class Puzzleprogress(models.Model):
    id = models.BigIntegerField(primary_key=True)
    currentmove = models.BigIntegerField(db_column='CurrentMove', blank=True, null=True)  # Field name made lowercase.
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId', blank=True,
                               null=True)  # Field name made lowercase.
    puzzleid = models.ForeignKey('Puzzles', models.DO_NOTHING, db_column='PuzzleId', blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PuzzleProgress'


class Puzzlesolutions(models.Model):
    id = models.BigIntegerField(primary_key=True)
    puzzleid = models.ForeignKey('Puzzles', models.DO_NOTHING, db_column='PuzzleId', blank=True,
                                 null=True)  # Field name made lowercase.
    move = models.TextField(db_column='Move', blank=True,
                            null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'PuzzleSolutions'


class Puzzles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    startingposition = models.TextField(db_column='StartingPosition', blank=True,
                                        null=True)  # Field name made lowercase. This field type is a guess.
    difficulty = models.BigIntegerField(db_column='Difficulty', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Puzzles'


class Solvedpuzzles(models.Model):
    id = models.BigIntegerField(primary_key=True)
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='UserId', blank=True,
                               null=True)  # Field name made lowercase.
    puzzleid = models.ForeignKey(Puzzles, models.DO_NOTHING, db_column='PuzzleId', blank=True,
                                 null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SolvedPuzzles'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True)
    password = models.CharField(db_column='Password', blank=True, null=True)
    nickname = models.CharField(db_column='Nickname')  # Field name made lowercase. This field type is a guess.
    email = models.CharField(db_column='Email', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    yearofbirth = models.BigIntegerField(db_column='YearOfBirth', blank=True, null=True)  # Field name made lowercase.
    ratingelo = models.BigIntegerField(db_column='RatingELO', blank=True, null=True)  # Field name made lowercase.
    ratingpuzzles = models.BigIntegerField(db_column='RatingPuzzles', blank=True,
                                           null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Users'
