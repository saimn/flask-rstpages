# -*- coding:utf-8 -*-
"""
flask_rstpages
~~~~~~~~~~~~~~

Flask-RSTPages adds support for reStructuredText to your Flask application.

:copyright: (c) 2012 by Simon Conseil.
:license: BSD, see LICENSE for more details.

"""

from __future__ import absolute_import

from flask import abort, safe_join, current_app, url_for
from jinja2 import TemplateNotFound
from docutils import nodes, utils
from docutils.parsers.rst import roles

# import the directives to have pygments support
from . import rstdirectives  # NOQA
from .parsers import rstDocument


def doc_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Cross-referencing documents

    Add the ``:doc:`` role of Sphinx to link to documents.
    ``:doc:\`example\``` will link to the ``example.rst`` document in the
    pages directory, using Flask's ``url_for`` function to determine the url
    of the page.

    """

    text = utils.unescape(text)
    ref = url_for(current_app.config['RSTPAGES_VIEW_FUNCTION'], page=text)
    rst_file = safe_join(current_app.config['RSTPAGES_SRC'], text + '.rst')
    rst = rstDocument(rst_file)

    roles.set_classes(options)
    node = nodes.reference(rawtext, rst.title, refuri=ref, **options)
    return [node], []

roles.register_local_role('doc', doc_role)


class RSTPages(object):
    "reStructuredText to html renderer"

    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        app.config.setdefault('RSTPAGES_SRC', 'pages')
        app.config.setdefault('RSTPAGES_URL', 'pages')
        app.config.setdefault('RSTPAGES_VIEW_FUNCTION', 'get_rstpage')

    def get(self, page):
        "Convert `page` to reStructuredText and return a `rstDocument`"

        try:
            rst_file = safe_join(current_app.config['RSTPAGES_SRC'],
                                 page + '.rst')
            return rstDocument(rst_file)
        except TemplateNotFound:
            abort(404)