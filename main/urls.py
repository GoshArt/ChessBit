from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile', views.profile),
    path('servers', views.servers),
    path('field', views.field),
    path('waiting', views.waiting),
    path('rules', views.rules),
    path('rules_part1', views.rules_part1, name='rules_part1'),
    path('rules_part2', views.rules_part2, name='rules_part2'),
]
