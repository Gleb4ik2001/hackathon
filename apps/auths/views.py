from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib import messages
from django.views import View

from .forms import LoginForm

from django.contrib.auth import logout
from django.shortcuts import redirect


class LoginView(View):
    def get(self, request):
        # Если пользователь уже авторизован, перенаправим его на главную страницу
        if request.user.is_authenticated:
            return redirect('main_view')  # Переход на главную страницу
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('main_view')  # Перенаправление на главную страницу после логина
            else:
                messages.error(request, 'Неверные данные для входа.')
        return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  