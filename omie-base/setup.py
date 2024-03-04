# -*- coding: utf-8 -*-
"""Setup per la llibreria de omie"""
from __future__ import print_function

import os
import shutil
from distutils.command.clean import clean as _clean
from setuptools import setup, find_packages

PACKAGES_DATA = {'omie': ['data/*.xsd']}

with open('requirements.txt', 'r') as f:
    INSTALL_REQUIRES = f.readlines()


class Clean(_clean):
    """Eliminem el directory build i els bindings creats."""

    def run(self):
        """Comença la tasca de neteja."""
        _clean.run(self)
        if os.path.exists(self.build_base):
            print("Cleaning {} dir".format(self.build_base))
            shutil.rmtree(self.build_base)


setup(
    name='omie',
    description='Libreria de interacción con OMIE',
    author='Adrià Orellana',
    author_email='aorellana@gisce.net',
    url='http://www.gisce.net',
    license='General Public Licence 2',
    long_description='''Long description''',
    provides=['omie'],
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    package_data=PACKAGES_DATA,
    scripts=[],
    cmdclass={'clean': Clean},
    test_suite='tests',
    entry_points='''
      [console_scripts]
      atr=omie.cli:atr
    '''
)