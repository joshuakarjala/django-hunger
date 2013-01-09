Hunger
======

.. image:: https://secure.travis-ci.org/joshuakarjala/django-hunger.png?branch=master
   :target: http://travis-ci.org/joshuakarjala/django-hunger

Django app to manage a private beta phase for a website.

- This app provides users with the change to sign up for a private beta - by providing their email address.
- The administrators of the website can manually invite people to join the beta from the Django admin panel.
- The signup view of the app is only accessible by providing the correct invitation code in the url.


Installation
------------

- Install ``django-hunger`` using ``pip`` or ``easy_install``.
- Add ``hunger`` to ``INSTALLED_APPS`` in settings.py.
- Add ``hunger.middleware.BetaMiddleware`` to ``MIDDLEWARE_CLASSES``.
- Create templates ``beta/request_invite.html``,
  ``beta/confirmation.html``, and ``beta/used.html``. The
  ``request_invite.html`` template receives a Context instance with a
  Django form for the email signup form. The ``confirmation.html`` and
  ``used.html`` templates are flatpages for confirming signup and used
  invites.
- By default Hunger redirects to "/beta/" if a users is not logged in. So your "request_invite" templates should be located here.

Settings
--------

``BETA_INVITE_CODE_LENGTH``
    String length of the invitation_code (Default: ``8``)
``BETA_ENABLE_BETA``
    Enable hunger middleware (Default: ``True``)
``BETA_ALWAYS_ALLOW_VIEWS``
    Always let unregistered user see these view (Default: ``[]``)
``BETA_ALWAYS_ALLOW_MODULES``
    Convenience settings - allow all views and a given module (Default: ``[]``)
``BETA_ALLOW_FLATPAGES``
    If using flatpages app (Default: ``[]``)
``BETA_REDIRECT_URL``
    If user is not logged in and trying to access a hidden view - where should
    he/she be redirected (Default: ``/beta/``)
``BETA_SIGNUP_URL``
    What is the url for the signup page (Default: ``/register/``)
``BETA_EMAIL_TEMPLATES_DIR``
    Directory containing email templates (Default: ``hunger``)
``BETA_EMAIL_MODULE``
    Module where the email functions are (Default: ``hunger.email``)
``BETA_EMAIL_CONFIRM_FUNCTION``
    Function for sending out confirmation that user is on waiting list
    (Default: ``beta_confirm``)
``BETA_EMAIL_INVITE_FUNCTION``
    Function for sending out the invitation code (Default: ``beta_invite``)

Integration with django_templated_email
---------------------------------------

If django_templated_email - https://github.com/bradwhittington/django-templated-email
is installed, you can use customized ``*.email`` templates with an
example setting such as::

   BETA_EMAIL_TEMPLATES_DIR = 'beta'

And create the following templates::

   <project_dir>/templates/beta/beta_confirm.email
   <project_dir>/templates/beta/beta_invite.email


Integration with django_social_auth
-----------------------------------

Modify ``SOCIAL_AUTH_PIPELINE`` in settings to replace
``social_auth.backends.pipeline.user.create_user`` with
``create_beta_user`` (using default pipeline)::

    SOCIAL_AUTH_PIPELINE = (
        'social_auth.backends.pipeline.social.social_auth_user',
        'social_auth.backends.pipeline.associate.associate_by_email',
        'social_auth.backends.pipeline.user.get_username',
        'hunger.contrib.social_auth_pipeline.create_beta_user',
        'social_auth.backends.pipeline.social.associate_user',
        'social_auth.backends.pipeline.social.load_extra_data',
        'social_auth.backends.pipeline.user.update_user_details'
    )

``BETA_ALWAYS_ALLOW_VIEWS`` must at bare minimum include the relevant
social_auth views::

    BETA_ALWAYS_ALLOW_VIEWS = (
        'social_auth.views.auth',
        'social_auth.views.complete',
    )

Credit
------
Hunger is partially based on:
- https://github.com/pragmaticbadger/django-privatebeta
