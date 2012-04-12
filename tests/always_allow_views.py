from django.views.generic.simple import direct_to_template


def allowed(request):
    return direct_to_template(request, template='default.html')