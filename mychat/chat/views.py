from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required

def register(request):
    """
    Представление для регистрации пользователей.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('chat_rooms') 
        else:
            messages.error(request, "Ошибка регистрации. Пожалуйста, проверьте введенные данные.")
    else:
        form = RegistrationForm()
    return render(request, 'chat/register.html', {'form': form})


def user_login(request):
    """
    Представление для входа пользователей.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Вход выполнен успешно!")
            return redirect('chat_rooms')
        else:
            messages.error(request, "Ошибка входа. Пожалуйста, проверьте имя пользователя и пароль.")
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})


@login_required
def user_logout(request):
    """
    Представление для выхода пользователей.
    """
    logout(request)
    messages.success(request, "Вы вышли из системы.")
    return redirect('login') 


@login_required
def chat_rooms(request):
    """
    Представление для отображения списка комнат чата.
    """
    chat_rooms = request.user.chatrooms.all()
    return render(request, 'chat/chat-rooms.html', {'chat_rooms': chat_rooms})