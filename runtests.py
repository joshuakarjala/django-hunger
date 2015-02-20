#!/usr/bin/env python
from __future__ import unicode_literals
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


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
            'hunger',
            'tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
        SITE_ID=1,

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


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()
