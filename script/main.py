# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'

import os
import sys
import optparse
import subprocess
import os.path


PROJECT_PATH = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir)
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)
import cache


def main():
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)
    parser.add_option("-i", "--initial", dest="data",
                      action="store_true",
                      default=False,
                      help="initial project data save to redis")
    options, args = parser.parse_args()
    if options.data:
        cache.inital()


def call_command(command):
    process = subprocess.popen(command.split(' '),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    return process.communicate()


if __name__ == '__main__':
    main()