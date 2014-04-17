from __future__ import unicode_literals
from django.shortcuts import render


def allowed(request):
    return render(request, 'default.html')
