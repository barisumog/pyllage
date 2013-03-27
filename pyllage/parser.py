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


import html.parser


class PyllageParser(html.parser.HTMLParser):

    def __init__(self):
        super().__init__()
        self.counter = 1
        self.stack = {1: {"tag": "", "attrs": "", "data": []}}

    def handle_previous_tag(self):
        """Checks whether previously handled tag was significant."""
        previous_tag = self.stack[self.counter]
        if not (previous_tag["attrs"] or previous_tag["data"]):
            del self.stack[self.counter]
            self.counter -= 1

    def handle_starttag(self, tag, attrs):
        self.handle_previous_tag()
        self.counter += 1
        attrs_string = " | ".join("{}={}".format(*attr) for attr in attrs)
        self.stack[self.counter] = {"tag": tag, "attrs": attrs_string, "data": []}

    def handle_data(self, data):
        data = data.strip()
        if data:
            self.stack[self.counter]["data"].append(data)

    def handle_entityref(self, name):
        self.stack[self.counter]["data"].append(self.unescape("&{};".format(name)))

    def handle_charref(self, name):
        self.stack[self.counter]["data"].append(self.unescape("&#{};".format(name)))

    def freeze_data(self):
        """Converts all data lists into string."""
        self.handle_previous_tag()
        for key in self.stack:
            self.stack[key]["data"] = "".join(self.stack[key]["data"])


def parse(html):
    """Instantiate a parser to process html, return the stack."""
    parser = PyllageParser()
    parser.feed(html)
    parser.freeze_data()
    return parser.stack
