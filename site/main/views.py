from django.shortcuts import render, redirect

from django.core.exceptions import ValidationError
from .forms import RegistrationForm, LoginForm
from .models import User
from .forms import CriterionForm
from django.conf import settings
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
import os
import bcrypt 
from django_ratelimit.decorators import ratelimit
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password


def index(request):
    return render(request, 'main/index.html')


def password_check(request,password,loggin,spesial_password):

        lock_key = f'login_lock_{loggin}'
        lock_time = cache.get(lock_key)
        print(f"Lock time from cache: {lock_time}") 

        if lock_time:
            remaining = (lock_time - timezone.now()).seconds
            return render(request, 'main/about.html', {
                'form': RegistrationForm(),
                'error_message': f"Потворите попыптку через {remaining} секунд"
            })

        fail_count = cache.get(f'login_fails_{loggin}', 0)

        try:
            hash_bytes = spesial_password.encode('utf-8')
            
            if bcrypt.checkpw(password.encode('utf-8'), hash_bytes):
                success_message = f"Авторизация для {loggin} выполнена успешно"
                return redirect('success')

            else:
                
                fail_count += 1
                cache.set(f'login_fails_{loggin}', fail_count, timeout=300)

                if fail_count > 4:
                    cache.set(lock_key, timezone.now() + timezone.timedelta(minutes=2), timeout=120)

                error_message = 'Неверный пароль'
                return render(request, 'main/about.html',
                        {'form': RegistrationForm(), 'error_message': error_message})
            
        except Exception as e:
                error_message = 'Ошибка аутентификации'
                return render(request, 'main/about.html',
                           {'form': RegistrationForm(), 'error_message': error_message})


def validation(username):

    validator = RegexValidator(r'^[a-zA-Zа-яА-ЯёЁ0-9_]+$', 'Invalid username!')
    try:
        validator(username)
        return None
    except ValidationError:
        return 'Username contains forbidden characters!'
    
    
# @ratelimit(key='ip', rate='8/m',block=True)
def about(request):
    """Авторизация"""
    if request.method == 'POST':
       
        username = request.POST.get('username')
        password = request.POST.get('password')
        ip = request.META.get('REMOTE_ADDR')    


        ip_fail_key = f'login_fails_ip_{ip}'
        ip_lock_key = f'login_lock_ip_{ip}'

        ip_lock = cache.get(ip_lock_key)

        if ip_lock:
            remaining = (ip_lock - timezone.now()).seconds
            return render(request, 'main/about.html', {
                'form': RegistrationForm(),
                'error_message': f"Потворите попыптку через {remaining} секунд"
            })

        error_message = validation(username)
        if error_message:
            return render(request, 'main/about.html', {
                'form': RegistrationForm(),
                'error_message': error_message
            })

        with connection.cursor() as cursor:
            # сначала ищем спец пользователей
            cursor.execute(
                "SELECT loggin,password FROM loging_password WHERE loggin = %s",
                [username]
            )
            special = cursor.fetchone()

            if special:
                return password_check(request, password,special[0],special[1])

            # тут обычных
            cursor.execute(
                "SELECT user_password,name FROM users WHERE name = %s",
                [username]
            )
            user_data = cursor.fetchone()

            if user_data:
                return password_check(request, password,user_data[1],user_data[0])
            
            else:
                ip_fails = cache.get(ip_fail_key, 0) + 1
                cache.set(ip_fail_key, ip_fails, timeout=300)

                if ip_fails > 5:
                    cache.set(ip_lock_key, 
                            timezone.now() + timezone.timedelta(minutes=2), 
                            timeout=120)
                    
                error_message = 'Пользователь не найден'
                return render(request, 'main/about.html', 
                           {'form': RegistrationForm(), 'error_message': error_message})

    else:
        return render(request, 'main/about.html', {'form': RegistrationForm()})

def registr(request):
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        

        if password != confirm_password:
            error_message = 'Пароли не совпадают'
            return render(request, 'main/registr.html', 
                        {'error_message': error_message})
        
        try:
            validate_password(password,username)
        except ValidationError as ve:
            error_message = 'Ошибка в пароле: ' + ', '.join(ve.messages)
            return render(request,'main/registr.html',
                        {'error_message':error_message})

        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashed_password_str = hashed_password.decode('utf-8')

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name FROM users WHERE name = %s",
                    [username]
                )
                not_uniq = cursor.fetchone()

                print(not_uniq)

                if not_uniq:
                    error_message = 'Логин занят'
                    return render(request, 'main/registr.html', 
                            {'error_message': error_message})

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, user_password) VALUES (%s, %s)",
                    [username, hashed_password_str]
                )
            
            return redirect("success") 
        
        except Exception as e:
            error_message = f"Ошибка при регистрации: {str(e)}"
    
    return render(request, 'main/registr.html', {'error_message': error_message})

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