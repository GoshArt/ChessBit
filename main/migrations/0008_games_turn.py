# Generated by Django 4.2.6 on 2023-11-13 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_gameparticipants_participant_id_alter_games_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='turn',
            field=models.BigIntegerField(default=1),
        ),
    ]
