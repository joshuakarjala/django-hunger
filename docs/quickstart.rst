.. _ref-quickstart:

==========
Quickstart
==========

Installation and Basic Configuration
------------------------------------

- Install ``django-hunger`` using ``pip`` or ``easy_install``.
- Add ``hunger`` to ``INSTALLED_APPS`` in settings.py.
- Add ``hunger.middleware.BetaMiddleware`` to ``MIDDLEWARE_CLASSES``.
- Add ``url(r'hunger', include('hunger.urls'))`` to your urlconf.
- List views that all users may see at any time regardless of beta
  status in the setting ``HUNGER_ALWAYS_ALLOW_VIEWS`` and
  ``HUNGER_ALWAYS_ALLOW_MODULES``. The views setting accepts views by
  function name or urlpattern name, while the modules accepts a string
  module name where all included views are always allowed. Typically,
  you at least want to let people register, login, and recover
  password, so include the auth urls::

     HUNGER_ALWAYS_ALLOW_MODULES = [
         'django.contrib.auth.views'
     ]

- Create template ``hunger/not_in_beta.html``, which is the page a
  user is redirected to when trying to access protected content when
  not in the beta.
- Create template ``hunger/verified.html``, which is the page
  after the user successfully has joined and verified their in-beta
  status.
- Create template ``hunger/invalid.html``, which is the page a user
  sees when they try to use a code but it is invalid. It could be a
  code that doesn't exist or one that has run out of invites.
- Create the email template ``hunger/invite_email.[html/txt]`` and
  email subject template ``hunger/invite_email_subject.txt``. These
  templates are rendered like Django templates with a simple context
  described in ``hunger/email.py``. To ensure the best user
  experience, you should provide both the html and txt email
  templates. Example versions of these templates are in
  ``example/example/templates/hunger/``.


Advanced Configuration
----------------------

The basic configuration basically involves creating a bunch of static
templates for various pre-configured views. For a more advanced
configuration, you can let hunger use your own urls, views, and
templates using custom redirect settings. All redirect targets must be
valid targets for the built-in ``django.shortcuts.redirect`` function.

- ``HUNGER_REDIRECT`` for users accessing protected content while not
  in the beta.
- ``HUNGER_VERIFIED_REDIRECT`` for the page a user sees after
  successfully joining and verifying in-beta status.
- ``HUNGER_EMAIL_TEMPLATES_DIR`` for a different directory holding the
  invite email templates.
- ``HUNGER_EMAIL_INVITE_FUNCTION`` for a different function to call
  when sending email invites. Takes precedence over
  ``HUNGER_EMAIL_TEMPLATES_DIR``.


Integration with django_templated_email
---------------------------------------

If `django_templated_email <https://github.com/bradwhittington/django-templated-email>`_
is installed, you can use a customized ``*.email`` template for beta invites.

And create the following template::

   <project_dir>/templates/hunger/invite_email.email
