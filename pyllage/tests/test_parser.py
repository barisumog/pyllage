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


from .. import parser


def test_init():
    p = parser.PyllageParser()
    assert p.stack == {1: {"tag": "", "attrs": "", "data": []}}
    assert p.counter == 1


def test_handle_previous_tag():
    p = parser.PyllageParser()
    p.handle_previous_tag()
    assert p.counter == 0
    assert p.stack == {}


def test_PyllageParser():
    p = parser.PyllageParser()
    html = """<html>
              <body style="somestyle">
              <p>Hello</p>
              <div class="wrap">
              Div data
              <p>&gt;</p>
              <p>&#62;&#x3E;</p>
              <p></p>
              </div>
              </body>
              <!-- comment -->
              </html>"""
    p.feed(html)
    assert p.counter == 6
    assert p.stack == {1: {"tag": "body", "attrs": "style=somestyle", "data": []},
                       2: {"tag": "p", "attrs": "", "data": ["Hello"]},
                       3: {"tag": "div", "attrs": "class=wrap", "data": ["Div data"]},
                       4: {"tag": "p", "attrs": "", "data": [">"]},
                       5: {"tag": "p", "attrs": "", "data": [">", ">"]},
                       6: {"tag": "p", "attrs": "", "data": []}}


def test_parse():
    html = """<html>
              <body style="somestyle">
              <p>Hello</p>
              <div class="wrap">
              Div data
              <p>&gt;</p>
              <p>&#62;&#x3E;</p>
              <p></p>
              </div>
              </body>
              <!-- comment -->
              </html>"""
    stack = parser.parse(html)
    assert stack == {1: {"tag": "body", "attrs": "style=somestyle", "data": ""},
                     2: {"tag": "p", "attrs": "", "data": "Hello"},
                     3: {"tag": "div", "attrs": "class=wrap", "data": "Div data"},
                     4: {"tag": "p", "attrs": "", "data": ">"},
                     5: {"tag": "p", "attrs": "", "data": ">>"}}
