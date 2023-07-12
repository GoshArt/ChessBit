from django.shortcuts import render
from django.http import HttpResponse
from .models import Gosha


def index(request):
    goshas = Gosha.objects.all()
    return render(request, 'main/index.html', {'goshas': goshas})


def about(request):
    return render(request, 'main/about.html')

# Create your views here.
