# Generated by Django 4.2.6 on 2023-11-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_users_rating_elo_alter_users_rating_puzzles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='games',
            name='black_player',
        ),
        migrations.RemoveField(
            model_name='games',
            name='white_player',
        ),
        migrations.AddField(
            model_name='gameparticipants',
            name='user_color',
            field=models.CharField(default='W'),
        ),
    ]