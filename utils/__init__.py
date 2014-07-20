#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

import markdown

_extensions = ["nl2br", "codehilite"]


def md_parse(md_str):
    html_str = markdown.markdown(md_str.decode(encoding='utf-8'),
                                 _extensions,
                                 safe_mode=True,
                                 enable_attributes=False)
    return html_str
