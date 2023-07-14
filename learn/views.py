from django.shortcuts import render
from django.http import HttpResponse

from .models import Course

# Create your views here.
def index(request):
    return  HttpResponse("hello world")


def courses(request):
    users = Course.objects.all()
    s = ""
    for user in users:
        s += str(user)
        s += '</br>'
    return HttpResponse(s)


def test(request):
    with open('./templates/index.html', 'r', encoding='utf-8') as f:
        s = f.read()
    return HttpResponse(s)
