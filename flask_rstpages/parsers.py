# -*- coding: utf-8 -*-
"""
reStructuredText parser
~~~~~~~~~~~~~~~~~~~~~~~

This module provides a reStructuredText parser based on the parser of
``flask-rst`` (see below), modified with a HTMLTranslator class to redefine
some stuff: abbreviations, no border for tables by default.

flask-rst.parsers
-----------------

    :copyright: (c) 2011 by Christoph Heer.
    :license: BSD, see LICENSE for more details.
    :source: https://github.com/jarus/flask-rst/blob/master/flaskrst/parsers.py

"""

from __future__ import with_statement

import os
import re

from flask import abort
from jinja2 import Markup
from docutils.core import publish_parts
from docutils.writers import html4css1

config_parser_re = re.compile(r"^:(\w+): ?(.*?)$", re.M)


class Writer(html4css1.Writer):
    "Subclass the html4css1.Writer to redefine the translator_class"

    def __init__(self):
        html4css1.writers.Writer.__init__(self)
        self.translator_class = HTMLTranslator


class HTMLTranslator(html4css1.HTMLTranslator):
    """HTMLTranslator class to redefine some stuff:

    - no border for tables by default !
    - abbreviations
    """

    def visit_abbreviation(self, node):
        attrs = {}
        if node.hasattr('explanation'):
            attrs['title'] = node['explanation']
        self.body.append(self.starttag(node, 'abbr', '', **attrs))

    def depart_abbreviation(self, node):
        self.body.append('</abbr>')

    def visit_table(self, node):
        classes = ' '.join(['docutils', self.settings.table_style]).strip()
        self.body.append(
            self.starttag(node, 'table', CLASS=classes))

    def depart_table(self, node):
        self.body.append('</table>\n')


class rstDocument(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = ".".join(os.path.basename(self.file_path).split(".")[:-1])
        self._config = None
        self._rst = None
        if not os.path.isfile(self.file_path):
            abort(404)
        with open(self.file_path) as f:
            self.raw = f.read()

    @property
    def config(self):
        if not isinstance(self._config, dict):
            self._config = {}
            for m in config_parser_re.finditer(self.raw):
                self._config[m.group(1)] = eval(m.group(2))
            self._config.setdefault('public', False)
        return self._config

    @property
    def rst(self):
        writer = Writer()

        if not isinstance(self._rst, dict):
            settings = {
                'initial_header_level': 2,
                #'table_style': 'borderless'
            }

            self._rst = publish_parts(source=self.raw,
                                      writer=writer,
                                      settings_overrides=settings)
        return self._rst

    @property
    def title(self):
        return Markup(self.rst['title']).striptags()

    @property
    def body(self):
        return Markup(self.rst['fragment'])

    def __repr__(self):
        return "<rstDocument %s>" % (self.file_name)
