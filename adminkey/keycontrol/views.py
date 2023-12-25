from datetime import datetime
import json
import csv
from django.forms import ValidationError
from django.db.models import Q
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from .forms import DeleteItemForm, SearchForm, AddScheduleForm, SearchAdminForm, ChangeEmployeeIDCardForm, ChangeEmployeeFullNameForm, AddEmployeeForm, KeyRequestForm, AudienceAddForm, AddRoleForm
from .models import Auditorium, Schedule, Employee, ByIDTakedKey, Role
from django.shortcuts import render, redirect

@login_required
def index(request):
    emps = Employee.objects.all()
    emp_choices = [(f"{emp.first_name} {emp.last_name}",
                    f"{emp.first_name} {emp.last_name}") for emp in emps]
    keys = Auditorium.objects.all()
    key_choices = [(key.room_number, key.room_number) for key in keys]
    
    form = KeyRequestForm(request.POST, emp_choices=emp_choices, key_choices=key_choices)
    search_form = SearchAdminForm(request.GET)
    key_records = ByIDTakedKey.objects.all()
    if request.method == 'POST' and form.is_valid():
        emp = form.cleaned_data['emp_choose']
        key = form.cleaned_data['key_choose']
        return_time = form.cleaned_data['return_time']
        today = datetime.now()
        return_time_str = today.strftime("%Y-%m-%d") + ' ' + return_time.strftime('%H:%M')

        existing_key_entries = ByIDTakedKey.objects.filter(
            employee_id__first_name=emp.split()[0],
            employee_id__last_name=emp.split()[1],
            is_returned=False
        ).count()

        existing_key_entry = ByIDTakedKey.objects.filter(
            auditorium__room_number=key,
            is_returned=False
        ).first()

        if existing_key_entry:
            raise ValidationError("Ключ используется.")
        employee = Employee.objects.get(first_name=emp.split()[0], last_name=emp.split()[1])

        if not employee.role.is_master and existing_key_entries >= 1:
            raise ValidationError("Роль данного сотрудника не позволяет использовать больше одного ключа.")
        key = Auditorium.objects.get(room_number=key)
        ByIDTakedKey.objects.create(employee_id=employee, auditorium=key, take_time=today,
                                    return_time=return_time_str, key_transferred=False, is_returned=False)
        return redirect('home')
    elif request.method == 'GET' and search_form.is_valid():
        search_full_name =search_form.cleaned_data['search_full_name']
        
        search_auditorium = search_form.cleaned_data['search_auditorium']
        if search_full_name:
            key_records = key_records.filter(Q(employee_id__first_name__icontains= search_full_name) | Q(employee_id__last_name__icontains= search_full_name))
        if search_auditorium:
            key_records = key_records.filter(auditorium__room_number__icontains=search_auditorium)
    
    rows = [{
        'id': record.id,
        'full_name': f"{record.employee_id.first_name} {record.employee_id.last_name}",
        'date': record.take_time.date(),
        'time_received': record.take_time.strftime('%H:%M'),
        'auditorium_key': record.auditorium.room_number,
        'return_time': record.return_time.strftime('%H:%M'),
        'is_returned': record.is_returned
    } for record in key_records]
    context = {
        'KeyRequestForm': form,
        'SearchAdminForm': search_form,
        'rows': rows,
    }
    return render(request, 'keycontrol/index.html', context)

def mark_returned(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        selected_ids = data.get('selected_ids', [])
        for row_id in selected_ids:
            ByIDTakedKey.objects.filter(id=int(row_id)).update(is_returned=True)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def mark_delete(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        selected_ids = data.get('selected_ids', [])
        for row_id in selected_ids:
            Schedule.objects.filter(id=int(row_id)).delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})    


@login_required
def profile(request):
    user = request.user

    # Now you can use user attributes, for example:
    username = user.username
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    # You can pass these variables to the template
    context = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
    }

    return render(request, 'keycontrol/profile.html', context)

@login_required
def tools(request):
    keys = Auditorium.objects.all()
    key_choices = [(key.room_number, key.room_number) for key in keys]
    roles = Role.objects.all()
    role_choices = [(role.role_name, role.role_name) for role in roles]
    emps = Employee.objects.all()
    emp_choices = [(f"{emp.first_name} {emp.last_name}",
                    f"{emp.first_name} {emp.last_name}") for emp in emps]
    ChangeEmployeeIDCardform =ChangeEmployeeIDCardForm(emp_choices=emp_choices)
    ChangeEmployeeFullNameform = ChangeEmployeeFullNameForm(emp_choices=emp_choices)
    AddAudienceform = AudienceAddForm()
    AddRoleform = AddRoleForm()
    DeleteEmployeeform = DeleteItemForm(lbl_name='Поиск по ФИО', lbl_ch_name='Выберите сотрудника...', item_choices=emp_choices)
    DeleteAudienceform = DeleteItemForm(lbl_name='Номер от аудитории', lbl_ch_name='Выберите аудиторию...', item_choices=key_choices)
    DeleteRoleform = DeleteItemForm(lbl_name='Имя роли', lbl_ch_name='Выберите роль...', item_choices=role_choices)
    if request.method == 'POST':
        if 'ChangeEmployeeFullNameForm' in request.POST:
            ChangeEmployeeFullNameform = ChangeEmployeeFullNameForm(request.POST, emp_choices=emp_choices)
            if ChangeEmployeeFullNameform.is_valid():
                first_name, last_name = ChangeEmployeeFullNameform.cleaned_data['emp_selected'].split()
                new_first_name, new_last_name = ChangeEmployeeFullNameform.cleaned_data['full_name'].split()
                employee = Employee.objects.filter(first_name=first_name, last_name=last_name).first()
                employee.first_name = new_first_name
                employee.last_name = new_last_name
                employee.save()
        if 'ChangeEmployeeIDCardForm' in request.POST:
            ChangeEmployeeIDCardform = ChangeEmployeeIDCardForm(request.POST, emp_choices=emp_choices)
            if ChangeEmployeeIDCardform.is_valid():
                first_name, last_name = ChangeEmployeeIDCardform.cleaned_data['emp_selected'].split()
                employee = Employee.objects.filter(first_name=first_name, last_name=last_name).first()
                if employee:
                    employee.id_card_code = ChangeEmployeeIDCardform.cleaned_data['id_card']
                    employee.save()
        if 'DeleteEmployeeForm' in request.POST:
            DeleteEmployeeform = DeleteItemForm(request.POST, lbl_name='Поиск по ФИО', lbl_ch_name='Выберите сотрудника...', item_choices=emp_choices)
            if DeleteEmployeeform.is_valid():
                first_name, last_name =  DeleteEmployeeform.cleaned_data['item_selected'].split()
                employee = Employee.objects.filter(first_name=first_name, last_name=last_name).first()
                tk = ByIDTakedKey.objects.filter(employee_id = employee.id)
                tk.delete()
                employee.delete()
        if 'AddAudienceForm' in request.POST:
            AddAudienceform = AudienceAddForm(request.POST)
            if AddAudienceform.is_valid():
                key = AddAudienceform.cleaned_data['key']
                Auditorium.objects.create(room_number=key)
        if 'AddRoleForm' in request.POST:
            AddRoleform = AddRoleForm(request.POST)
            if AddRoleform.is_valid():
                role = AddRoleform.cleaned_data['role_name']
                if AddRoleform.cleaned_data['key_access'] == "master":
                    is_master = False
                else:
                    is_master = True
                Role.objects.create(role_name = role, is_master = is_master)
        if 'DeleteAudienceForm' in request.POST:
            DeleteAudienceform = DeleteItemForm(request.POST, lbl_name='Номер от аудитории', lbl_ch_name='Выберите аудиторию...', item_choices=key_choices)
            if DeleteAudienceform.is_valid():
                key = DeleteAudienceform.cleaned_data['item_selected']
                auditorium_to_delete = Auditorium.objects.filter(room_number=key)
                auditorium_to_delete.delete()
        if 'DeleteRoleForm' in request.POST:
            DeleteRoleform = DeleteItemForm(request.POST, lbl_name='Имя роли', lbl_ch_name='Выберите роль...', item_choices=role_choices)
            if DeleteRoleform.is_valid():
                role = DeleteRoleform.cleaned_data['item_selected']
                role_to_delete = Role.objects.filter(role_name=role)
                role_to_delete.delete()
        return redirect(request.path)

    context = {
    'ChangeEmployeeIDCardForm': ChangeEmployeeIDCardform,
    'ChangeEmployeeFullNameForm': ChangeEmployeeFullNameform,
    'DeleteEmployeeForm': DeleteEmployeeform,
    'AddAudienceForm': AddAudienceform,
    'AddRoleForm': AddRoleform,
    'DeleteAudienceForm': DeleteAudienceform,
    'DeleteRoleForm': DeleteRoleform,
    }

    return render(request, 'keycontrol/tools.html', context=context)

@login_required
def addemp(request):
    roles = Role.objects.all()

    role_choices = [(role.role_name, role.role_name) for role in roles]

    form = AddEmployeeForm(role_choices=role_choices)

    if request.method == 'POST':
        form = AddEmployeeForm(request.POST, role_choices=role_choices)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            date_of_birth = form.cleaned_data['date_of_birth']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            employee_card_id = form.cleaned_data['employee_card_id']
            role = form.cleaned_data['role']
            fn, ln = fullname.split(maxsplit=1)
            role_obj = Role.objects.get(role_name=role)
            Employee.objects.create(
                role=role_obj, birthday=date_of_birth, id_card_code = employee_card_id, first_name=fn, last_name=ln, email=email, phone=phone_number)
        return redirect(request.path)
    return render(request, 'keycontrol/addemp.html', {'form': form})

@login_required
def all_info(request):
    form = SearchForm(request.GET)
    key_records = Employee.objects.all()
    rows = []
    if form.is_valid():
        inp = form.cleaned_data['search']
        if inp:
            key_records = Employee.objects.filter(
    Q(first_name__icontains=inp) | Q(last_name__icontains=inp)
)
    for record in key_records:
        rows.append({
            'full_name': f"{record.first_name} {record.last_name}",
            'birthday': record.birthday,
            'email': record.email,
            'phone': record.phone,
            'role': record.role.role_name,
            'cardID':record.id_card_code,
        })

    return render(request, 'keycontrol/all_info.html', {'rows': rows, 'form': form})

@login_required
def roles_info(request):
    form = SearchForm(request.GET)
    key_records = Role.objects.all()
    rows = []
    if form.is_valid():
        inp = form.cleaned_data['search']
        if inp:
            key_records =  Role.objects.filter(
    Q(role_name__icontains=inp))
    for record in key_records:
        rows.append({
            'role': record.role_name
        })
    return render(request, 'keycontrol/roles_info.html', {'rows': rows, 'form': form})

@login_required
def audience_info(request):
    form = SearchForm(request.GET)
    key_records = Auditorium.objects.all()
    rows = []
    if form.is_valid():
        inp = form.cleaned_data['search']
        if inp:
            key_records =  Auditorium.objects.filter(
    Q(room_number__icontains=inp))
    for record in key_records:
        rows.append({
            'audience': record.room_number
        })
    return render(request, 'keycontrol/audience_info.html', {'rows': rows, 'form': form})

@login_required
def upload(request):
    if request.method == 'GET':
        with open('roli.csv', 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                role = row[0].strip()  
                master = row[1].strip()
                rol = Role(role_name = role, is_master = bool(master))
                rol.save()
        with open('employee.csv', 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                role = row[5]
                role, created = Role.objects.get_or_create(role_name=role, defaults={'is_master': False})
                employee, created = Employee.objects.get_or_create(
                    email=row[3],
                    defaults={'first_name': row[0], 'last_name': row[1], 'birthday': datetime.strptime(row[2], '%d.%m.%Y').date(), 
                              'phone': row[4], 'role': role, 'id_card_code': row[6]}
                )
        with open('auditory.csv', 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                room_number = row[0].strip()  
                auditorium = Auditorium(room_number=room_number)
                auditorium.save()


    return redirect('all_info')

@login_required
def schedule(request):
    search_form = SearchAdminForm(request.GET)
    emps = Employee.objects.all()
    emp_choices = [(f"{emp.first_name} {emp.last_name}",
                    f"{emp.first_name} {emp.last_name}") for emp in emps]
    keys = Auditorium.objects.all()
    key_choices = [(key.room_number, key.room_number) for key in keys]
    
    form = AddScheduleForm(request.POST, emp_choices=emp_choices, key_choices=key_choices)
    search_form = SearchAdminForm(request.GET)
    schedule_records = Schedule.objects.all()
    if request.method == 'POST' and form.is_valid():
        emp = form.cleaned_data['emp_choose']
        key = form.cleaned_data['key_choose']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        day_of_week = form.cleaned_data['day_choose']
        employee = Employee.objects.get(first_name=emp.split()[0], last_name=emp.split()[1])
        key = Auditorium.objects.get(room_number=key)
        Schedule.objects.create(employee = employee, auditorium = key, day_of_week = day_of_week, start_time = start_time, end_time = end_time)
        return redirect('schedule')
    elif request.method == 'GET' and search_form.is_valid():
        search_full_name =search_form.cleaned_data['search_full_name']
        search_auditorium = search_form.cleaned_data['search_auditorium']
        day_of_week = search_form.cleaned_data['day_of_week']
        if search_full_name:
            schedule_records = schedule_records.filter(Q(employee_id__first_name__icontains= search_full_name) | Q(employee_id__last_name__icontains= search_full_name))
        if search_auditorium:
            schedule_records = schedule_records.filter(auditorium__room_number__icontains=search_auditorium)
        if day_of_week and day_of_week != 'Все':
            schedule_records = schedule_records.filter(day_of_week=day_of_week)   
    rows = [{
        'id': record.id,
        'full_name': f"{record.employee.first_name} {record.employee.last_name}",
        'key': record.auditorium.room_number,
        'start_time': record.start_time.strftime('%H:%M'),
        'end_time': record.end_time.strftime('%H:%M'),
        "day_of_week": record.day_of_week
    } for record in schedule_records]
    context = {
        'SearchAdminForm': search_form,
        'AddScheduleForm': form,
        'rows': rows
    }
    if 'day_of_week' in request.GET:
        return JsonResponse({'rows': rows})
    return render(request, 'keycontrol/schedule.html', context)
