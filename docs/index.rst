Welcome to Flask RSTPages's documentation!
==========================================

.. module:: flask_rstpages


Flask-RSTPages adds support for `reStructuredText`_ to your `Flask`_
application, allowing to convert a reStructuredText file to html.

* BSD licensed
* Latest documentation on `python.org`_
* Source, issues and pull requests on `Github`_
* Releases on `PyPI`_

.. _Flask: http://flask.pocoo.org/
.. _reStructuredText: http://docutils.sourceforge.net/rst.html
.. _python.org: http://packages.python.org/Flask-RSTPages/
.. _Github: https://github.com/saimn/Flask-RSTPages/
.. _PyPI: http://pypi.python.org/pypi/Flask-RSTPages

Installation
------------

Install the extension with one of the following commands::

    $ easy_install Flask-RSTPages

or alternatively if you have pip installed::

    $ pip install Flask-RSTPages

How to Use
----------

To get started you must construct a :class:`RSTPages` object with your
:class:`~flask.Flask` instance::

       from flask.ext.rstpages import RSTPages
       pages = RSTPages(app)

Then, you can use the :func:`RSTPages.get` method to convert your
reStructuredText file to html::

       @app.route('/<path:page>/')
       def get_page(page):
           html = pages.get(page)
           return render_template("page.html", page=html)

The :func:`RSTPages.get` returns an object with ``title`` and ``body``
attributes.

Configuration
-------------

Flask-RSTPages accepts the following configuration values.

``RSTPAGES_SRC``
    Path to the directory where to look for page files. Defaults to ``pages``.

``RSTPAGES_VIEW_FUNCTION``
    The view function used to route pages. This is used to support the
    ``:doc:`page``` markup of Sphinx to `cross-reference`_ documents.
    Defaults to ``get_rstpage``.

.. _cross-reference: http://sphinx-doc.org/markup/inline.html#cross-referencing-documents

API Reference
-------------

.. autoclass:: RSTPages
   :members:


Changelog
---------

Version 0.1
~~~~~~~~~~~

Released on 2012-xx-xx.

First public release.