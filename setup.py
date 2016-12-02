#!/usr/bin/env python

from setuptools import setup

setup(name = 'qdotsync',
      version = '1.0',
      description = 'download data from qdot-server using rsync',
      author = 'Nik Hartman',
      author_email = 'nik.hartman@gmail.com',
      url = 'https://github.com/nikhartman/qdotsync',
      py_modules = ['qdotsync'],
      install_requires = ['paramiko']
      )
