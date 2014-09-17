#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

import base64
import markdown

_extensions = ["nl2br", "codehilite"]


def md_parse(md_str):
    html_str = markdown.markdown(md_str.decode(encoding='utf-8'),
                                 _extensions,
                                 safe_mode=True,
                                 enable_attributes=False)
    return html_str


def encrypt(s):
    return base64.encodestring(s).strip()


def decrypt(s):
    return base64.decodestring(s)

if __name__ == "__main__":
    s =  encrypt("E:/workspace/my/note/note/python/sphinx/introduce.md")
    print s
    print decrypt(s)
