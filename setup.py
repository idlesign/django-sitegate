import io
import os
import re
import sys
from setuptools import setup, find_packages

PATH_BASE = os.path.dirname(__file__)


def read_file(fpath):
    """Reads a file within package directories."""
    with io.open(os.path.join(PATH_BASE, fpath)) as f:
        return f.read()


def get_version():
    """Returns version number, without module import (which can lead to ImportError
    if some dependencies are unavailable before install."""
    contents = read_file(os.path.join('sitegate', '__init__.py'))
    version = re.search('VERSION = \(([^)]+)\)', contents)
    version = version.group(1).replace(', ', '.').strip()
    return version


setup(
    name='django-sitegate',
    version=get_version(),
    url='http://github.com/idlesign/django-sitegate',

    description='Reusable application for Django to ease sign up & sign in processes',
    long_description=read_file('README.rst'),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(),
    install_requires=[
        'django-etc>=1.2.0',
        'django-siteprefs>=1.1.0',
        'requests',
    ],
    setup_requires=[] + (['pytest-runner'] if 'test' in sys.argv else []),

    include_package_data=True,
    zip_safe=False,

    test_suite='tests',
    tests_require=[
        'pytest',
        'pytest-djangoapp>=1.0.0',
        'pytest-responsemock',
    ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
