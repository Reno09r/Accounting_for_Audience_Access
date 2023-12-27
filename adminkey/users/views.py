
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from django.urls import reverse_lazy
from .forms import LoginUserForm

# Класс LoginUser наследуется от LoginView и представляет кастомизированное представление для авторизации пользователей.

# Использует форму LoginUserForm для входа.
# Устанавливает шаблон 'users/login.html' и добавляет дополнительный контекст с заголовком "Авторизация".

# Метод get_success_url возвращает URL, на который будет перенаправлен пользователь после успешной авторизации.
# В данном случае, используется reverse_lazy для указания имени URL-маршрута 'home'.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        return reverse_lazy('home')
