#
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


from .http import get
from .parser import parse
from .selectors import choose, relative, rip_data, rip_index, between
from .utils import stack_to_file, get_stack


__title__ = "pyllage"
__version__ = "0.1.0"
__author__ = "barisumog at gmail.com"
__copyright__ = "copyright 2013 barisumog"
__license__ = "GPLv3"
__doc__ = """Please see the README.rst for full documentation.

Quick Start
-----------

Here's a few quick examples illustrating *some* of the functions::

    import pyllage
    stack = pyllage.get_stack("http://somesite.com/etcetera")
    
    # get all links, print the href=... parts
    
    links = pyllage.choose(stack, tag="a")
    for key in links:
        print(links[key]["attrs"])
    
    # get all text data except scripts and print it
    
    texts = pyllage.choose(stack, tag="script", select=False)
    data = pyllage.rip_data(texts)
    print("\n".join(data))
    
    # get all spans and divs with class=help (but not class=helpmore)
    
    helps = pyllage.choose(stack, tag="span div", attrs="class=help", exact=True)
    
    # get all divs containing the word pyllage in their text part
    
    pylls = pyllage.choose(stack, tag="div", data="pyllage")
"""