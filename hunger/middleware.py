from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.shortcuts import redirect
from django.db.models import Q
from hunger.models import InvitationCode, Invitation
from hunger.utils import setting, now


class BetaMiddleware(object):
    """
    Add this to your ``MIDDLEWARE_CLASSES`` make all views except for
    those in the account application require that a user be logged in.
    This can be a quick and easy way to restrict views on your site,
    particularly if you remove the ability to create accounts.

    **Settings:**

    ``HUNGER_ENABLE_BETA``
        Whether or not the beta middleware should be used. If set to
        `False` the BetaMiddleware middleware will be ignored and the
        request will be returned. This is useful if you want to
        disable privatebeta on a development machine. Default is
        `True`.

    ``HUNGER_ALWAYS_ALLOW_VIEWS``
        A list of full view names that should always pass through.

    ``HUNGER_ALWAYS_ALLOW_MODULES``
        A list of modules that should always pass through.  All
        views in ``django.contrib.auth.views``, ``django.views.static``
        and ``hunger.views`` will pass through.

    ``HUNGER_REDIRECT``
        The redirect when not in beta.
    """

    def __init__(self):
        self.enable_beta = setting('HUNGER_ENABLE')

        self.always_allow_views = setting('HUNGER_ALWAYS_ALLOW_VIEWS')
        self.always_allow_modules = setting('HUNGER_ALWAYS_ALLOW_MODULES')
        self.redirect = setting('HUNGER_REDIRECT')
        self.allow_flatpages = setting('HUNGER_ALLOW_FLATPAGES')

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not self.enable_beta:
            return

        if (request.path in self.allow_flatpages or
            (getattr(settings, 'APPEND_SLASH', True) and
             '%s/' % request.path in self.allow_flatpages)):
            from django.contrib.flatpages.views import flatpage
            return flatpage(request, request.path_info)

        whitelisted_modules = ['django.contrib.auth.views',
                               'django.contrib.admin.sites',
                               'django.views.static',
                               'django.contrib.staticfiles.views']

        # All hunger views, except NotBetaView, are off limits until in beta
        whitelisted_views = ['hunger.views.NotBetaView',
                             'hunger.views.verify_invite',
                             'hunger.views.InvalidView']

        short_name = view_func.__class__.__name__
        if short_name == 'function':
            short_name = view_func.__name__
        view_name = self._get_view_name(request)

        full_view_name = '%s.%s' % (view_func.__module__, short_name)

        if self.always_allow_modules:
            whitelisted_modules += self.always_allow_modules

        if '%s' % view_func.__module__ in whitelisted_modules:
            return

        if self.always_allow_views:
            whitelisted_views += self.always_allow_views

        if (full_view_name in whitelisted_views or
            view_name in whitelisted_views):
            return

        if not request.user.is_authenticated():
            # Ask anonymous user to log in if trying to access in-beta view
            return redirect(setting('LOGIN_URL'))

        if request.user.is_staff:
            return

        # Prevent queries by caching in_beta status in session
        if request.session.get('hunger_in_beta'):
            return

        cookie_code = request.COOKIES.get('hunger_code')
        invitations = Invitation.objects.filter(
            Q(user=request.user) |
            Q(email=request.user.email)
            ).select_related('code')

        # User already in the beta - cache in_beta in session
        if any([i.used for i in invitations if i.invited]):
            request.session['hunger_in_beta'] = True
            return

        # User has been invited - use the invitation and place in beta.
        activates = [i for i in invitations if i.invited and not i.used]

        # Check for matching cookie code if available.
        if cookie_code:
            for invitation in activates:
                if invitation.code.code == cookie_code:
                    # Invitation may be attached to email
                    invitation.user = request.user
                    invitation.used = now()
                    invitation.save()
                    request.session['hunger_in_beta'] = True
                    request._hunger_delete_cookie = True
                    return

        # No cookie - let's just choose the first invitation if it exists
        if activates:
            invitation = activates[0]
            # Invitation may be attached to email
            invitation.user = request.user
            invitation.used = now()
            invitation.save()
            request.session['hunger_in_beta'] = True
            return


        if not cookie_code:
            if not invitations:
                invitation = Invitation(user=request.user)
                invitation.save()
            return redirect(self.redirect)

        # No invitation, all we have is this cookie code
        try:
            code = InvitationCode.objects.get(code=cookie_code,
                num_invites__gt=0)
        except InvitationCode.DoesNotExist:
            request._hunger_delete_cookie = True
            return redirect(reverse('hunger-invalid', args=(cookie_code,)))

        right_now = now()
        if code.private:
            # If we got here, we're trying to fix up a previous private
            # invitation to the correct user/email.
            invitation = Invitation.objects.filter(code=code)[0]
            invitation.user = request.user
            invitation.invited = right_now
            invitation.used = right_now
            code.num_invites = 0
        else:
            invitation = Invitation(user=request.user,
                                    code=code,
                                    invited=right_now,
                                    used=right_now)
            code.num_invites -= 1
        invitation.save()
        code.save()
        return

    def process_response(self, request, response):
        if getattr(request, '_hunger_delete_cookie', False):
            response.delete_cookie('hunger_code')
        return response

    @staticmethod
    def _get_view_name(request):
        """Return the urlpattern name."""
        if hasattr(request, 'resolver_match'):
            # Django >= 1.5
            return request.resolver_match.view_name

        match = resolve(request.path)
        return match.url_name
