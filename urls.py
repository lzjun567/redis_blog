#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'
from handlers.blog_service import ArchivesHandler
from handlers.blog_service import ArticleHandler
from handlers.blog_service import CategoryHandler
from handlers.blog_service import AboutHandler
from handlers.blog_service import IndexHandler
from handlers.auth_service import AuthLoginHandler
from handlers.auth_service import AuthLogoutHandler
from handlers.admin_service import AdminHandler
from handlers.admin_service import AdminPublishHandler
url_patterns = [
    (r"/auth/login/?", AuthLoginHandler),
    (r"/auth/logout/?", AuthLogoutHandler),

    (r"/admin/publish/?", AdminPublishHandler),
    (r"/admin/?", AdminHandler),
    (r"^/$", IndexHandler),
    (r"/archives/?", ArchivesHandler),
    (r"/category/(.+)/?", CategoryHandler),
    (r"/about/?", AboutHandler),
    (r"/(.+\.md)/?", ArticleHandler),
]
