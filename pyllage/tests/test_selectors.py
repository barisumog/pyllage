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


from .. import selectors


def test_choose():
    stack = {1: {"tag": "p", "attrs": "", "data": "Hello"},
             2: {"tag": "div", "attrs": "class=x", "data": "p"},
             3: {"tag": "a", "attrs": "", "data": "p"},
             4: {"tag": "p", "attrs": "class=x", "data": "nop"},
             5: {"tag": "p", "attrs": "class=x", "data": "nop"}}
    sel = selectors.choose(stack, tag="a", before=2, after=1)
    assert sel == {1: {"tag": "p", "attrs": "", "data": "Hello"},
                   2: {"tag": "div", "attrs": "class=x", "data": "p"},
                   3: {"tag": "a", "attrs": "", "data": "p"},
                   4: {"tag": "p", "attrs": "class=x", "data": "nop"}}

def test_choose_2():
    stack = {1: {"tag": "p", "attrs": "", "data": "Hello"},
             2: {"tag": "div", "attrs": "class=x", "data": "p"},
             3: {"tag": "a", "attrs": "", "data": "p"},
             4: {"tag": "p", "attrs": "class=x", "data": "nop"},
             5: {"tag": "p", "attrs": "class=x", "data": "nop"}}
    sel = selectors.choose(stack, data="Hello", before=2, after=1)
    assert sel == {1: {"tag": "p", "attrs": "", "data": "Hello"},
                   2: {"tag": "div", "attrs": "class=x", "data": "p"}}

def test_choose_3():
    stack = {1: {"tag": "p", "attrs": "", "data": "Hello"},
             2: {"tag": "div", "attrs": "class=x", "data": "p"},
             3: {"tag": "a", "attrs": "", "data": "p"},
             4: {"tag": "p", "attrs": "class=tux", "data": "nop"},
             5: {"tag": "p", "attrs": "class=x", "data": "nop"}}
    sel = selectors.choose(stack, attrs="tux", after=3)
    assert sel == {4: {"tag": "p", "attrs": "class=tux", "data": "nop"},
                   5: {"tag": "p", "attrs": "class=x", "data": "nop"}}


def test_index():
    stack = {1: {"tag": "p", "attrs": "", "data": "Hello"},
             2: {"tag": "div", "attrs": "class=x", "data": "p"}}
    keys = selectors.index(stack)
    assert keys == [1, 2]

def test_index_2():
    stack = {1: {"tag": "p", "attrs": "", "data": "Hello"}}
    keys = selectors.index(stack)
    assert keys == 1


def test_between():
    stack = {1: {"tag": "p", "attrs": "", "data": "Hello"},
             3: {"tag": "div", "attrs": "class=x", "data": "p"},
             5: {"tag": "a", "attrs": "", "data": "p"},
             8: {"tag": "p", "attrs": "class=x", "data": "nop"}}
    sel = selectors.between(2, 6, stack)
    assert sel == {3: {"tag": "div", "attrs": "class=x", "data": "p"},
                   5: {"tag": "a", "attrs": "", "data": "p"}}


def test_rip_data():
    stack = {1: {"tag": "p", "attrs": "", "data": "Hello"},
             3: {"tag": "div", "attrs": "class=x", "data": "p"},
             5: {"tag": "a", "attrs": "", "data": ""},
             8: {"tag": "p", "attrs": "class=x", "data": "nop"}}
    data = selectors.rip_data(stack)
    assert data == ["Hello", "p", "nop"]
