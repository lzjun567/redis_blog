#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

import os
import os.path
import settings
from base import redis


def read_all():
    base_dir = settings.BASE_DIR
    project_dir = settings.PROJECT_DIR
    path = os.path.join(base_dir, project_dir).replace("\\", "/")
    category_dir = os.listdir(os.path.join(base_dir, project_dir).replace("\\", "/"))

    for category in category_dir:
        tag = os.path.join(path, category).replace("\\", "/")
        if os.path.isdir(tag):
            posts = [os.path.join(tag, name).replace("\\", "/") for name in os.listdir(tag)]
            for post in posts:
                if os.path.isfile(post):
                    create_time = os.path.getctime(post)
                    print post
                    redis.zadd('archives', create_time, post)
                    redis.hset('category', post, category)
                    if category in post:
                        redis.zadd('category.%s' % category, create_time, post)

    posts = redis.zrange('archives', 0, -1)
    for post in posts:
        with open(post, 'r') as p:
            lines = p.readlines()
            if len(lines) > 0:
                redis.hset(post, 'title', lines[0])
                redis.hset(post, 'create_at', os.path.getctime(post))
                uri = os.path.basename(
                    os.path.abspath(os.path.join(post, os.pardir).replace("\\", "/"))) + "/" + os.path.basename(post)
                redis.hset(post, 'uri', uri)
