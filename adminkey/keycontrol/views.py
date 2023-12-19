from datetime import datetime
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect, JsonResponse
from .forms import AddEmployeeForm, DeleteAudienceForm, DeleteRoleForm, KeyRequestForm, AudienceAddForm,  DeleteAudienceForm, AddRoleForm
from .models import Auditorium, KeyTransfer, Employee, ByIDTakedKey, IDCard, EmployeeIDCard, Role
from django.shortcuts import render, redirect


def index(request):
    emps = Employee.objects.all()
    emp_choices = [(f"{emp.first_name} {emp.last_name}",
                    f"{emp.first_name} {emp.last_name}") for emp in emps]
    keys = Auditorium.objects.all()
    key_choices = [(key.room_number, key.room_number) for key in keys]
    
    form = KeyRequestForm(request.POST, emp_choices=emp_choices, key_choices=key_choices)
    
    if request.method == 'POST' and form.is_valid():
        emp = form.cleaned_data['emp_choose']
        key = form.cleaned_data['key_choose']
        return_time = form.cleaned_data['return_time']
        today = datetime.now()
        return_time_str = today.strftime("%Y-%m-%d") + ' ' + return_time.strftime('%H:%M')

        existing_key_entries = ByIDTakedKey.objects.filter(
            IDCard__employee__first_name=emp.split()[0],
            IDCard__employee__last_name=emp.split()[1],
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
        emp_id_card = EmployeeIDCard.objects.get(employee=employee)
        ByIDTakedKey.objects.create(IDCard=emp_id_card, auditorium=key, take_time=today,
                                    return_time=return_time_str, key_transferred=False, is_returned=False)

    key_records = ByIDTakedKey.objects.all()
    rows = [{
        'full_name': f"{record.IDCard.employee.first_name} {record.IDCard.employee.last_name}",
        'date': record.take_time.date(),
        'time_received': record.take_time.strftime('%H:%M'),
        'auditorium_key': record.auditorium.room_number,
        'return_time': record.return_time.strftime('%H:%M'),
    } for record in key_records]

    return render(request, 'keycontrol/index.html', {'rows': rows, 'form': form})

def mark_returned(request):
    if request.method == 'POST' and request.is_ajax():
        selected_ids = request.POST.getlist('selected_ids[]')
        for row_id in selected_ids:
            ByIDTakedKey.objects.filter(id=row_id).update(is_returned=True)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})



def login(request):
    return render(request, 'keycontrol/login.html')


def profile(request):
    return render(request, 'keycontrol/profile.html')


def tools(request):
    keys = Auditorium.objects.all()
    key_choices = [(key.room_number, key.room_number) for key in keys]
    roles = Role.objects.all()
    role_choices = [(role.role_name, role.role_name) for role in roles]
    AddAudienceform = AudienceAddForm()
    AddRoleform = AddRoleForm()
    DeleteAudienceform = DeleteAudienceForm(key_choices=key_choices)
    DeleteRoleform = DeleteRoleForm(role_choices=role_choices)
    if request.method == 'POST':
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
            DeleteAudienceform = DeleteAudienceForm(request.POST, key_choices=key_choices)
            if DeleteAudienceform.is_valid():
                key = DeleteAudienceform.cleaned_data['key_selected']
                auditorium_to_delete = Auditorium.objects.filter(room_number=key)
                auditorium_to_delete.delete()
        if 'DeleteRoleForm' in request.POST:
            DeleteRoleform = DeleteRoleForm(request.POST, role_choices=role_choices)
            if DeleteRoleform.is_valid():
                role = DeleteRoleform.cleaned_data['role_selected']
                role_to_delete = Role.objects.filter(role_name=role)
                role_to_delete.delete()
        return redirect(request.path)

    context = {
        'AddAudienceForm': AddAudienceform,
        'AddRoleForm': AddRoleform,
        'DeleteAudienceForm': DeleteAudienceform,
        'DeleteRoleForm': DeleteRoleform
    }
    return render(request, 'keycontrol/tools.html', context=context)


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
            emp = Employee.objects.create(
                role=role_obj, birthday=date_of_birth, first_name=fn, last_name=ln, email=email, phone=phone_number)
            idc = IDCard.objects.create(code=employee_card_id)
            EmployeeIDCard.objects.create(employee_id=emp.pk, IDCard=idc)

    return render(request, 'keycontrol/addemp.html', {'form': form})


def all_info(request):
    key_records = Employee.objects.all()
    rows = []
    for record in key_records:
        rows.append({
            'full_name': f"{record.first_name} {record.last_name}",
            'birthday': record.birthday,
            'email': record.email,
            'phone': record.phone,
            'role': record.role.role_name,
            'cardID': EmployeeIDCard.objects.get(employee=record).IDCard.code,
        })

    return render(request, 'keycontrol/all_info.html', {'rows': rows})


def roles_info(request):
    key_records = Role.objects.all()
    rows = []
    for record in key_records:
        rows.append({
            'role': record.role_name
        })
    return render(request, 'keycontrol/roles_info.html', {'rows': rows})


def audience_info(request):
    key_records = Auditorium.objects.all()
    rows = []
    for record in key_records:
        rows.append({
            'audience': record.room_number
        })
    return render(request, 'keycontrol/audience_info.html', {'rows': rows})


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
