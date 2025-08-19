from django.shortcuts import redirect
from django.urls import reverse , resolve
from django.contrib.auth import logout

from django.utils.cache import add_never_cache_headers

PROTECTED_URL_NAMES = {'success', 'success1'}

class AuthRequiredMiddleware:
    """
    Пускаем на приватные вьюхи только
    при валидной Django-сессии + совпадении ID.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            match = resolve(request.path_info)
            url_name = match.url_name
        except Exception:
            url_name = None

        is_protected = url_name in PROTECTED_URL_NAMES

        if is_protected:
            if not request.user.is_authenticated:
                return redirect(reverse('registr'))

            sess_uid = request.session.get('custom_user_id')
            if not sess_uid or sess_uid != request.user.id:
                print("Сработал")
                logout(request)
                request.session.flush()
                return redirect(reverse('registr'))

        response = self.get_response(request)

        if is_protected:
            # ломаем любые варианты кэша, включая bfcache
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            add_never_cache_headers(response)

        return response


    
class NoCacheMiddleware:
    """
    Полностью запрещает кеширование приватных страниц (включая back/forward cache).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        protected_paths = ['/success/', '/success1/']
        if request.path in protected_paths:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response

