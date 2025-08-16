# Ссылки на странички. Каждую новую страницу добавлять сюда
from django.contrib import admin
from django.urls import path, include
from  . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index),
    path('about/', views.about, name='about'),
    path('registr/', views.registr, name='registr'),
    path('success/', views.success, name='success'),
    path('captcha/', include('captcha.urls')),
    path('success1/<str:username>/<int:user_id>/', views.success1, name='success1'),
    path('media/', views.media, name='media_view'),
    # path('check-doc-data/<int:user_id>/', views.check_doc_data, name='check_doc_data'),
    path('generate-doc/<int:user_id>/', views.generate_doc, name='generate_doc'),
    path('city-autocomplete/', views.city_autocomplete, name='city_autocomplete')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)