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
import os


def test_stack_to_file(tmpdir):
    d = tmpdir.mkdir("pyllage_test").chdir()
    stack = {1: {"tag": "p", "attrs": "class=ex", "data": "Hello"}}
    core.stack_to_file("test.stack", stack, "utf-8")
    with open("test.stack") as file:
        data = file.read()
    assert data == "1 | p | class=ex\nHello\n\n"


def test_get_stack(tmpdir):
    d = tmpdir.mkdir("pyllage_test").chdir()
    stack = core.get_stack("http://google.com", filename="test.out")
    assert bool(stack)
    with open("test.out") as file:
        data = file.read(10)
    assert bool(data)
