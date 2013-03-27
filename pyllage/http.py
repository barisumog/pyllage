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


import urllib.request
import re


def get(url):
    """Http GET the url, return response, headers, status and codec."""
    response = {}
    request = urllib.request.Request(url)
    with urllib.request.urlopen(request) as resp:
        response["headers"] = dict(resp.getheaders())
        response["status"] = resp.status
        response["html"] = resp.read()
    response["codec"] = get_codec(response)
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
