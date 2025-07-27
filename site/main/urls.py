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
    path('success1/', views.success, name='success1'),
    path('media/', views.media, name='media_view'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)