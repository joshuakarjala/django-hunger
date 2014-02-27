Trying the Example App
======================

Clone the repo and run the included example django project::

   git clone git://github.com/joshuakarjala/django-hunger.git
   cd django-hunger/example
   pip install -r requirements.txt
   python manage.py syncdb
   python manage.py runserver

Alternately, if you want to leave your local environment untouched, you can also instantiate a Vagrant instance and run the Django server using::

   vagrant provision
   vagrant up
   vagrant ssh
   cd /vagrant/example
   source env/bin/activate
   python manage.py syncdb
   python manage.py runserver

Guide
-----

The example app utilizes a basic configuration with
`django-registration
<https://bitbucket.org/ubernostrum/django-registration>`_ for
verifying emails. Therefore the list of views in
``HUNGER_ALWAYS_ALLOW_VIEWS`` utlizes the ``registration_*`` views
instead of ``django.contrib.auth.views`` for registration.

Note that the email backend being used in the example is the console
backend, meaning that all emails are printed to the console.

Once the example project is running, registering an ordinary user will
result in the creation of the account + activation through email.
After registration, the standard user does not have beta access and
will be restricted.

To grant beta access to the created user, simply sign into the admin
site at ``/admin/``, click on ``Invitations``, and invite the
invitation corresponding to the registered user via the admin actions
menu.

Signing in as the original user will result in being able to access
protected beta content.
