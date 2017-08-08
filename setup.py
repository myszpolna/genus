#!/usr/bin/env python
#
# Genus - Compute topological characteristic for Protein structure
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='genus',
    version='1.0',
    description='Compute genus for Protein and RNA structures',
    long_description=long_description,
    keywords='Protein, Genus analysis',
    url='https://github.com/sebkaz/genus',
    author='Joanna Sułkowska, Piotr Sułkowski, Sebastian Zając',
    author_email='s.zajac@ukw.edu.pl',
    license='GPL-3.0',
    platforms=['Linux', 'Mac OS X'],
    classifiers=['Environment :: Console',
                 'Development Status :: 4 - Beta',
                 'Topic :: RNA :: Proteins',
                 'License :: OSI Approved :: GNU General Public License v3'
                 '(GPLv3+)',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6', ],
    packages=['genus'],
    install_requires=['numpy', 'pandas'],
    include_package_data=True,
    zip_safe=False)
