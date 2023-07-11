from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("<h4>test</h4>")

# Create your views here.
