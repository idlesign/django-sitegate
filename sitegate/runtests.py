#! /usr/bin/env python
import sys
import os

from django.conf import settings, global_settings


APP_NAME = 'sitegate'


def main():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'etc', APP_NAME
            ),
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
            MIDDLEWARE_CLASSES=(
                'django.middleware.common.CommonMiddleware',
                'django.contrib.sessions.middleware.SessionMiddleware',
                'django.contrib.auth.middleware.AuthenticationMiddleware',
                'django.contrib.messages.middleware.MessageMiddleware',
            ),
            ROOT_URLCONF = 'sitegate.tests',
        )

    try:  # Django 1.7 +
        from django import setup
        setup()
    except ImportError:
        pass

    from django.test.utils import get_runner
    runner = get_runner(settings)()
    failures = runner.run_tests((APP_NAME,))

    sys.exit(failures)


if __name__ == '__main__':
    main()
