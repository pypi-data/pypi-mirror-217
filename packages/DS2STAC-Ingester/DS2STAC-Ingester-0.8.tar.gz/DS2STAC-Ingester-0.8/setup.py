#!/usr/bin/env python

"""Setup script for the DS2STAC-Ingester package."""

from setuptools import setup, find_packages
import versioneer
from setuptools import setup

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description_content_type = 'text/x-rst',
)

