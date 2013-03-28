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


def choose(stack, tag="", attrs="", data="", before=0, after=0):
    """Return lines in stack that match the given parameters."""
    selected = {}
    for key in stack:
        line = stack[key]
        if tag:
            tags = tag.split()
            if line["tag"] not in tags:
                continue
        if attrs:
            if attrs not in line["attrs"]:
                continue
        if data:
            if data not in line["data"]:
                continue
        selected[key] = line
        for i in range(1, before + 1):
            try:
                selected[key - i]= stack[key - i]
            except KeyError:
                pass
        for i in range(1, after + 1):
            try:
                selected[key + i]= stack[key + i]
            except KeyError:
                pass
    return selected


def index(stack):
    """Returns the index of line or lines in stack."""
    keys = list(sorted(stack.keys()))
    if len(keys) == 1:
        keys = keys[0]
    return keys


def between(start, stop, stack):
    """Return lines between the range, endpoints inclusive."""
    selected = {}
    for i in range(start, stop + 1):
        try:
            selected[i] = stack[i]
        except KeyError:
            pass
    return selected


def rip_data(stack):
    """Return a list of all data from stack."""
    data = []
    for key in sorted(stack.keys()):
        d = stack[key]["data"]
        if d:
            data.append(d)
    return data
