from django.shortcuts import render
from django.http import HttpResponse
from chatBot.botModel.app.robot import Bot

# Create your views here.
web_path = "./templates/robot.html"


def content(request):
    bot = Bot()
    if request.GET:
        cont = request.GET['ques']
        print(cont)
        res = bot.query(cont)
        return render(request, 'robot.html', {'response': res})
    return render(request, 'robot.html', {'response': ''})
