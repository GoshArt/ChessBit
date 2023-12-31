# Generated by Django 4.2.6 on 2023-11-13 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_games_chessboard_position_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='games',
            name='finished',
        ),
        migrations.AlterField(
            model_name='games',
            name='result',
            field=models.TextField(choices=[('black_victory', 'BlackVictory'), ('white_victory', 'WhiteVictory'), ('active', 'Active'), ('aborted', 'Aborted')], default='active'),
        ),
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.TextField(choices=[('bot', 'Bot'), ('user', 'User'), ('admin', 'Admin'), ('banned', 'Banned')], default='user'),
        ),
    ]
