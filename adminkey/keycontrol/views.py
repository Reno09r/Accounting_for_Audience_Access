from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render

def index(request):
    data = {'title': 'Главная страница', 'cssfile': 'admin.css'}
    return render(request, 'keycontrol/index.html', context=data)

def login(request):
    return render(request, 'keycontrol/login.html')

def profile(request):
    return render(request, 'keycontrol/profile.html')

def tools(request):
    return render(request, 'keycontrol/tools.html')

def addemp(request):
    data = {'title': 'Добавление', 'cssfile': 'addemp.css'}
    return render(request, 'keycontrol/addemp.html', context=data)

def all_info(request):
    return render(request, 'keycontrol/all_info.html')

def roles_info(request):
    return render(request, 'keycontrol/roles_info.html')

def audience_info(request):
    return render(request, 'keycontrol/audience_info.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")