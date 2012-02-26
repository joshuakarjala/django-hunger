from django.conf import settings
from django.http import HttpResponseRedirect
from hunger.signals import invite_used
from hunger.receivers import invitation_code_used

#setup signals
invite_used.connect(invitation_code_used)

class BetaMiddleware(object):
    """
    Add this to your ``MIDDLEWARE_CLASSES`` make all views except for
    those in the account application require that a user be logged in.
    This can be a quick and easy way to restrict views on your site,
    particularly if you remove the ability to create accounts.

    **Settings:**

    ``BETA_ENABLE_BETA``
        Whether or not the beta middleware should be used. If set to `False`
        the PrivateBetaMiddleware middleware will be ignored and the request
        will be returned. This is useful if you want to disable privatebeta
        on a development machine. Default is `True`.

    ``BETA_NEVER_ALLOW_VIEWS``
        A list of full view names that should *never* be displayed.  This
        list is checked before the others so that this middleware exhibits
        deny then allow behavior.

    ``BETA_ALWAYS_ALLOW_VIEWS``
        A list of full view names that should always pass through.

    ``BETA_ALWAYS_ALLOW_MODULES``
        A list of modules that should always pass through.  All
        views in ``django.contrib.auth.views``, ``django.views.static``
        and ``privatebeta.views`` will pass through unless they are
        explicitly prohibited in ``PRIVATEBETA_NEVER_ALLOW_VIEWS``

    ``BETA_REDIRECT_URL``
        The URL to redirect to.  Can be relative or absolute.
    """

    def __init__(self):
        self.enable_beta = getattr(settings, 'BETA_ENABLE_BETA', True)
        self.never_allow_views = getattr(settings, 'BETA_NEVER_ALLOW_VIEWS', [])
        self.always_allow_views = getattr(settings, 'BETA_ALWAYS_ALLOW_VIEWS', [])
        self.always_allow_modules = getattr(settings, 'BETA_ALWAYS_ALLOW_MODULES', [])
        self.redirect_url = getattr(settings, 'BETA_REDIRECT_URL', '/beta/')
        self.signup_views = getattr(settings, 'BETA_SIGNUP_VIEWS', [])
        self.signup_confirmation_view = getattr(settings, 'BETA_SIGNUP_CONFIRMATION_VIEW', '')
        self.signup_url = getattr(settings, 'BETA_SIGNUP_URL', '/register/')
        self.allow_flatpages = getattr(settings, 'BETA_ALLOW_FLATPAGES', [])

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in self.allow_flatpages or '%s/' % request.path in self.allow_flatpages:
            from django.contrib.flatpages.views import flatpage
            return flatpage(request, request.path_info)

        if not self.enable_beta:
            #Do nothing is beta is not activated
            return

        in_beta = request.session.get('in_beta', False)
        whitelisted_modules = ['django.contrib.auth.views',
                               'django.contrib.admin.sites',
                               'django.views.static',
                               'django.contrib.staticfiles.views',
                               'hunger.views']

        full_view_name = '%s.%s' % (view_func.__module__, view_func.__name__)

        #Check modules
        if self.always_allow_modules:
            whitelisted_modules += self.always_allow_modules

        #if view in module then ignore - except if view is signup confirmation
        if '%s' % view_func.__module__ in whitelisted_modules and not full_view_name == self.signup_confirmation_view:
            return

        #Check views
        if full_view_name in self.never_allow_views:
            return HttpResponseRedirect(self.redirect_url)

        if full_view_name in self.always_allow_views:
            return

        if full_view_name == self.signup_confirmation_view:
            #signup completed - deactivate invitation code
            invitation_code = request.session.get('invitation_code', None)
            request.session['beta_complete'] = True
            invite_used.send(sender=self.__class__, user=request.user, invitation_code=invitation_code)
            return

        if request.user.is_authenticated() and full_view_name not in self.signup_views:
            # User is logged in, or beta is not active, no need to check anything else.
            return

        if full_view_name in self.signup_views and in_beta:
            #if beta code is valid and trying to register then let them through
            return
        else:
            next_page = request.META.get('REQUEST_URI')
            if in_beta:
                return HttpResponseRedirect(self.signup_url + '?next=%s' % next_page)
            else:
                return HttpResponseRedirect(self.redirect_url + '?next=%s' % next_page)

    def process_response(self, request, response):
        try:
            if request.session.get('beta_complete', False):
                del response.session['in_beta']
                del response.session['invitation_code']
                request.session['beta_complete'] = None
        except AttributeError:
            pass
        return response
