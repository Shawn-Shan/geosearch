#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='geosearch',
    version='0.0.1',
    description='GeoSearch searchs and extracts country and city mentions from text',
    author = 'Shawn Sixiong Shan',
    author_email='shansixioing@uchicago.edu',
    url='https://github.com/shansixiong/geosearch',
    packages=[
        'geosearch',
    ],
    package_dir={'geosearch': 'geosearch'},
    include_package_data=True,
    package_data={
        'geosearch': ['geosearch/*.txt', 'geosearch/*.json'],
    },
    license="MIT",
    keywords='geosearch',
    classifiers=[],)