from django.http import HttpResponse


def index(request):
    with open('./templates/index.html', 'r', encoding='utf-8') as f:
        file = f.read()
    return HttpResponse(file)
