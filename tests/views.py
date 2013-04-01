from django.shortcuts import render


def always_allow(request):
    return render(request, 'default.html')


def rejection(request):
    return render(request, 'default.html')


def invited_only(request):
    return render(request, 'default.html')
