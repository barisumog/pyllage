
pyllage
=======

A web scraping tool in Python 3.

**pyllage** is a simple and practical tool to extract data
from web pages.

As opposed to full fledged scraping frameworks, it provides a
bare bones approach. The basic API allows quick testing of
ideas and easy integration with other tools and scripts.


Features
--------

* supports HTTP GET and POST requests

* allows custom request headers (cookies, user-agents, etc)

* adjusts encoding according to *Content-Type* information in either the response headers, or the <head> of the html document

* custom parser built upon the standard HTMLParser class

* practical selectors for extracting data (no tree traversal or XPath)


Requirements
------------

Currently, all package functionality is built upon the standard library.
This may or may not change in the future.

Tests are written to **py.test**, so that's a requirement if you want to
run the bundled tests.


Installing
----------

::

    pip install pyllage



Quick Start
-----------

Here's a few quick examples illustrating *some* of the functions::

    import pyllage
    stack = pyllage.get_stack("http://somesite.com/etcetera")
    
    # get all links, print the href=... parts
    
    links = pyllage.choose(stack, tag="a")
    for key in links:
        print(links[key]["attrs"])
    
    # get all text data except scripts and print it
    
    texts = pyllage.choose(stack, tag="script", select=False)
    data = pyllage.rip_data(texts)
    print("\n".join(data))
    
    # get all spans and divs with class=help (but not class=helpmore)
    
    helps = pyllage.choose(stack, tag="span div", attrs="class=help", exact=True)
    
    # get all divs containing the word pyllage in their text part
    
    pylls = pyllage.choose(stack, tag="div", data="pyllage")


How the parser works & The stack
--------------------------------

The parser spits out a dictionary that we call the *stack*.

It's looks something like this::

    {1: {"tag": "div", "attrs": "class=main", "data": ""},
     2: {"tag": "p", "attrs": "", "data": "Hello world"},
     3: {"tag": "span", "attrs": "class=red bold", "data": "Exclaim!"},
     4: {"tag": "a", "attrs": 'href="http://somewhere"', "data": "click me"}}

The keys of *stack* are consecutive integers starting from 1.

While parsing an html document, the parser creates a new entry in the *stack* every time
it finds an opening tag. Every entry itself is a dictionary with 3 items:

``tag`` is the tag name of the encountered tag

``attrs`` is everything else inside the opening bracket (class, id, style, href, etc.)

``data`` is the text that is parsed *after* the opening bracket, and before the closing
bracket (or a new opening bracket)

For example: ``<div id=main_div>Hello</div>``

``tag`` is "div"

``attrs`` is "id=main_div"

``data`` is "Hello"

While parsing the html and populating the *stack* this way, the parser prunes *insignificant*
entries (entries with no attrs or data). For example:

``<div><span>Hello</span></div>``

The outer div here won't be included in the *stack*, since it doesn't have any useful
info (no class or id etc, and no direct data).

Some tags may have more than 1 attribute. These will be concatenated into a single string
like this:

``<div class="wrapper" style="float:left;"></div>`` will parse into:

``{'tag': 'div', 'attrs': 'class=wrapper | style=float:left;', 'data': ''}``


API
---

Functions for retrieving the stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pyllage.get_stack(url, headers={}, method="GET", postdata=None, filename=""):
    """Wraps http request and parsing. Also allows stack write."""

This is the main utility function for retrieving the stack from a url. It wraps the
functionality of the 3 functions below, providing a shortcut. Normally, you can just
use ``get_stack`` unless you need to interfere with the **url -> stack** process.

``headers`` lets you include cookies or user-agent strings.

``method`` is either "GET" or "POST".

``postdata`` is a bytes object containing data to be sent to the server for POST requests.

If ``filename`` is given, the returned stack will also be written to disk, allowing
for inspecting with a text editor.


::

    pyllage.get(url, headers={} method="GET", postdata=None):
    """Http request the url, return response, headers, status and codec."""

Raw function that makes the Http request.

``response = get("http://somesite.com", {"Cookie": "valid=true;"})``

``response = get("http://othersite.com", method="POST", postdata=b"answer=42")``

The function returns a dictionary with the following keys:

``headers`` contains the received http headers (may include cookies, etc)

``status`` is an integer representing the status message returned by the server
(200 = OK, 404 = Not found, etc)

``html`` contains the body of the response. Note that this is of *bytes* type.

``codec`` is a string containing the encoding declared in the http response.
**pyllage** looks at the response headers for a *Content-Type* with charset
value. If there's none, it looks at the <head> part of the html body. If there's no
codec information there, it defaults to *utf-8*.


::

    pyllage.parse(html):
    """Instantiate a parser to process html, return the stack."""

Please note that the html must be decoded into a string before it can be parsed.
The ``get_stack`` function handles this automatically.


::

    pyllage.stack_to_file(filename, stack, codec):
    """Write a stack to file with formatting."""

Writes the stack to a file on disk. Note that it **overwrites** any existing data in the given file.


Selector functions for operating on the stack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    pyllage.choose(stack, tag=None, attrs=None, data=None, select=True, exact=False):
    """Returns a dictionary of items from stack that fit given criteria.

    If select is True, returns items that fit criteria. If False, returns all others.
    If exact is False, compares tag, attrs and data flexibly.
    If exact is True, compares tag, attrs and data exactly as given."""

Main selector function. Examples:

``pyllage.choose(stack, tag="a")``
Returns all <a> entries.

``pyllage.choose(stack, tag="div span a", select=False)``
Returns all entries with tags other than <div>, <span>, or <a>.

``pyllage.choose(stack, tag="div", attrs="id=")``
Returns all <div> entries with an *id* attribute.

``pyllage.choose(stack, attrs="class=blue", exact=True)``
Returns all entries with **exactly** the attribute "class=blue" (won't select "class=blue button" for example)

``pyllage.choose(stack, data="", exact=True, select=False)``
Returns all entries with non-empty data.

::

    pyllage.relative(stack, index, offset=1, count=1):
    """Returns count number of items, starting at offset from index.

    With defaults, it just returns the next item.
    Offset can be negative, count must be greater than 1."""

``index`` is the integer key for the base item in stack.
Useful for extracting data from tags with no id or class attribute.

E.g. something like ``<div class="x"><span>The data you need is</span><span>42</span></div>``
When you can select the wrapping div with its class, and then using its index, call
``pyllage.relative(stack, index, 2, 1)``

``pyllage.relative(stack, index, -5, count=4)``
Returns the 4 entries that comes right before the given index.

Note that this function works as expected on stacks that you have manipulated. That is,
if the indexes in your stack are [3, 5, 88, 101], then ``pyllage.relative(stack, 5)`` will
give the entry at 88.


::

    pyllage.rip_data(stack):
    """Returns an ordered list of non-blank data values in stack."""

For getting the data after you have selected the entry.

::

    pyllage.rip_index(stack):
    """Returns an ordered list of the indexes in stack."""

Useful for doing batch operations with ``pyllage.relative``. For example::

    links = pyllage.choose(stack, tag="a")      # choose all links
    link_inds = pyllage.rip_index(links)        # get the indexes
    new_stack = {}
    for i in link_inds:
        new_stack.update(pyllage.relative(stack, i))

Now ``new_stack`` contains all the elements directly following an <a> tag.

::

    pyllage.between(stack, start, stop):
    """Returns items between given indexes, inclusive."""

When you have a very large document, and you're only interested in a certain
part of it, you can use this crop the stack.

Also works as expected in manipulated stacks. Say your stack indexes are
[3, 5, 88, 101]. ``pyllage.between(stack, 50, 90)`` will return the item at 88.



Feedback
--------

**pyllage** is currently under development, so more features are on their way.

If you have any ideas about features, or would like some new selector functions,
feel free to open an issue on Github.


License
-------

**pyllage** is open sourced under GPLv3.

