# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    current_turn = models.CharField(blank=True, null=True)
    white_player_chosen_square = models.CharField(blank=True, null=True)
    black_player_chosen_square = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'games'


class MoveHistory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    move = models.CharField(blank=True, null=True)
    match = models.ForeignKey(Games, models.DO_NOTHING, db_column='match_Id', blank=True, null=True)  # Field name made lowercase.

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
