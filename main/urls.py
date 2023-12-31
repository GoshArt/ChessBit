from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('profile', views.profile),
    path('servers', views.servers),
    path('field', views.field),
    path('waiting', views.waiting),
    path('rules', views.rules),
]
