import logging
import tornado
import tornado.template
import os
from tornado.options import define, options

import environment
import logconfig
import tomlpython

# Make filepaths relative to settings.
path = lambda root, *a: os.path.join(root, *a)
ROOT = os.path.dirname(os.path.abspath(__file__))

define("port", default=8888, help="run on the given port", type=int)
define("config", default=None, help="tornado config file")
define("debug", default=False, help="debug mode")


MEDIA_ROOT = path(ROOT, 'media')
TEMPLATE_ROOT = path(ROOT, 'templates')

#load config file
DEBUG_CONFIG_PATH = path(ROOT, "debug.config.toml")
PRODUCTION_CONFIG_PATH = path(ROOT, 'config.toml')
config = DEBUG_CONFIG_PATH if os.path.exists(DEBUG_CONFIG_PATH) else PRODUCTION_CONFIG_PATH
with open(config) as config_file:
    data = tomlpython.parse(config_file)
    for k in data.keys():
        v = data.get(k)
        vars()[k] = v
# Deployment Configuration


class DeploymentType:
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"
    SOLO = "SOLO"
    STAGING = "STAGING"
    dict = {
        SOLO: 1,
        PRODUCTION: 2,
        DEV: 3,
        STAGING: 4
    }


if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DeploymentType.SOLO

settings = dict()
settings['debug'] = DEPLOYMENT != DeploymentType.PRODUCTION or options.debug
settings['static_path'] = MEDIA_ROOT
settings['cookie_secret'] = "your-cookie-secret"
settings['xsrf_cookies'] = True
settings['template_loader'] = tornado.template.Loader(TEMPLATE_ROOT)
settings['login_url'] = "/auth/login/"

SYSLOG_TAG = "boilerplate"
SYSLOG_FACILITY = logging.handlers.SysLogHandler.LOG_LOCAL2

# See PEP 391 and logconfig for formatting help.  Each section of LOGGERS
# will get merged into the corresponding section of log_settings.py.
# Handlers and log levels are set up automatically based on LOG_LEVEL and DEBUG
# unless you set them here.  Messages will not propagate through a logger
# unless propagate: True is set.
LOGGERS = {
    'loggers': {
        'boilerplate': {},
    },
}

if settings['debug']:
    LOG_LEVEL = logging.DEBUG
else:
    LOG_LEVEL = logging.INFO
USE_SYSLOG = DEPLOYMENT != DeploymentType.SOLO

if options.config:
    tornado.options.parse_config_file(options.config)
