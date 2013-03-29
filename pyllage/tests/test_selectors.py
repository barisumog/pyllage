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
import pytest


stack = {1: {"tag": "div", "attrs": "", "data": "div 1 here"},
         2: {"tag": "p", "attrs": "class=x", "data": "hello"},
         3: {"tag": "p", "attrs": "", "data": "world"},
         4: {"tag": "span", "attrs": "class=x", "data": ""},
         5: {"tag": "div", "attrs": "class=y", "data": "div 2 now"}}


def test_choose_tags():
    c = selectors.choose(stack, tag="p div")
    assert c == {1: {"tag": "div", "attrs": "", "data": "div 1 here"},
                 2: {"tag": "p", "attrs": "class=x", "data": "hello"},
                 3: {"tag": "p", "attrs": "", "data": "world"},
                 5: {"tag": "div", "attrs": "class=y", "data": "div 2 now"}}


def test_choose_tags_exact():
    c = selectors.choose(stack, tag="span", exact=True)
    assert c == {4: {"tag": "span", "attrs": "class=x", "data": ""}}


def test_choose_attrs():
    c = selectors.choose(stack, attrs="class")
    assert c == {2: {"tag": "p", "attrs": "class=x", "data": "hello"},
                 4: {"tag": "span", "attrs": "class=x", "data": ""},
                 5: {"tag": "div", "attrs": "class=y", "data": "div 2 now"}}


def test_choose_attrs_exact():
    c = selectors.choose(stack, attrs="class=y", exact=True)
    assert c == {5: {"tag": "div", "attrs": "class=y", "data": "div 2 now"}}


def test_choose_data():
    c = selectors.choose(stack, data="he")
    assert c == {1: {"tag": "div", "attrs": "", "data": "div 1 here"},
                 2: {"tag": "p", "attrs": "class=x", "data": "hello"}}


def test_choose_data_exact():
    c = selectors.choose(stack, data="", exact=True)
    assert c == {4: {"tag": "span", "attrs": "class=x", "data": ""}}


def test_choose_select():
    c = selectors.choose(stack, attrs="", exact=True, select=False)
    assert c == {2: {"tag": "p", "attrs": "class=x", "data": "hello"},
                 4: {"tag": "span", "attrs": "class=x", "data": ""},
                 5: {"tag": "div", "attrs": "class=y", "data": "div 2 now"}}


def test_relative_invalid_count():
    with pytest.raises(ValueError) as e:
        c = selectors.relative(stack, 3, count=0)
    assert e.value.args[0] == "count < 1"


def test_relative_invalid_index():
    with pytest.raises(ValueError) as e:
        c = selectors.relative(stack, 7)
    assert e.value.args[0] == "index not in stack"


def test_relative_invalid_offset():
    with pytest.raises(ValueError) as e:
        c = selectors.relative(stack, 3, offset=3)
    assert e.value.args[0] == "offset out of range"


def test_relative_over_count():
    with pytest.raises(ValueError) as e:
        c = selectors.relative(stack, 3, offset=1, count=3)
    assert e.value.args[0] == "count out of range"


def test_relative_defaults():
    c = selectors.relative(stack, 4)
    assert c == {5: {"tag": "div", "attrs": "class=y", "data": "div 2 now"}}


def test_relative_negative_offset():
    c = selectors.relative(stack, 4, offset=-2, count=2)
    assert c =={2: {"tag": "p", "attrs": "class=x", "data": "hello"},
                3: {"tag": "p", "attrs": "", "data": "world"}}

