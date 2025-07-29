from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registration', views.registration, name='registration'),
]