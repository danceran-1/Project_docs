from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, World!")

def registration(request):
    return render(request, 'main/registration.html')
