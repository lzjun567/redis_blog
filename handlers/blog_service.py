#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

from handlers.base import BaseHandler
import logging
from models import Blog
from cache import cache


logger = logging.getLogger('foofish.' + __name__)


class IndexHandler(BaseHandler):
    @cache
    def get(self):
        latest_blog_id = self.redis.zrange('blog.list', -1, -1)[0]
        post = self.redis.hgetall(latest_blog_id)
        blog = Blog(id=latest_blog_id, **post)
        self.render("blog-post.html", blog=blog)


class ArchivesHandler(BaseHandler):
    def get(self):
        blog_ids = self.redis.zrevrange('blog.list', 0, -1)
        blogs = [Blog(id=b_id, **self.redis.hgetall(b_id)) for b_id in blog_ids]
        self.render("archives.html", blogs=blogs)


class ArticleHandler(BaseHandler):

    @cache
    def get(self, blog_id):
        post = self.redis.hgetall(blog_id)
        blog = Blog(id=blog_id, **post)
        self.render("blog-post.html", blog=blog)


class CategoryHandler(BaseHandler):
    def get(self, tag):
        key = 'blog.tag.%s' % tag
        blog_ids = self.redis.zrevrange(key, 0, -1)
        blogs = [Blog(id=b_id, **self.redis.hgetall(b_id)) for b_id in blog_ids if self.redis.hgetall(b_id)]
        self.render("archives.html", blogs=blogs)


class AboutHandler(BaseHandler):
    def get(self):
        self.render("about.html")
