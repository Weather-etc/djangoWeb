from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
web_path = "./templates/robot.html"


def content(request):
    with open(web_path, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read())
