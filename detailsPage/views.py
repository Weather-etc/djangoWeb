from django.shortcuts import render
import requests

# Create your views here.


def show_detail(request):
    print(request.GET)
    return render(request, "detailPage.html", {})
