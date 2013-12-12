#! /usr/bin/env python
import sys
import os

from django.conf import settings


APP_NAME = 'sitegate'


def main():
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', APP_NAME),
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
            PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
        )

    from django.test.utils import get_runner
    runner = get_runner(settings)()
    failures = runner.run_tests((APP_NAME,))

    sys.exit(failures)


if __name__ == '__main__':
    main()