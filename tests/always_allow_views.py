from django.shortcuts import render


def allowed(request):
    return render(request, 'default.html')
