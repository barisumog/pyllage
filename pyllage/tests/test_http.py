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


from .. import http


def test_get():
    response = http.get("http://google.com")
    assert response["headers"] != {}
    assert response["status"] == 200
    assert b"google" in response["html"]
    assert response["codec"] != ""


def test_post():
    response = http.get("http://httpbin.org/post", method="POST", postdata=b"answer=42")
    assert response["headers"] != {}
    assert response["status"] == 200
    assert b"answer" in response["html"]
    assert b"42" in response["html"]
    assert response["codec"] != ""


def test_get_headers():
    response = http.get("http://httpbin.org/headers", {"Test": "pass"})
    assert b'"Test": "pass"' in response["html"]


def test_codec_in_headers():
    response = {"headers": {"Content-Type": "text/html; charset=ISO-8859-9"}}
    codec = http.codec_in_headers(response)
    assert codec == "ISO-8859-9"


def test_codec_in_headers_2():
    response = {"headers": {}}
    codec = http.codec_in_headers(response)
    assert codec is None


def test_codec_in_headers_no_charset():
    response = {"headers": {"Content-Type": "text/html;"}}
    codec = http.codec_in_headers(response)
    assert codec is None


def test_codec_in_html():
    html = b"""<html>\n<head>\n<meta http-equiv="content-type" content="text/html; charset=utf-16" />
               </head>\n<body>\nHello\nmeta http-equiv="content-type" content="text/html; charset=utf-8"
               </body></html>"""
    response = {"html": html}
    codec = http.codec_in_html(response)
    assert codec == "utf-16"


def test_codec_in_html_no_head():
    html = b"""<html>\n<meta http-equiv="content-type" content="text/html; charset=utf-16" />
               <body>\nHello\nmeta http-equiv="content-type" content="text/html; charset=utf-8"
               </body></html>"""
    response = {"html": html}
    codec = http.codec_in_html(response)
    assert codec is None


def test_codec_in_html_no_charset():
    html = b"""<html>\n<head>\n<meta http-equiv="content-type" content="text/html;" />
               </head>\n<body>\nHello\nmeta http-equiv="content-type" content="text/html; charset=utf-8"
               </body></html>"""
    response = {"html": html}
    codec = http.codec_in_html(response)
    assert codec is None


def test_get_codec():
    response = {"headers": {"Content-Type": "text/html; charset=ISO-8859-9"}}
    codec = http.get_codec(response)
    assert codec == "ISO-8859-9"


def test_get_codec_2():
    html = b"""<html>\n<head>\n<meta http-equiv="content-type" content="text/html; charset=utf-16" />
               </head>\n<body>\nHello\nmeta http-equiv="content-type" content="text/html; charset=utf-8"
               </body></html>"""
    response = {"headers": {"Content-Type": "text/html;"},
                "html": html}
    codec = http.get_codec(response)
    assert codec == "utf-16"


def test_get_codec_3():
    html = b"""<html>\n<head>\n<meta http-equiv="content-type" content="text/html;" />
               </head>\n<body>\nHello\n</body></html>"""
    response = {"headers": {"Content-Type": "text/html;"},
                "html": html}
    codec = http.get_codec(response)
    assert codec == "utf-8"
