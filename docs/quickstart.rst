.. _ref-quickstart:

==========
Quickstart
==========


Installation
------------

- Install ``django-hunger`` using ``pip`` or ``easy_install``.
- Add ``hunger`` to ``INSTALLED_APPS`` in settings.py.
- Add ``hunger.middleware.BetaMiddleware`` to ``MIDDLEWARE_CLASSES``.
- Create templates ``hunger/request_invite.html``,
  ``hunger/confirmation.html``, and ``hunger/used.html``. The
  ``request_invite.html`` template receives a Context instance with a
  Django form for the email signup form. The ``confirmation.html`` and
  ``used.html`` templates are flatpages for confirming signup and used
  invites.
- By default Hunger redirects to ``/beta/`` if a users is not logged in. So your "request_invite" templates should be located here.
