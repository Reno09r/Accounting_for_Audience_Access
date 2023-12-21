# forms.py
from django import forms


class AddEmployeeForm(forms.Form):
    fullname = forms.CharField(label='Полное ФИО сотрудника', required=True)
    date_of_birth = forms.DateField(
        label='Дата рождения', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(
        label='Номер телефона', required=True, widget=forms.TextInput(attrs={'type': 'tel'}))
    email = forms.EmailField(label='Почта сотрудника', required=True)
    employee_card_id = forms.CharField(
        label='ID карточка сотрудника', required=True)
    role = forms.ChoiceField(label='Роль', choices=[], required=True)

    def __init__(self, *args, **kwargs):
        role_choices = kwargs.pop('role_choices', [])
        super(AddEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = role_choices


class KeyRequestForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'ФИО'}), required=False
    )
    emp_choose = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'required': True})
    )
    key = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Ключ'}), required=False
    )
    key_choose = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'required': True})
    )
    return_time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'placeholder': 'Время возврата', 'required': True})
    )

    def __init__(self, *args, **kwargs):
        emp_choices = kwargs.pop('emp_choices', [])
        key_choices = kwargs.pop('key_choices', [])
        super(KeyRequestForm, self).__init__(*args, **kwargs)
        self.fields['emp_choose'].choices = emp_choices
        self.fields['key_choose'].choices = key_choices


class AudienceAddForm(forms.Form):
    key = forms.CharField(label='Номер от аудитории', widget=forms.TextInput(attrs={'placeholder': 'Номер'}), required=True)

class AddRoleForm(forms.Form):
    role_name = forms.CharField(label='Имя роли', widget=forms.TextInput(attrs={'placeholder': 'Имя'}), required=True)
    key_access = forms.ChoiceField(
        label='Доступ к ключу',
        choices=[('master', 'Мастер ключ'), ('alone', 'Одиночный ключ')],
        widget=forms.RadioSelect(attrs={'class': 'radio_key'}),
        required=True
    )

class DeleteAudienceForm(forms.Form):
    key_name = forms.CharField(label='Номер от аудитории', widget=forms.TextInput(attrs={'placeholder': 'Номер'}), required=False)
    key_selected = forms.ChoiceField(
        label='Выберите аудиторию...',
        choices=[],
        widget=forms.Select(attrs={'required': True})
    )

    def __init__(self, *args, **kwargs):
        key_choices = kwargs.pop('key_choices', [])
        super(DeleteAudienceForm, self).__init__(*args, **kwargs)
        self.fields['key_selected'].choices = key_choices 


class DeleteRoleForm(forms.Form):
    role = forms.CharField(label='Имя роли', widget=forms.TextInput(attrs={'placeholder': 'Имя'}), required=False)
    role_selected = forms.ChoiceField(
        label='Выберите роль...',
        choices=[],
        widget=forms.Select(attrs={'required': True})
    )
    def __init__(self, *args, **kwargs):
        role_choices = kwargs.pop('role_choices', [])
        super(DeleteRoleForm, self).__init__(*args, **kwargs)
        self.fields['role_selected'].choices = role_choices 


class ChangeEmployeeIDCardForm(forms.Form):
    full_name = forms.CharField(label='Поиск по ФИО', widget=forms.TextInput(attrs={'placeholder': 'Поиск по ФИО'}), required=False)
    emp_selected = forms.ChoiceField(
        label='Выберите сотрудника...',
        choices=[],
        widget=forms.Select(attrs={'required': True})
    )
    id_card = forms.CharField(label='Изменить ID карты на:', widget=forms.TextInput(attrs={'placeholder': 'Изменить ID карты на:'}), required=True)
    def __init__(self, *args, **kwargs):
        emp_choices = kwargs.pop('emp_choices', [])
        super(ChangeEmployeeIDCardForm, self).__init__(*args, **kwargs)
        self.fields['emp_selected'].choices = emp_choices

class ChangeEmployeeFullNameForm(forms.Form):
    full_name_search = forms.CharField(label='Поиск по ФИО', widget=forms.TextInput(attrs={'placeholder': 'Поиск по ФИО'}), required=False)
    emp_selected = forms.ChoiceField(
        label='Выберите сотрудника...',
        choices=[],
        widget=forms.Select(attrs={'required': True})
    )
    full_name = forms.CharField(label='Изменить ФИО на:', widget=forms.TextInput(attrs={'placeholder': 'Изменить ФИО на:'}), required=True)
    def __init__(self, *args, **kwargs):
        emp_choices = kwargs.pop('emp_choices', [])
        super(ChangeEmployeeFullNameForm, self).__init__(*args, **kwargs)
        self.fields['emp_selected'].choices = emp_choices

class DeleteEmployeeForm(forms.Form):
    full_name = forms.CharField(label='Поиск по ФИО', widget=forms.TextInput(attrs={'placeholder': 'Поиск по ФИО'}), required=False)
    emp_selected = forms.ChoiceField(
        label='Выберите сотрудника...',
        choices=[],
        widget=forms.Select(attrs={'required': True})
    )
    def __init__(self, *args, **kwargs):
        emp_choices = kwargs.pop('emp_choices', [])
        super(DeleteEmployeeForm, self).__init__(*args, **kwargs)
        self.fields['emp_selected'].choices = emp_choices

class SearchForm(forms.Form):
    search = forms.CharField(label='Поиск', widget=forms.TextInput(attrs={'placeholder': 'Поиск', 'class': 'search'}), required=False)

class SearchAdminForm(forms.Form):
    search_full_name = forms.CharField(label='ФИО', widget=forms.TextInput(attrs={'placeholder': 'ФИО', 'class': 'search_one'}), required=False)
    search_auditorium = forms.CharField(label='Кабинет', widget=forms.TextInput(attrs={'placeholder': 'Аудитория', 'class': 'search'}),required=False)
