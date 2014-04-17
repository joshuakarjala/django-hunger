#!/usr/bin/env python
from __future__ import unicode_literals
import sys
from os.path import dirname, abspath, join
from optparse import OptionParser

parent = dirname(abspath(__file__))
sys.path.insert(0, parent)

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='sqlite3',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'TEST_NAME': 'hunger_tests.db',
            },
        },
        DATABASE_NAME='test_hunger',
        TEST_DATABASE_NAME='hunger_tests.db',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.admin',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.contenttypes',
            # 'south',
            'hunger',
            'tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,
        TEMPLATE_DEBUG=True,
        TEMPLATE_DIRS=[join(parent, 'tests', 'templates')],

        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'hunger.middleware.BetaMiddleware'
        ),
        HUNGER_REDIRECT='rejection',
        HUNGER_ALWAYS_ALLOW_VIEWS=[
            'tests.views.always_allow',
            'tests.views.rejection',
        ],
        HUNGER_ALWAYS_ALLOW_MODULES=['tests.always_allow_views'],
    )

from django.test.simple import DjangoTestSuiteRunner

def runtests(*test_args, **kwargs):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['tests']

    test_runner = DjangoTestSuiteRunner(verbosity=kwargs.get('verbosity', 1),
                                        interactive=kwargs.get('interactive', False),
    failfast=kwargs.get('failfast'))
    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true', default=False, dest='failfast')

    (options, args) = parser.parse_args()

    runtests(failfast=options.failfast, *args)
