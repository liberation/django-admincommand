#!/usr/bin/env python
import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-admincommand',
    version='0.1',
    description='Execute management commands from the admin',
    long_description=read('README.rst'),
    author='Djaz Team',
    author_email='devweb@liberation.fr',
    url='https://github.com/liberation/django-admincommand',
    packages=['admincommand'],
)
