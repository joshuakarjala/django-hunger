from django.views.generic.simple import direct_to_template


def never_allow(request):
    return direct_to_template(request, template='default.html')

def always_allow(request):
    return direct_to_template(request, template='default.html')

def signup(request):
    return direct_to_template(request, template='default.html')

def signup_confirmation(request):
    return direct_to_template(request, template='default.html')
