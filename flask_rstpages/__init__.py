# -*- coding:utf-8 -*-

from __future__ import absolute_import

import re

from flask import abort, safe_join, current_app, url_for
from jinja2 import TemplateNotFound
from docutils import nodes, utils
from docutils.parsers.rst import roles

# import the directives to have pygments support
from . import rstdirectives  # NOQA
from .parsers import rstDocument

#-----------------------------------------------------------------------------
# RST roles definition

_abbr_re = re.compile('\((.*)\)$')


class abbreviation(nodes.Inline, nodes.TextElement):
    pass


def abbr_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    m = _abbr_re.search(text)
    if m is None:
        return [abbreviation(text, text)], []
    abbr = text[:m.start()].strip()
    expl = m.group(1)
    return [abbreviation(abbr, abbr, explanation=expl)], []

roles.register_local_role('abbr', abbr_role)


def doc_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    text = utils.unescape(text)
    ref = url_for(current_app.config['RSTPAGES_VIEW_FUNCTION'], page=text)
    rst_file = safe_join(current_app.config['RSTPAGES_SRC'], text + '.rst')
    rst = rstDocument(rst_file)

    roles.set_classes(options)
    node = nodes.reference(rawtext, rst.title, refuri=ref, **options)
    return [node], []

roles.register_local_role('doc', doc_role)

#-----------------------------------------------------------------------------
# Main class


class RSTPages(object):

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
        try:
            rst_file = safe_join(current_app.config['RSTPAGES_SRC'],
                                 page + '.rst')
            return rstDocument(rst_file)
        except TemplateNotFound:
            abort(404)
