from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import User
from .forms import CriterionForm
from django.conf import settings
from django.db import connection
import os


def index(request):
    return render(request, 'main/index.html')


def special_users(request,password,user_id):
    
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT loggin FROM loging_password WHERE password = %s AND id = %s",
            [password, user_id]
            )
        
        auth_data = cursor.fetchone()

        if not auth_data:
            error_message = 'Неверный пароль для спецпользователя'
            return render(request, 'main/about.html',
                    {'form': RegistrationForm(), 'error_message': error_message})

        name = auth_data[0]
        request.session['is_special'] = True
        return redirect('success')


def about(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:
            # сначала ищем спец пользователей
            cursor.execute(
                "SELECT id FROM loging_password WHERE loggin = %s",
                [username]
            )
            special = cursor.fetchone()

            if special:
                return special_users(request, password, special[0])

            # тут обычных
            cursor.execute(
                "SELECT id FROM users WHERE name = %s",
                [username]
            )
            user_data = cursor.fetchone()

            if not user_data:
                error_message = 'Пользователь не найден'
                return render(request, 'main/about.html', 
                           {'form': RegistrationForm(), 'error_message': error_message})

            user_id = user_data[0]

            cursor.execute(
                "SELECT name FROM users WHERE user_password = %s AND id = %s",
                [password, user_id]
            )
            auth_data = cursor.fetchone()

            if not auth_data:
                error_message = 'Неверный пароль'
                return render(request, 'main/about.html',
                           {'form': RegistrationForm(), 'error_message': error_message})

            name = auth_data[0]
            request.session['user_id'] = user_id
            success_message = f"Авторизация для {name} выполнена успешно"
            return redirect('success')

    else:
        return render(request, 'main/about.html', {'form': RegistrationForm()})


def success(request):
    if request.method == 'POST':
        if 'A' in request.POST and 'B' in request.POST:
            A = request.POST.get('A')
            B = request.POST.get('B')

            if A is not None and B is not None:
                try:
                    A = int(A)
                    B = int(B)

                    K1 = (A / B) * 100
                    result = f"К1 = {K1:.2f}%"
                    mark = 0
                    if 55 < K1 <= 59:
                        mark = 1
                    elif 60 < K1 <= 64:
                        mark = 3
                    elif 65 < K1 <= 70:
                        mark = 5

                except (ValueError, ZeroDivisionError):
                    result = "Ошибка ввода данных. Пожалуйста, введите числовые значения для A и B."
                    mark = 0
            else:
                result = "Пожалуйста, введите значения для A и B."
                mark = 0

            return render(request, 'main/success.html', {'result': result, 'mark': mark})

        elif 'A1' in request.POST and 'B1' in request.POST:
            A1 = request.POST.get('A1')
            B1 = request.POST.get('B1')

            if A1 is not None and B1 is not None:
                try:
                    A1 = int(A1)
                    B1 = int(B1)

                    K2 = (A1 / B1) * 100
                    result2 = f"К2 = {K2:.2f}%"
                    mark1 = 0
                    if 45 < K2 <= 49:
                        mark1 = 1
                    elif 50 < K2 <= 54:
                        mark1 = 3
                    elif 55 < K2 <= 60:
                        mark1 = 5

                except (ValueError, ZeroDivisionError):
                    result2 = "Ошибка ввода данных. Пожалуйста, введите числовые значения для A1 и B1."
                    mark1 = 0
            else:
                result2 = "Пожалуйста, введите значения для A1 и B1."
                mark1 = 0

            return render(request, 'main/success.html', {'result2': result2, 'mark1': mark1})

    return render(request, 'main/success.html')


def success1(request):
    if request.method == 'POST':
        if 'A' in request.POST and 'B' in request.POST:
            A = request.POST.get('A')
            B = request.POST.get('B')

            if A is not None and B is not None:
                try:
                    A = int(A)
                    B = int(B)

                    K1 = (A / B) * 100
                    result = f"К1 = {K1:.2f}%"
                    mark = 0
                    if 55 < K1 <= 59:
                        mark = 1
                    elif 60 < K1 <= 64:
                        mark = 3
                    elif 65 < K1 <= 70:
                        mark = 5

                except (ValueError, ZeroDivisionError):
                    result = "Ошибка ввода данных. Пожалуйста, введите числовые значения для A и B."
                    mark = 0
            else:
                result = "Пожалуйста, введите значения для A и B."
                mark = 0

            return render(request, 'main/success.html', {'result': result, 'mark': mark})

        elif 'A1' in request.POST and 'B1' in request.POST:
            A1 = request.POST.get('A1')
            B1 = request.POST.get('B1')

            if A1 is not None and B1 is not None:
                try:
                    A1 = int(A1)
                    B1 = int(B1)

                    K2 = (A1 / B1) * 100
                    result2 = f"К2 = {K2:.2f}%"
                    mark1 = 0
                    if 45 < K2 <= 49:
                        mark1 = 1
                    elif 50 < K2 <= 54:
                        mark1 = 3
                    elif 55 < K2 <= 60:
                        mark1 = 5

                except (ValueError, ZeroDivisionError):
                    result2 = "Ошибка ввода данных. Пожалуйста, введите числовые значения для A1 и B1."
                    mark1 = 0
            else:
                result2 = "Пожалуйста, введите значения для A1 и B1."
                mark1 = 0

            return render(request, 'main/success.html', {'result2': result2, 'mark1': mark1})

    return render(request, 'main/success.html')

def criterion_view(request):
    if request.method == 'POST':
        form = CriterionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = CriterionForm()
    return render(request, 'main/criterion.html', {'form': form})

def media(request):
    media_root = settings.MEDIA_ROOT
    files = os.listdir(media_root)
    return render(request, 'main/media.html', {'files': files})