#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

import os.path
import redis
import settings
from models import Blog
import utils
from tornado.web import asynchronous

redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def inital():
    """
    inital project data to redis
    :return:
    """
    for path in get_files(settings.PROJECT_DIR, ".md"):
        # 文件创建时间
        # 有序结合保存所有文档，查看所有文章时，可以按照时间顺序查看
        create_time = os.path.getctime(path)
        redis.zadd('admin.blog.list', create_time, utils.encrypt(path))

        # 把文件的上级目录当作标签
        #有序set存放该标签下的文章，相当于文章按标签分类，用有序集合的原因是可以按时间顺序显示
        tag_name = os.path.basename(os.path.dirname(path))
        redis.zadd('blog.tag.%s' % tag_name, create_time, utils.encrypt(path))

        #set集合存放所有标签
        redis.sadd('blog.tag', tag_name)


def get_files(path, pattern):
    """
    获取path路径下所有pattern格式文件
    :param path:
    :param pattern:
    :return:
    """
    result = set()
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith(pattern):
                p = os.path.join(root, f).replace("\\", '/')
                result.add(p)
    return result


def cache(func):
    @asynchronous
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            handler = args[0]
            blog_id = handler.get_argument("blog_id", None)
            if not blog_id:
                blog_id = redis.zrange('blog.list', -1, -1)
                if blog_id:
                    blog_id = redis.zrange('blog.list', -1, -1)[0]
                else:
                    handler.write("请先在管理后台添加预发布的文章")
                    handler.finish()
                    return
        else:
            blog_id = args[1]
        blog = redis.hgetall(blog_id)
        if not blog:
            with open(utils.decrypt(blog_id), 'r') as p:
                lines = p.readlines() or ['']
                title = lines[0]
                create_at = int(os.path.getctime(utils.decrypt(blog_id)) or 1504724902)
                content = utils.md_parse(''.join(lines[2:-1]))
                redis.hset(blog_id, 'title', title)
                redis.hset(blog_id, 'create_at', create_at)
                redis.hset(blog_id, 'content', content)
        return func(*args, **kwargs)

    return wrapper


if __name__ == "__main__":
    inital()
