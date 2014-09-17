#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'
import datetime


class Blog(object):
    def __init__(self, id="", title='', content='', create_at=""):
        self.id = id
        self.title = title
        self.content = content
        if isinstance(create_at, basestring) and create_at.isdigit():
            self.create_at = datetime.datetime.fromtimestamp(int(create_at))
        else:
            self.create_at = datetime.datetime.now()

    def __repr__(self):
        return 'id:%s,title:%s,create_at:%s' % (self.id, self.title, self.create_at)
