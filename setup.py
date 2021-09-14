#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Lipson on 2021/9/1.
# email to LipsonChan@yahoo.com
#

from setuptools import setup, find_packages

setup(
    name='lipson_tools',
    version='0.1.0',
    author='lipson',
    packages=['compare_table'],
    include_package_data=True,
    install_requires=[
        'pandas>=1.1',
    ],
)
