#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

from handlers.base import BaseHandler
from tornado.escape import json_encode
from tornado.escape import url_escape

import settings

class AuthLoginHandler(BaseHandler):
    def get(self):
        error_message = self.get_argument("error", '')
        self.render("login.html", error_msg=error_message)

    def check_permission(self, username, password):
        return username == settings.USERNAME and password == settings.PASSWORD

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        auth = self.check_permission(username, password)
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"用户名或密码错误"
            self.render("login.html", error_msg=error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("username", json_encode(user))
        else:
            self.clear_cookie("user")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("uesr")
        self.redirect(self.get_argument("next", u"/"))



