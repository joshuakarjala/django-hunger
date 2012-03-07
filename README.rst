Hunger
======

Django app to manage a private beta phase for a website.

- This app provides users with the change to sign up for a private beta - by providing their email address.
- The administrators of the website can manually invite people to join the beta from the Django admin panel.
- The signup view of the app is only accessible by providing the correct invitation code in the url.


Installation
------------

- Install django-hunger into your site-packages
- Add 'hunger.middleware.BetaMiddleware' to MIDDLEWARE_CLASSES


Settings
--------


``BETA_INVITE_CODE_LENGTH``
    String length of the invitation_code
``BETA_ENABLE_BETA``
    Enable hunger middleware
``BETA_NEVER_ALLOW_VIEWS``
    Never allow access to these views
``BETA_ALWAYS_ALLOW_VIEWS``
    Always let unregistered user see these view
``BETA_ALWAYS_ALLOW_MODULES``
    Convenience settings - allow all views and a given module
``BETA_ALLOW_FLATPAGES``
    If using flatpages app
``BETA_SIGNUP_VIEWS``
    Which views are used for signing up
``BETA_SIGNUP_CONFIRMATION_VIEW``
    The view which comes directly after a user hass signed up
``BETA_REDIRECT_URL``
    If user is not logged in and trying to access a hidden view - where should he/she be redirected
``BETA_SIGNUP_URL``
    What is the url for the signup page
``BETA_EMAIL_TEMPLATES_DIR``
    Directory containing email templates
``BETA_EMAIL_MODULE``
    Module where the email functions are
``BETA_EMAIL_CONFIRM_FUNCTION``
    Function for sending out confirmation that user is on waiting list
``BETA_EMAIL_INVITE_FUNCTION``
    Function for sending out the invitation code

Integrating with django_social_auth
-----------------------------------

Modify ``SOCIAL_AUTH_PIPELINE`` in settings to replace
``social_auth.backends.pipeline.user.create_user`` with
``create_beta_user`` (using default pipeline)::

    SOCIAL_AUTH_PIPELINE = (
        'social_auth.backends.pipeline.social.social_auth_user',
        'social_auth.backends.pipeline.associate.associate_by_email',
        'social_auth.backends.pipeline.user.get_username',
        'hunger.contrib.social_auth.create_beta_user',
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
