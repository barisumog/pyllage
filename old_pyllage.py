#! /usr/bin/env python3
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


import urllib.request
import re
import html.parser


def simple_get(url):
    response = {}
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as resp:
        response["headers"] = dict(resp.getheaders())
        response["status"] = resp.status
        response["html"] = resp.read()
    return response


def codec_in_headers(response):
    """Check the response headers for codec information."""
    ct = response["headers"]["Content-Type"]
    if "charset=" in ct:
        return ct.split("charset=")[1]
    return None


def codec_in_html(response):
    """Check the <head> of the response html for codec information."""
    flag = re.DOTALL | re.IGNORECASE
    head = re.findall(b"<head>(.*)</head>", response["html"], flag)
    if not head:
        return None
    charset = re.findall(b'Content-Type.*?charset=(.*?)"', head[0], flag)
    if not charset:
        return None
    return charset[0].decode()


def get_codec(response):
    """Return appropriate codec information."""
    return codec_in_headers(response) or codec_in_html(response) or "utf-8"


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


def get_pyllage_stack(url):
    response = simple_get(url)
    codec = get_codec(response)
    decoded_html = response["html"].decode(codec)
    pyll = PyllageParser()
    pyll.feed(decoded_html)
    pyll.freeze_data()
    return pyll.stack, codec


def examine_stack(stack, filename, codec):
    """Writes a stack to file for examination."""
    output = []
    for key in range(1, len(stack) + 1):
        lines = []
        lines.append("{} | {} | {}".format(key, stack[key]["tag"], stack[key]["attrs"]))
        data = stack[key]["data"]
        if data:
            lines.append(data)
        lines.append("\n")
        output.append("\n".join(lines))
    with open(filename, "w", encoding=codec) as file:
        file.write("".join(output))


if __name__ == "__main__":
    url = input("url >")
    stack, codec = get_pyllage_stack(url)
    examine_stack(stack, "output", codec)
