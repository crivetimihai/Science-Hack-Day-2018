#!/usr/bin/env Python3

from setuptools import setup

setup(
        package_dir = {'':'src'},
        packages = ['campie'],
        install_requires =['flask','PiCamera'])
