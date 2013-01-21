.. _ref-userflow:

=========
User Flow
=========


Cases
-----

#. User is unregistered

   * Can only visit views listed in ``HUNGER_ALWAYS_ALLOW_VIEWS`` or
     views in modules listed in ``HUNGER_ALWAYS_ALLOW_MODULES``. The
     views list may refer to the view by the view's function name or
     urlpattern name.

   * All other urls redirect to ``HUNGER_REDIRECT``.
   * If registration view is listed above, then the user can register
     for an account that doesn't yet have beta access.
   * If invited by a friend by receiving an email with a beta invite
     link, then the code is stored in a cookie. When the user
     registers, then they are automatically placed into the beta.
   * If registering via a public beta code, the code is similarly
     placed in a cookie, where later registration will place the user
     automatically in the beta and the invitation code count
     decrements by 1.

#. User is registered but not in beta

   * An admin can invite that specific user to the beta through the
     Django admin interface.
   * The user can be invited by another beta who has beta access,
     provided that the inviter has enough invitations to send the
     invitation. The user clicks a link.
   * The user can join the beta themselves by using a public beta code
     as long as the code has enough uses left.
   * Upon being verified as in-beta, the user is redirected to
     ``HUNGER_VERIFIED_REDIRECT``.

#. User is registered and in beta

   * An admin can dispense invitations so that users can invite their
     friends.
   * Invitations in hand, the user invites friends via either email or
     their username if applicable.
   * Otherwise, allow user to invite friends at-will.
