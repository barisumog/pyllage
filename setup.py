#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# pyllage
#
# Copyright (C) 2013 barisumog at gmail.com
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
#

from setuptools import setup, find_packages
import pyllage


with open("README.rst") as file:
    long_description = file.read()


setup(name='pyllage',
      version=pyllage.__version__,
      description='A web scraping tool in Python 3',
      long_description=long_description,
      author='barisumog',
      author_email='barisumog@gmail.com',
      url='https://github.com/barisumog/pyllage',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      keywords="web scraper scraping",
      license="GPLv3"
     )
