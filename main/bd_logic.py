from .models import *


def find_user_data_by_name(name):
    return Users.objects.get(nickname=name)


def find_user_data_by_id(user_id):
    return Users.objects.get(id=user_id)
