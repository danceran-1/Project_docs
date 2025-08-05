from django.shortcuts import render, redirect

from django.core.exceptions import ValidationError
from .forms import RegistrationForm, LoginForm
from .models import User
from .forms import CriterionForm
from django.conf import settings
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
from .models import UserAvatar
import os
import bcrypt 
from django_ratelimit.decorators import ratelimit
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password


def index(request):
    return render(request, 'main/index.html')


def password_check(request,password,loggin,spesial_password,id,is_admin):

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

                    view_name = parsing(loggin)

                    if is_admin:
                        return redirect('success1', username = view_name,user_id = id)
                    
                    else:
                        return redirect('success', username = view_name,user_id = id)


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

    validator = RegexValidator(
    r'^[a-zA-Zа-яА-ЯёЁ0-9_@.+\-]+$',
    'Invalid username!'
)
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
                "SELECT loggin,password,id FROM loging_password WHERE loggin = %s",
                [username]
            )
            special = cursor.fetchone()

            if special:
                return password_check(request, password,special[0],special[1],special[2],True)

            # тут обычных
            cursor.execute(
                "SELECT user_password,name,id FROM users WHERE name = %s",
                [username]
            )
            user_data = cursor.fetchone()

            if user_data:
                return password_check(request, password,user_data[1],user_data[0],user_data[2],False)
            
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

        if password != confirm_password:
            error_message = 'Пароли не совпадают'
            return render(request, 'main/registr.html', 
                        {'error_message': error_message})
        
        error_message = validation(username)
        if error_message:
            return render(request, 'main/registr.html', {
                'form': RegistrationForm(),
                'error_message': error_message
            })

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
                    "INSERT INTO users (name, user_password) VALUES (%s, %s)",
                    [username, hashed_password_str]
                )
                

            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM users WHERE name = %s",
                    [username]
                )
                user_id = cursor.fetchone()

            view_name = parsing(username)
            print(parsing(username))
            return redirect('success', username=view_name,user_id = user_id[0])
        
        except Exception as e:
            error_message = f"Ошибка при регистрации: {str(e)}"
    
    return render(request, 'main/registr.html', {'error_message': error_message})


def parsing(username):

    if "@" in username:
        dog_sep = username.split("@")[0]
        dot_sep = username.split(".")[0]

        return dog_sep if len(dog_sep) < len(dot_sep) else dot_sep
    
    else:
         return username
 
def success(request, username,user_id):
    
    form_data = {
            'first_name': '',
            'last_name': '',
            'middle_name': '',
            'birth_date': '',
            'city': ''
        }

    if request.method == 'POST':
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        city = request.POST.get('city', '').strip()

        avatar_file = request.FILES.get('avatar')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM personal_data WHERE user_id = %s",
                [user_id]
            )
            is_data = cursor.fetchone()

        if is_data:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE personal_data SET name = %s, surname = %s, last_name = %s, dob = %s, sity = %s 
                    WHERE user_id = %s""", [first_name, last_name, middle_name, birth_date, city, user_id])

            
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO personal_data (user_id, name,surname,last_name,dob,sity) VALUES (%s, %s,%s,%s,%s,%s)",
                    [user_id,last_name,first_name,middle_name,birth_date,city]
                    )
                
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'middle_name': middle_name,
            'birth_date': birth_date,
            'city': city
        }
        if avatar_file:
            avatar_obj, created = UserAvatar.objects.get_or_create(user_id=user_id)
            avatar_obj.avatar = avatar_file
            avatar_obj.save()   

        avatar_url = ''
        avatar = UserAvatar.objects.filter(user_id=user_id).first()
        if avatar and avatar.avatar:
            avatar_url = avatar.avatar.url

    else:
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM personal_data WHERE user_id = %s", [user_id])
            row = cursor.fetchone()
            if row:
                birth_date = row[4].strftime('%Y-%m-%d') if row[4] else ''

                form_data = {
                    'first_name': row[2],
                    'last_name': row[1],
                    'middle_name': row[3],
                    'birth_date': birth_date,
                    'city': row[5]
                }

        avatar_url = ''
        avatar = UserAvatar.objects.filter(user_id=user_id).first()
        if avatar and avatar.avatar:
            avatar_url = avatar.avatar.url

    return render(request, 'main/success.html', {
        'username': username,
        'user_id': user_id,
        'form_data': form_data,
        'full_name': f"{form_data['last_name']} {form_data['first_name']} {form_data['middle_name']}",
        'birth_date': form_data['birth_date'],
        'city': form_data['city'],
        'avatar_url': avatar_url
    })



def success1(request,username,user_id):
    if request.method == 'POST':
        last_name = request.POST.get('last_name', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        birth_date = request.POST.get('birth_date', '').strip()
        city = request.POST.get('city', '').strip()

        

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO personal_data (user_id, name,surname,last_name,dob,sity) VALUES (%s, %s,%s,%s,%s,%s)",
                [user_id,last_name,first_name,middle_name,birth_date,city]
            )

        
    return render(request, 'main/success.html',{'username':username},{'user_id':user_id})

        

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