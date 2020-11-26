from django.shortcuts import render


def base(request):
    return render(request, 'base.html')


def index(request):
    return render(request, 'index.html')
