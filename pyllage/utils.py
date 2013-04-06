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

def stack_to_file(filename, stack, codec):
    """Write a stack to file with formatting."""
    # Utility function to help with inspecting and debugging the stack
    # Note that it **OVERWRITES** any existing data in the given file
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


def get_stack(url, headers={}, method="GET", postdata=None, filename=""):
    """Wraps http get and parsing. Also allows stack write."""
    response = get(url, headers, method, postdata)
    codec = response["codec"]
    html = response["html"].decode(codec)
    stack = parse(html)
    if filename:
        stack_to_file(filename, stack, codec)
    return stack
