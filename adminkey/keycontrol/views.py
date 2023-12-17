from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from .models import Auditorium, KeyTransfer, Employee, ByIDTakedKey, IDCard, EmployeeIDCard
from django.shortcuts import render

def index(request):
    key_records = ByIDTakedKey.objects.all()
    rows = []
    for record in key_records:
        rows.append({
            'full_name': f"{record.IDCard.employee.first_name} {record.IDCard.employee.last_name}",
            'date': record.take_time.date(),
            'time_received': record.take_time.strftime('%H:%M %p'),
            'auditorium_key': record.auditorium.room_number,
            'return_time': record.return_time.strftime('%H:%M %p'),
        })

    return render(request, 'keycontrol/index.html', {'rows': rows})

def login(request):
    return render(request, 'keycontrol/login.html')

def profile(request):
    return render(request, 'keycontrol/profile.html')

def tools(request):
    return render(request, 'keycontrol/tools.html')

def addemp(request):
    return render(request, 'keycontrol/addemp.html')

def all_info(request):
    return render(request, 'keycontrol/all_info.html')

def roles_info(request):
    return render(request, 'keycontrol/roles_info.html')

def audience_info(request):
    return render(request, 'keycontrol/audience_info.html')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")