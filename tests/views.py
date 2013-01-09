from django.views.generic.simple import direct_to_template


def always_allow(request):
    return direct_to_template(request, template='default.html')


def rejection(request):
    return direct_to_template(request, template='default.html')
