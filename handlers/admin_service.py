#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

from tornado.web import authenticated
import tornado.web
from cache import cache
from base import BaseHandler
import utils


class AdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        all_archives = self.redis.zrevrange("admin.blog.list", 0, -1)
        all_archives = [(blog_id, utils.decrypt(blog_id)) for blog_id in all_archives]
        self.render('admin.html', archives=all_archives)


class AdminPublishHandler(BaseHandler):
    @cache
    def post(self):
        blog_ids = self.get_arguments("blog_id")
        data = []
        for blog_id in blog_ids:
            create_time = self.redis.zscore('admin.blog.list', blog_id)
            if not create_time:
                self.write(u"文档不存在")
                self.finish()
                return
            else:
                data.append((create_time, blog_id))
        for d in data:
            self.redis.zadd('blog.list', d[0], d[1])
        # self.write(u"操作成功")
        self.redirect("/archives")