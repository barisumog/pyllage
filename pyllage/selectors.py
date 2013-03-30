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


def choose(stack, tag=None, attrs=None, data=None, select=True, exact=False):
    """Returns a dictionary of items from stack that fit given criteria.

    If select is True, returns items that fit criteria. If False, returns all others.
    If exact is False, compares tag, attrs and data flexibly.
    If exact is True, compares tag, attrs and data exactly as given."""
    if (tag is not None) and not exact:
        tag = tag.split()
    chosen = {}
    for key in stack:
        item = stack[key]
        if tag is not None:
            if exact and tag != item["tag"]:
                continue
            if item["tag"] not in tag:
                continue
        if attrs is not None:
            if exact and attrs != item["attrs"]:
                continue
            if attrs not in item["attrs"]:
                continue
        if data is not None:
            if exact and data != item["data"]:
                continue
            if data not in item["data"]:
                continue
        chosen[key] = item
    if select:
        return chosen
    others = {}
    for key in stack:
        if key not in chosen:
            others[key] = stack[key]
    return others


def relative(stack, index, offset=1, count=1):
    """Returns count number of items, starting at offset from index.

    With defaults, it just returns the next item.
    Offset can be negative, count must be greater than 1."""
    if count < 1:
        raise ValueError("count < 1")
    keys = sorted(stack.keys())
    try:
        start = keys.index(index) + offset
    except ValueError as ve:
        raise ValueError("index not in stack") from ve
    if start < 0 or start > (len(keys) - 1):
        raise ValueError("offset out of range")
    if start + count > len(keys):
        raise ValueError("count out of range")
    chosen = {}
    for i in range(count):
        key = keys[start + i]
        chosen[key] = stack[key]
    return chosen


def rip_data(stack):
    """Returns an ordered list of non-blank data values in stack."""
    keys = sorted(stack.keys())
    data = []
    for k in keys:
        d = stack[k]["data"]
        if d:
            data.append(d)
    return data


def rip_index(stack):
    """Returns an ordered list of the indexes in stack."""
    return sorted(stack.keys())


def between(stack, start, stop):
    """Returns items between given indexes, inclusive."""
    chosen = {}
    for i in range(start, stop + 1):
        if i in stack:
            chosen[i] = stack[i]
    return chosen
