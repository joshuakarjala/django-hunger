from django.shortcuts import render


def home(request):
    return render(request, 'base.html')


def nonbeta(request):
    return render(request, 'nonbeta.html')


def profile(request):
    return render(request, 'profile.html')
