#!/usr/bin/env python3
# coding: utf-8

from setuptools import setup


setup(
    package_dir={'': 'src'},
    packages=['pimock'],
    install_requires=['jsonschema'],
)
