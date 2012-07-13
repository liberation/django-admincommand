#!/usr/bin/env python
import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


packages, data_files = [], []
root_dir = os.path.dirname(__file__)
tagging_dir = os.path.join(root_dir, 'tagging')
pieces = fullsplit(root_dir)


if pieces[-1] == '':
    len_root_dir = len(pieces) - 1
else:
    len_root_dir = len(pieces)


for dirpath, dirnames, filenames in os.walk(tagging_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): 
            del dirnames[i]
        if '__init__.py' in filenames:
            packages.append('.'.join(fullsplit(dirpath)[len_root_dir:]))
        elif filenames:
            data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


setup(
    name='django-admincommand',
    version='0.1',
    description='Execute management commands from the admin',
    long_description=read('README.rst'),
    author='Djaz Team',
    author_email='devweb@liberation.fr',
    url='https://github.com/liberation/django-admincommand',
    packages=packages,
    data_files=data_files,
)
