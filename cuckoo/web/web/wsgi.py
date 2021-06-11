# coding=utf-8
# Copyright (C) 2010-2013 Claudio Guarnieri.
# Copyright (C) 2014-2019 Cuckoo Foundation.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

"""
WSGI config for web project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

web项目的WSGI配置。
此模块包含Django的开发服务器使用的WSGI应用程序以及任何生产WSGI部署。它应该公开一个模块级变量
命名为``application``。Django的``runserver``和``runfcgi``命令通过“WSGI\u application”设置创建此应用程序。
通常这里有标准的Django WSGI应用程序，但是将整个Django WSGI应用程序替换为自定义应用程序可能是有意义的
后来它被委托给了Django一号。例如，您可以引入WSGI或者将Django应用程序与另一个应用程序相结合框架。

"""

import os
import sys

import cuckoo

from cuckoo.core.startup import ensure_tmpdir, init_console_logging
from cuckoo.misc import decide_cwd

if os.environ.get("CUCKOO_APP") == "web":
    decide_cwd(exists=True)

    os.chdir(os.path.join(cuckoo.__path__[0], "web"))
    sys.path.insert(0, ".")

    cuckoo.core.database.Database().connect()
    init_console_logging()
    ensure_tmpdir()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

    # This application object is used by any WSGI server configured to use
    # this file. This includes Django's development server, if the
    # WSGI_APPLICATION setting points here.
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    # Apply WSGI middleware here.
    # from helloworld.wsgi import HelloWorldApplication
    # application = HelloWorldApplication(application)
