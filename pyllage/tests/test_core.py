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


#
# Tests for the pyllage package, using py.test
#


from .. import core
from .. import parser


def test_stack_to_file():
    html = '<p class="ex">Hello</p>'
    stack = parser.parse(html)
    core.stack_to_file("test.stack", stack, "utf-8")
    with open("test.stack") as file:
        data = file.read()
    assert data == "1 | p | class=ex\nHello\n\n"
