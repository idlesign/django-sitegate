#!/usr/bin/env python
from django.conf import settings
from django.core.management import call_command


if not settings.configured:
    settings.configure(
        INSTALLED_APPS=('django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'sitegate'),
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
        PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)
    )


if __name__ == '__main__':
    call_command('test', 'sitegate')
