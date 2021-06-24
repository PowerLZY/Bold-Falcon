---
sort: 2
---
# 使用
.. Usage chapter frontpage

Usage
=====

This chapter explains how to use Cuckoo.

.. toctree::

    start
    submit
    web
    api
    dist
    packages
    results
    clean
    utilities

## 启动毕方云沙箱
===============
Starting Cuckoo
===============

To start Cuckoo use the command::

    $ python cuckoo.py

Make sure to run it inside Cuckoo's root directory.

You will get an output similar to this::

      eeee e   e eeee e   e  eeeee eeeee
      8  8 8   8 8  8 8   8  8  88 8  88
      8e   8e  8 8e   8eee8e 8   8 8   8
      88   88  8 88   88   8 8   8 8   8
      88e8 88ee8 88e8 88   8 8eee8 8eee8

     Cuckoo Sandbox 1.2
     www.cuckoosandbox.org
     Copyright (c) 2010-2015

     Checking for updates...
     Good! You have the latest version available.

    2013-04-07 15:57:17,459 [lib.cuckoo.core.scheduler] INFO: Using "virtualbox" machine manager
    2013-04-07 15:57:17,861 [lib.cuckoo.core.scheduler] INFO: Loaded 1 machine/s
    2013-04-07 15:57:17,862 [lib.cuckoo.core.scheduler] INFO: Waiting for analysis tasks...

Note that Cuckoo checks for updates on a remote API located at *api.cuckoosandbox.org*.
You can avoid this by disabling the ``version_check`` option in the configuration file.

Now Cuckoo is ready to run and it's waiting for submissions.

``cuckoo.py`` accepts some command line options as shown by the help::

    usage: cuckoo.py [-h] [-q] [-d] [-v] [-a] [-t] [-m MAX_ANALYSIS_COUNT]
                     [-u USER] [--clean]

    optional arguments:
      -h, --help            show this help message and exit
      -q, --quiet           Display only error messages
      -d, --debug           Display debug messages
      -v, --version         show program's version number and exit
      -a, --artwork         Show artwork
      -t, --test            Test startup
      -m MAX_ANALYSIS_COUNT, --max-analysis-count MAX_ANALYSIS_COUNT
                            Maximum number of analyses
      -u USER, --user USER  Drop user privileges to this user
      --clean               Remove all tasks and samples and their associated data


Most importantly ``--debug`` and ``--quiet`` respectively increase and decrease the logging
verbosity.

## 毕方云沙箱工作目录

## 提交分析
==================
Submit an Analysis
==================

    * :ref:`submitpy`
    * :ref:`apipy`
    * :ref:`distpy`
    * :ref:`python`

.. _submitpy:

Submission Utility
==================

The easiest way to submit an analysis is to use the provided *submit.py*
command-line utility. It currently has the following options available::

    usage: submit.py [-h] [-d] [--remote REMOTE] [--url] [--package PACKAGE]
                     [--custom CUSTOM] [--owner OWNER] [--timeout TIMEOUT]
                     [-o OPTIONS] [--priority PRIORITY] [--machine MACHINE]
                     [--platform PLATFORM] [--memory] [--enforce-timeout]
                     [--clock CLOCK] [--tags TAGS] [--max MAX] [--pattern PATTERN]
                     [--shuffle] [--unique] [--quiet]
                     target

    positional arguments:
      target                URL, path to the file or folder to analyze

    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Enable debug logging
      --remote REMOTE       Specify IP:port to a Cuckoo API server to submit
                            remotely
      --url                 Specify whether the target is an URL
      --package PACKAGE     Specify an analysis package
      --custom CUSTOM       Specify any custom value
      --owner OWNER         Specify the task owner
      --timeout TIMEOUT     Specify an analysis timeout
      -o OPTIONS, --options OPTIONS
                            Specify options for the analysis package (e.g.
                            "name=value,name2=value2")
      --priority PRIORITY   Specify a priority for the analysis represented by an
                            integer
      --machine MACHINE     Specify the identifier of a machine you want to use
      --platform PLATFORM   Specify the operating system platform you want to use
                            (windows/darwin/linux)
      --memory              Enable to take a memory dump of the analysis machine
      --enforce-timeout     Enable to force the analysis to run for the full
                            timeout period
      --clock CLOCK         Set virtual machine clock
      --tags TAGS           Specify tags identifier of a machine you want to use
      --max MAX             Maximum samples to add in a row
      --pattern PATTERN     Pattern of files to submit
      --shuffle             Shuffle samples before submitting them
      --unique              Only submit new samples, ignore duplicates
      --quiet               Only print text on failure

If you specify a directory as path, all the files contained in it will be
submitted for analysis.

The concept of analysis packages will be dealt later in this documentation (at
:doc:`packages`). Following are some usage examples:

*Example*: submit a local binary::

    $ ./utils/submit.py /path/to/binary

*Example*: submit an URL::

    $ ./utils/submit.py --url http://www.example.com

*Example*: submit a local binary and specify an higher priority::

    $ ./utils/submit.py --priority 5 /path/to/binary

*Example*: submit a local binary and specify a custom analysis timeout of
60 seconds::

    $ ./utils/submit.py --timeout 60 /path/to/binary

*Example*: submit a local binary and specify a custom analysis package::

    $ ./utils/submit.py --package <name of package> /path/to/binary

*Example*: submit a local binary and specify a custom analysis package and
some options (in this case a command line argument for the malware)::

    $ ./utils/submit.py --package exe --options arguments=--dosomething /path/to/binary.exe

*Example*: submit a local binary to be run on virtual machine *cuckoo1*::

    $ ./utils/submit.py --machine cuckoo1 /path/to/binary

*Example*: submit a local binary to be run on a Windows machine::

    $ ./utils/submit.py --platform windows /path/to/binary

*Example*: submit a local binary and take a full memory dump of the analysis machine::

    $ ./utils/submit.py --memory /path/to/binary

*Example*: submit a local binary and force the analysis to be executed for the full timeout (disregarding the internal mechanism that Cuckoo uses to decide when to terminate the analysis)::

    $ ./utils/submit.py --enforce-timeout /path/to/binary

*Example*: submit a local binary and set virtual machine clock. Format is %m-%d-%Y %H:%M:%S. If not specified, the current time is used. For example if we want run a sample the 24 january 2001 at 14:41:20::

    $ ./utils/submit.py --clock "01-24-2001 14:41:20" /path/to/binary

*Example*: submit a sample for Volatility analysis (to reduce side effects of the cuckoo hooking, switch it off with *options free=True*)::

    $ ./utils/submit.py --memory --options free=True /path/to/binary

.. _apipy:

API
===

Detailed usage of the REST API interface is described in :doc:`api`.

.. _distpy:

Distributed Cuckoo
==================

Detailed usage of the Distributed Cuckoo API interface is described in
:doc:`dist`.

.. _python:

Python Functions
================

In order to keep track of submissions, samples and overall execution, Cuckoo
uses a popular Python ORM called `SQLAlchemy`_ that allows you to make the sandbox
use SQLite, MySQL, PostgreSQL and several other SQL database systems.

Cuckoo is designed to be easily integrated in larger solutions and to be fully
automated. In order to automate analysis submission we suggest to use the REST
API interface described in :doc:`api`, but in case you want to write your
own Python submission script, you can also use the ``add_path()`` and ``add_url()`` functions.

.. function:: add_path(file_path[, timeout=0[, package=None[, options=None[, priority=1[, custom=None[, owner=""[, machine=None[, platform=None[, memory=False[, enforce_timeout=False], clock=None[]]]]]]]]]])

    Add a local file to the list of pending analysis tasks. Returns the ID of the newly generated task.

    :param file_path: path to the file to submit
    :type file_path: string
    :param timeout: maximum amount of seconds to run the analysis for
    :type timeout: integer
    :param package: analysis package you want to use for the specified file
    :type package: string or None
    :param options: list of options to be passed to the analysis package (in the format ``key=value,key=value``)
    :type options: string or None
    :param priority: numeric representation of the priority to assign to the specified file (1 being low, 2 medium, 3 high)
    :type priority: integer
    :param custom: custom value to be passed over and possibly reused at processing or reporting
    :type custom: string or None
    :param owner: task owner
    :type owner: string or None
    :param machine: Cuckoo identifier of the virtual machine you want to use, if none is specified one will be selected automatically
    :type machine: string or None
    :param platform: operating system platform you want to run the analysis one (currently only Windows)
    :type platform: string or None
    :param memory: set to ``True`` to generate a full memory dump of the analysis machine
    :type memory: True or False
    :param enforce_timeout: set to ``True`` to force the execution for the full timeout
    :type enforce_timeout: True or False
    :param clock: provide a custom clock time to set in the analysis machine
    :type clock: string or None
    :rtype: integer

    Example usage:

    .. code-block:: python
        :linenos:

        >>> from lib.cuckoo.core.database import Database
        >>> db = Database()
        >>> db.add_path("/tmp/malware.exe")
        1
        >>>

.. function:: add_url(url[, timeout=0[, package=None[, options=None[, priority=1[, custom=None[, owner=""[, machine=None[, platform=None[, memory=False[, enforce_timeout=False], clock=None[]]]]]]]]]])

    Add a local file to the list of pending analysis tasks. Returns the ID of the newly generated task.

    :param url: URL to analyze
    :type url: string
    :param timeout: maximum amount of seconds to run the analysis for
    :type timeout: integer
    :param package: analysis package you want to use for the specified URL
    :type package: string or None
    :param options: list of options to be passed to the analysis package (in the format ``key=value,key=value``)
    :type options: string or None
    :param priority: numeric representation of the priority to assign to the specified URL (1 being low, 2 medium, 3 high)
    :type priority: integer
    :param custom: custom value to be passed over and possibly reused at processing or reporting
    :type custom: string or None
    :param owner: task owner
    :type owner: string or None
    :param machine: Cuckoo identifier of the virtual machine you want to use, if none is specified one will be selected automatically
    :type machine: string or None
    :param platform: operating system platform you want to run the analysis one (currently only Windows)
    :type platform: string or None
    :param memory: set to ``True`` to generate a full memory dump of the analysis machine
    :type memory: True or False
    :param enforce_timeout: set to ``True`` to force the execution for the full timeout
    :type enforce_timeout: True or False
    :param clock: provide a custom clock time to set in the analysis machine
    :type clock: string or None
    :rtype: integer

Example Usage:

.. code-block:: python
    :linenos:

    >>> from lib.cuckoo.core.database import Database
    >>> db = Database()
    >>> db.add_url("http://www.cuckoosandbox.org")
    2
    >>>

.. _`SQLAlchemy`: http://www.sqlalchemy.org

## Web接口
=============
Web interface
=============

Cuckoo provides a full-fledged web interface in the form of a Django application.
This interface will allow you to submit files, browse through the reports as well
as search across all the analysis results.

Configuration
=============

The web interface pulls data from a Mongo database, so having the Mongo reporting
module enabled in ``reporting.conf`` is mandatory for this interface.
If that's not the case, the application won't start and it will raise an exception.

The interface can be configured by editing ``local_settings.py`` under ``web/web/``::

    # If you want to customize your cuckoo path set it here.
    # CUCKOO_PATH = "/where/cuckoo/is/placed/"

    # Maximum upload size.
    MAX_UPLOAD_SIZE = 26214400

    # Override default secret key stored in secret_key.py
    # Make this unique, and don't share it with anybody.
    # SECRET_KEY = "YOUR_RANDOM_KEY"

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = "en-us"

    ADMINS = (
        # ("Your Name", "your_email@example.com"),
    )

    MANAGERS = ADMINS

    # Allow verbose debug error message in case of application fault.
    # It's strongly suggested to set it to False if you are serving the
    # web application from a web server front-end (i.e. Apache).
    DEBUG = True

    # A list of strings representing the host/domain names that this Django site
    # can serve.
    # Values in this list can be fully qualified names (e.g. 'www.example.com').
    # When DEBUG is True or when running tests, host validation is disabled; any
    # host will be accepted. Thus it's usually only necessary to set it in production.
    ALLOWED_HOSTS = ["*"]

In production deploys it is suggested to disable verbose error reporting setting
``DEBUG`` to False, it could lead to an information disclosure vulnerability. It
is also suggested to set at least one administrator email address in the
``ADMIN`` variable to enable error notification by mail.

In some cases, if you are submitting large files, it is suggested to increase
the maximum file size limit editing ``MAX_UPLOAD_SIZE``.

Usage
=====

In order to start the web interface, you can simply run the following command
from the ``web/`` directory::

    $ python manage.py runserver

If you want to configure the web interface as listening for any IP on a
specified port, you can start it with the following command (replace PORT
with the desired port number)::

    $ python manage.py runserver 0.0.0.0:PORT

You can serve Cuckoo's web interface using WSGI interface with common web servers:
Apache, Nginx, Unicorn and so on.
Please refer both to the documentation of the web server of your choice as well as `Django documentation`_.

.. _`Django documentation`: https://docs.djangoproject.com/

## REST API
========
REST API
========

As mentioned in :doc:`submit`, Cuckoo provides a simple and lightweight REST
API server implemented in `Flask`_, therefore in order to make the service
work you'll need it installed.

On Debian/Ubuntu with pip::

    $ pip install flask

.. _`Flask`: http://flask.pocoo.org/

Starting the API server
=======================

In order to start the API server you can simply do::

    $ ./utils/api.py

By default it will bind the service on **localhost:8090**. If you want to change
those values, you can for example do this::

    $ ./utils/api.py --host 0.0.0.0 --port 1337

Web deployment
--------------

While the default method of starting the API server works fine for many cases,
some users may wish to deploy the server in a robust manner. This can be done
by exposing the API as a WSGI application through a web server. This section shows
a simple example of deploying the API via `uWSGI`_ and `Nginx`_. These
instructions are written with Ubuntu GNU/Linux in mind, but may be adapted for
other platforms.

This solution requires uWSGI, the uWSGI Python plugin, and Nginx. All are
available as packages::

    $ sudo apt-get install uwsgi uwsgi-plugin-python nginx

uWSGI setup
^^^^^^^^^^^
First, use uWSGI to run the API server as an application.

To begin, create a uWSGI configuration file at ``/etc/uwsgi/apps-available/cuckoo-api.ini``::

    [uwsgi]
    plugins = python
    chdir = /home/cuckoo/cuckoo
    file = utils/api.py
    uid = cuckoo
    gid = cuckoo

This configuration inherits a number of settings from the distribution's
default uWSGI configuration, loading ``api.py`` from the Cuckoo installation
directory. In this example we installed Cuckoo in /home/cuckoo/cuckoo, if Cuckoo
is installed in a different path, adjust the configuration (the *chdir* setting,
and perhaps the *uid* and *gid* settings) accordingly.

Enable the app configuration and start the server::

    $ sudo ln -s /etc/uwsgi/apps-available/cuckoo-api.ini /etc/uwsgi/apps-enabled/
    $ sudo service uwsgi start cuckoo-api    # or reload, if already running

.. note::

   Logs for the application may be found in the standard directory for distribution
   app instances, i.e.:

   ``/var/log/uwsgi/app/cuckoo-api.log``

   The UNIX socket is created in a conventional location as well:

   ``/run/uwsgi/app/cuckoo-api/socket``

Nginx setup
^^^^^^^^^^^

With the API server running in uWSGI, Nginx can now be set up to run as a web
server/reverse proxy, backending HTTP requests to it.

To begin, create a Nginx configuration file at ``/etc/nginx/sites-available/cuckoo-api``::

    upstream _uwsgi_cuckoo_api {
        server unix:/run/uwsgi/app/cuckoo-api/socket;
    }

    # HTTP server
    #
    server {
        listen 8090;
        listen [::]:8090 ipv6only=on;

        # REST API app
        location / {
            uwsgi_pass  _uwsgi_cuckoo_api;
            include     uwsgi_params;
        }
    }

Make sure that Nginx can connect to the uWSGI socket by placing its user in the
**cuckoo** group::

    $ sudo adduser www-data cuckoo

Enable the server configuration and start the server::

    $ sudo ln -s /etc/nginx/sites-available/cuckoo-api /etc/nginx/sites-enabled/
    $ sudo service nginx start    # or reload, if already running

At this point, the API server should be available at port **8090** on the server.
Various configurations may be applied to extend this configuration, such as to
tune server performance, add authentication, or to secure communications using
HTTPS.

.. _`uWSGI`: http://uwsgi-docs.readthedocs.org/en/latest/
.. _`Nginx`: http://nginx.org/

Resources
=========

Following is a list of currently available resources and a brief description of
each one. For details click on the resource name.

+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| Resource                          | Description                                                                                                      |
+===================================+==================================================================================================================+
| ``POST`` :ref:`tasks_create_file` | Adds a file to the list of pending tasks to be processed and analyzed.                                           |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``POST`` :ref:`tasks_create_url`  | Adds an URL to the list of pending tasks to be processed and analyzed.                                           |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`tasks_list`         | Returns the list of tasks stored in the internal Cuckoo database.                                                |
|                                   | You can optionally specify a limit of entries to return.                                                         |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`tasks_view`         | Returns the details on the task assigned to the specified ID.                                                    |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`tasks_reschedule`   | Reschedule a task assigned to the specified ID.                                                                  |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`tasks_delete`       | Removes the given task from the database and deletes the results.                                                |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`tasks_report`       | Returns the report generated out of the analysis of the task associated with the specified ID.                   |
|                                   | You can optionally specify which report format to return, if none is specified the JSON report will be returned. |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`tasks_shots`        | Retrieves one or all screenshots associated with a given analysis task ID.                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`tasks_rereport`     | Re-run reporting for task associated with a given analysis task ID.                                              |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`memory_list`        | Returns a list of memory dump files associated with a given analysis task ID.                                    |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`memory_get`         | Retrieves one memory dump file associated with a given analysis task ID.                                         |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`files_view`         | Search the analyzed binaries by MD5 hash, SHA256 hash or internal ID (referenced by the tasks details).          |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`files_get`          | Returns the content of the binary with the specified SHA256 hash.                                                |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`pcap_get`           | Returns the content of the PCAP associated with the given task.                                                  |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`machines_list`      | Returns the list of analysis machines available to Cuckoo.                                                       |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`machines_view`      | Returns details on the analysis machine associated with the specified name.                                      |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`cuckoo_status`      | Returns the basic cuckoo status, including version and tasks overview.                                           |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``GET`` :ref:`vpn_status`         | Returns VPN status.                                                                                              |
+-----------------------------------+------------------------------------------------------------------------------------------------------------------+

.. highlight:: javascript

.. _tasks_create_file:

/tasks/create/file
------------------

    **POST /tasks/create/file**

        Adds a file to the list of pending tasks. Returns the ID of the newly created task.

        **Example request**::

            curl -F file=@/path/to/file http://localhost:8090/tasks/create/file

        **Example request using Python**::

            import requests
            import json

            REST_URL = "http://localhost:8090/tasks/create/file"
            SAMPLE_FILE = "/path/to/malwr.exe"

            with open(SAMPLE_FILE, "rb") as sample:
                multipart_file = {"file": ("temp_file_name", sample)}
                request = requests.post(REST_URL, files=multipart_file)

            # Add your code to error checking for request.status_code.

            json_decoder = json.JSONDecoder()
            task_id = json_decoder.decode(request.text)["task_id"]

            # Add your code for error checking if task_id is None.

        **Example response**::

            {
                "task_id" : 1
            }

        **Form parameters**:
            * ``file`` *(required)* - sample file (multipart encoded file content)
            * ``package`` *(optional)* - analysis package to be used for the analysis
            * ``timeout`` *(optional)* *(int)* - analysis timeout (in seconds)
            * ``priority`` *(optional)* *(int)* - priority to assign to the task (1-3)
            * ``options`` *(optional)* - options to pass to the analysis package
            * ``machine`` *(optional)* - ID of the analysis machine to use for the analysis
            * ``platform`` *(optional)* - name of the platform to select the analysis machine from (e.g. "windows")
            * ``tags`` *(optional)* - define machine to start by tags. Platform must be set to use that. Tags are comma separated
            * ``custom`` *(optional)* - custom string to pass over the analysis and the processing/reporting modules
            * ``owner`` *(optional)* - task owner in case multiple users can submit files to the same cuckoo instance
            * ``memory`` *(optional)* - enable the creation of a full memory dump of the analysis machine
            * ``enforce_timeout`` *(optional)* - enable to enforce the execution for the full timeout value
            * ``clock`` *(optional)* - set virtual machine clock (format %m-%d-%Y %H:%M:%S)

        **Status codes**:
            * ``200`` - no error

.. _tasks_create_url:

/tasks/create/url
-----------------

    **POST /tasks/create/url**

        Adds a file to the list of pending tasks. Returns the ID of the newly created task.

        **Example request**::

            curl -F url="http://www.malicious.site" http://localhost:8090/tasks/create/url

        **Example request using Python**::

            import requests
            import json

            REST_URL = "http://localhost:8090/tasks/create/url"
            SAMPLE_URL = "http://example.org/malwr.exe"

            multipart_url = {"url": ("", SAMPLE_URL)}
            request = requests.post(REST_URL, files=multipart_url)

            # Add your code to error checking for request.status_code.

            json_decoder = json.JSONDecoder()
            task_id = json_decoder.decode(request.text)["task_id"]

            # Add your code toerror checking if task_id is None.

        **Example response**::

            {
                "task_id" : 1
            }

        **Form parameters**:
            * ``url`` *(required)* - URL to analyze (multipart encoded content)
            * ``package`` *(optional)* - analysis package to be used for the analysis
            * ``timeout`` *(optional)* *(int)* - analysis timeout (in seconds)
            * ``priority`` *(optional)* *(int)* - priority to assign to the task (1-3)
            * ``options`` *(optional)* - options to pass to the analysis package
            * ``machine`` *(optional)* - ID of the analysis machine to use for the analysis
            * ``platform`` *(optional)* - name of the platform to select the analysis machine from (e.g. "windows")
            * ``tags`` *(optional)* - define machine to start by tags. Platform must be set to use that. Tags are comma separated
            * ``custom`` *(optional)* - custom string to pass over the analysis and the processing/reporting modules
            * ``owner`` *(optional)* - task owner in case multiple users can submit files to the same cuckoo instance
            * ``memory`` *(optional)* - enable the creation of a full memory dump of the analysis machine
            * ``enforce_timeout`` *(optional)* - enable to enforce the execution for the full timeout value
            * ``clock`` *(optional)* - set virtual machine clock (format %m-%d-%Y %H:%M:%S)

        **Status codes**:
            * ``200`` - no error

.. _tasks_list:

/tasks/list
-----------

    **GET /tasks/list/** *(int: limit)* **/** *(int: offset)*

        Returns list of tasks.

        **Example request**::

            curl http://localhost:8090/tasks/list

        **Example response**::

            {
                "tasks": [
                    {
                        "category": "url",
                        "machine": null,
                        "errors": [],
                        "target": "http://www.malicious.site",
                        "package": null,
                        "sample_id": null,
                        "guest": {},
                        "custom": null,
                        "owner": "",
                        "priority": 1,
                        "platform": null,
                        "options": null,
                        "status": "pending",
                        "enforce_timeout": false,
                        "timeout": 0,
                        "memory": false,
                        "tags": []
                        "id": 1,
                        "added_on": "2012-12-19 14:18:25",
                        "completed_on": null
                    },
                    {
                        "category": "file",
                        "machine": null,
                        "errors": [],
                        "target": "/tmp/malware.exe",
                        "package": null,
                        "sample_id": 1,
                        "guest": {},
                        "custom": null,
                        "owner": "",
                        "priority": 1,
                        "platform": null,
                        "options": null,
                        "status": "pending",
                        "enforce_timeout": false,
                        "timeout": 0,
                        "memory": false,
                        "tags": [
                                    "32bit",
                                    "acrobat_6",
                                ],
                        "id": 2,
                        "added_on": "2012-12-19 14:18:25",
                        "completed_on": null
                    }
                ]
            }

        **Parameters**:
            * ``limit`` *(optional)* *(int)* - maximum number of returned tasks
            * ``offset`` *(optional)* *(int)* - data offset

        **Status codes**:
            * ``200`` - no error

.. _tasks_view:

/tasks/view
-----------

    **GET /tasks/view/** *(int: id)*

        Returns details on the task associated with the specified ID.

        **Example request**::

            curl http://localhost:8090/tasks/view/1

        **Example response**::

            {
                "task": {
                    "category": "url",
                    "machine": null,
                    "errors": [],
                    "target": "http://www.malicious.site",
                    "package": null,
                    "sample_id": null,
                    "guest": {},
                    "custom": null,
                    "owner": "",
                    "priority": 1,
                    "platform": null,
                    "options": null,
                    "status": "pending",
                    "enforce_timeout": false,
                    "timeout": 0,
                    "memory": false,
                    "tags": [
                                "32bit",
                                "acrobat_6",
                            ],
                    "id": 1,
                    "added_on": "2012-12-19 14:18:25",
                    "completed_on": null
                }
            }

        Note: possible value for key ``status``:
            * ``pending``
            * ``running``
            * ``completed``
            * ``reported``

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to lookup

        **Status codes**:
            * ``200`` - no error
            * ``404`` - task not found

.. _tasks_reschedule:

/tasks/reschedule
-----------------

    **GET /tasks/reschedule/** *(int: id)* **/** *(int: priority)*

        Reschedule a task with the specified ID and priority (default priority
        is 1).

        **Example request**::

            curl http://localhost:8090/tasks/reschedule/1

        **Example response**::

            {
                "status": "OK"
            }

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to reschedule
            * ``priority`` *(optional)* *(int)* - Task priority

        **Status codes**:
            * ``200`` - no error
            * ``404`` - task not found

.. _tasks_delete:

/tasks/delete
-------------

    **GET /tasks/delete/** *(int: id)*

        Removes the given task from the database and deletes the results.

        **Example request**::

            curl http://localhost:8090/tasks/delete/1

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to delete

        **Status codes**:
            * ``200`` - no error
            * ``404`` - task not found
            * ``500`` - unable to delete the task

.. _tasks_report:

/tasks/report
-------------

    **GET /tasks/report/** *(int: id)* **/** *(str: format)*

        Returns the report associated with the specified task ID.

        **Example request**::

            curl http://localhost:8090/tasks/report/1

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to get the report for
            * ``format`` *(optional)* - format of the report to retrieve [json/html/all/dropped/package_files]. If none is specified the JSON report will be returned. ``all`` returns all the result files as tar.bz2, ``dropped`` the dropped files as tar.bz2, ``package_files`` files uploaded to host by analysis packages.

        **Status codes**:
            * ``200`` - no error
            * ``400`` - invalid report format
            * ``404`` - report not found

.. _tasks_shots:

/tasks/screenshots
------------------

    **GET /tasks/screenshots/** *(int: id)* **/** *(str: number)*

        Returns one or all screenshots associated with the specified task ID.

        **Example request**::

            wget http://localhost:8090/tasks/screenshots/1

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to get the report for
            * ``screenshot`` *(optional)* - numerical identifier of a single screenshot (e.g. 0001, 0002)

        **Status codes**:
            * ``404`` - file or folder not found

.. _tasks_rereport:

/tasks/rereport
---------------

    **GET /tasks/rereport/** *(int: id)*

        Re-run reporting for task associated with the specified task ID.

        **Example request**::

            curl http://localhost:8090/tasks/rereport/1

        **Example response**::

            {
                "success": true
            }

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to re-run report

        **Status codes**:
            * ``200`` - no error
            * ``404`` - task not found

.. _memory_list:

/memory/list
------------------

    **GET /memory/list/** *(int: id)*

        Returns a list of memory dump files or one memory dump file associated with the specified task ID.

        **Example request**::

            wget http://localhost:8090/memory/list/1

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to get the report for

        **Status codes**:
            * ``404`` - file or folder not found

.. _memory_get:

/memory/get
------------------

    **GET /memory/get/** *(int: id)* **/** *(str: number)*

        Returns one memory dump file associated with the specified task ID.

        **Example request**::

            wget http://localhost:8090/memory/get/1/1908

        **Parameters**:
            * ``id`` *(required)* *(int)* - ID of the task to get the report for
            * ``pid`` *(required)* - numerical identifier (pid) of a single memory dump file (e.g. 205, 1908)

        **Status codes**:
            * ``404`` - file or folder not found

.. _files_view:

/files/view
-----------

    **GET /files/view/md5/** *(str: md5)*

    **GET /files/view/sha256/** *(str: sha256)*

    **GET /files/view/id/** *(int: id)*

        Returns details on the file matching either the specified MD5 hash, SHA256 hash or ID.

        **Example request**::

            curl http://localhost:8090/files/view/id/1

        **Example response**::

            {
                "sample": {
                    "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                    "file_type": "empty",
                    "file_size": 0,
                    "crc32": "00000000",
                    "ssdeep": "3::",
                    "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                    "sha512": "cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e",
                    "id": 1,
                    "md5": "d41d8cd98f00b204e9800998ecf8427e"
                }
            }

        **Parameters**:
            * ``md5`` *(optional)* - MD5 hash of the file to lookup
            * ``sha256`` *(optional)* - SHA256 hash of the file to lookup
            * ``id`` *(optional)* *(int)* - ID of the file to lookup

        **Status codes**:
            * ``200`` - no error
            * ``400`` - invalid lookup term
            * ``404`` - file not found

.. _files_get:

/files/get
----------

    **GET /files/get/** *(str: sha256)*

         Returns the binary content of the file matching the specified SHA256 hash.

        **Example request**::

            curl http://localhost:8090/files/get/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 > sample.exe

        **Status codes**:
            * ``200`` - no error
            * ``404`` - file not found

.. _pcap_get:

/pcap/get
---------

    **GET /pcap/get/** *(int: task)*

        Returns the content of the PCAP associated with the given task.

        **Example request**::

            curl http://localhost:8090/pcap/get/1 > dump.pcap

        **Status codes**:
            * ``200`` - no error
            * ``404`` - file not found


.. _machines_list:

/machines/list
--------------

    **GET /machines/list**

        Returns a list with details on the analysis machines available to Cuckoo.

        **Example request**::

            curl http://localhost:8090/machines/list

        **Example response**::

            {
                "machines": [
                    {
                        "status": null,
                        "locked": false,
                        "name": "cuckoo1",
                        "resultserver_ip": "192.168.56.1",
                        "ip": "192.168.56.101",
                        "tags": [
                                    "32bit",
                                    "acrobat_6",
                                ],
                        "label": "cuckoo1",
                        "locked_changed_on": null,
                        "platform": "windows",
                        "snapshot": null,
                        "interface": null,
                        "status_changed_on": null,
                        "id": 1,
                        "resultserver_port": "2042"
                    }
                ]
            }

        **Status codes**:
            * ``200`` - no error

.. _machines_view:

/machines/view
--------------

    **GET /machines/view/** *(str: name)*

        Returns details on the analysis machine associated with the given name.

        **Example request**::

            curl http://localhost:8090/machines/view/cuckoo1

        **Example response**::

            {
                "machine": {
                    "status": null,
                    "locked": false,
                    "name": "cuckoo1",
                    "resultserver_ip": "192.168.56.1",
                    "ip": "192.168.56.101",
                    "tags": [
                                "32bit",
                                "acrobat_6",
                            ],
                    "label": "cuckoo1",
                    "locked_changed_on": null,
                    "platform": "windows",
                    "snapshot": null,
                    "interface": null,
                    "status_changed_on": null,
                    "id": 1,
                    "resultserver_port": "2042"
                }
            }

        **Status codes**:
            * ``200`` - no error
            * ``404`` - machine not found

.. _cuckoo_status:

/cuckoo/status
--------------

    **GET /cuckoo/status/**

        Returns status of the cuckoo server. In version 1.3 the diskspace
        entry was added. The diskspace entry shows the used, free, and total
        diskspace at the disk where the respective directories can be found.
        The diskspace entry allows monitoring of a Cuckoo node through the
        Cuckoo API. Note that each directory is checked separately as one
        may create a symlink for $CUCKOO/storage/analyses to a separate
        harddisk, but keep $CUCKOO/storage/binaries as-is. (This feature is
        only available under Unix!)

        In version 1.3 the cpuload entry was also added - the cpuload entry
        shows the CPU load for the past minute, the past 5 minutes, and the
        past 15 minutes, respectively. (This feature is only available under
        Unix!)

        **Diskspace directories**:
            * ``analyses`` - $CUCKOO/storage/analyses/
            * ``binaries`` - $CUCKOO/storage/binaries/
            * ``temporary`` - ``tmppath`` as specified in ``conf/cuckoo.conf``

        **Example request**::

            curl http://localhost:8090/cuckoo/status

        **Example response**::

            {
                "tasks": {
                    "reported": 165,
                    "running": 2,
                    "total": 167,
                    "completed": 0,
                    "pending": 0
                },
                "diskspace": {
                    "analyses": {
                        "total": 491271233536,
                        "free": 71403470848,
                        "used": 419867762688
                    },
                    "binaries": {
                        "total": 491271233536,
                        "free": 71403470848,
                        "used": 419867762688
                    },
                    "temporary": {
                        "total": 491271233536,
                        "free": 71403470848,
                        "used": 419867762688
                    }
                },
                "version": "1.0",
                "protocol_version": 1,
                "hostname": "Patient0",
                "machines": {
                    "available": 4,
                    "total": 5
                }
            }

        **Status codes**:
            * ``200`` - no error
            * ``404`` - machine not found

.. _vpn_status:

/vpn/status
-----------

    **GET /vpn/status**

        Returns VPN status.

        **Example request**::

            curl http://localhost:8090/vpn/status

        **Status codes**:
            * ``200`` - show status
            * ``500`` - not available

## 分布式
==================
Distributed Cuckoo
==================

As mentioned in :doc:`submit`, Cuckoo provides a REST API for Distributed
Cuckoo usage. The distributed script allows one to setup a single REST API
point to which samples and URLs can be submitted which will then, in turn, be
submitted to one of the configured Cuckoo nodes.

A typical setup thus includes a machine on which the distributed script is run
and one or more machines running an instance of the Cuckoo daemon
(``./cuckoo.py``) and the :doc:`Cuckoo REST API <api>`.

A few notes;

* Using the distributed script makes more sense when running at least two
  cuckoo nodes.
* The distributed script can be run on a machine that also runs a Cuckoo
  daemon and REST API, however, make sure it has enough disk space if the
  intention is to submit a lot of samples.

Dependencies
============

The distributed script uses a few Python libraries which can be installed
through the following command (on Debian/Ubuntu)::

    $ sudo pip install flask flask-sqlalchemy requests

Starting the Distributed REST API
=================================

The Distributed REST API requires a few commandline options in order to run.
Following is a listing of all available commandline options::

    $ ./distributed/app.py -h

    usage: app.py [-h] [-s SETTINGS] [-v] [host] [port]

    positional arguments:
        host                  Host to listen on.
        port                  Port to listen on.

    optional arguments:
        -h, --help            show this help message and exit
        -s SETTINGS, --settings SETTINGS
                              Settings file.
        -v, --verbose         Enable verbose logging.

The various configuration options are described in the configuration file, but following we have more in-depth
descriptions as well.

Report Formats
--------------

The reporting formats denote which reports you'd like to retrieve later on.
Note that all task-related data will be removed from the Cuckoo nodes once the
related reports have been fetches so that the machines are not running out of
disk space. This does, however, force you to specify all the report formats
that you're interested in, because otherwise that information will be lost.

Reporting formats include, but are not limited to and may also include your
own reporting formats, ``json``, ``html``, etc.

Samples Directory
-----------------

The samples directory denotes the directory where the submitted samples will
be stored temporarily, until they're passed on to a Cuckoo node and processed.

Reports Directory
-----------------

Much like the ``Samples Directory`` the Reports Directory defines the
directory where reports will be stored until they're fetched and deleted from
the Distributed REST API.

RESTful resources
=================

Following are all RESTful resources. Also make sure to check out the
:ref:`quick-usage` section which documents the most commonly used commands.

+-----------------------------------+---------------------------------------------------------------+
| Resource                          | Description                                                   |
+===================================+===============================================================+
| ``GET`` :ref:`node_root_get`      | Get a list of all enabled Cuckoo nodes.                       |
+-----------------------------------+---------------------------------------------------------------+
| ``POST`` :ref:`node_root_post`    | Register a new Cuckoo node.                                   |
+-----------------------------------+---------------------------------------------------------------+
| ``GET`` :ref:`node_get`           | Get basic information about a node.                           |
+-----------------------------------+---------------------------------------------------------------+
| ``PUT`` :ref:`node_put`           | Update basic information of a node.                           |
+-----------------------------------+---------------------------------------------------------------+
| ``DELETE`` :ref:`node_delete`     | Disable (not completely remove!) a node.                      |
+-----------------------------------+---------------------------------------------------------------+
| ``GET`` :ref:`task_root_get`      | Get a list of all (or a part) of the tasks in the database.   |
+-----------------------------------+---------------------------------------------------------------+
| ``POST`` :ref:`task_root_post`    | Create a new analysis task.                                   |
+-----------------------------------+---------------------------------------------------------------+
| ``GET`` :ref:`task_get`           | Get basic information about a task.                           |
+-----------------------------------+---------------------------------------------------------------+
| ``DELETE`` :ref:`task_delete`     | Delete all associated information of a task.                  |
+-----------------------------------+---------------------------------------------------------------+
| ``GET`` :ref:`report_get`         + Fetch an analysis report.                                     |
+-----------------------------------+---------------------------------------------------------------+

.. _node_root_get:

GET /api/node
-------------

Returns all enabled nodes. For each node its associated name, API url, and
machines are returned::

    $ curl http://localhost:9003/api/node
    {
        "success": true,
        "nodes": {
            "localhost": {
                "machines": [
                    {
                        "name": "cuckoo1",
                        "platform": "windows",
                        "tags": []
                    }
                ],
                "name": "localhost",
                "url": "http://localhost:8090/"
            }
        }
    }

.. _node_root_post:

POST /api/node
--------------

Register a new Cuckoo node by providing the name and the URL::

    $ curl http://localhost:9003/api/node -F name=localhost \
        -F url=http://localhost:8090/
    {
        "success": true
    }

.. _node_get:

GET /api/node/<name>
--------------------

Get basic information about a particular Cuckoo node::

    $ curl http://localhost:9003/api/node/localhost
    {
        "success": true,
        "nodes": [
            {
                "name": "localhost",
                "url": "http://localhost:8090/"
                "machines": [
                    {
                        "name": "cuckoo1",
                        "platform": "windows",
                        "tags": []
                    }
                ]
            }
        ]
    }

.. _node_put:

PUT /api/node/<name>
--------------------

Update basic information of a Cuckoo node::

    $ curl -XPUT http://localhost:9003/api/node/localhost -F name=newhost \
        -F url=http://1.2.3.4:8090/
    {
        "success": true
    }

.. _node_delete:

DELETE /api/node/<name>
-----------------------

Disable a Cuckoo node, therefore not having it process any new tasks, but
keeping its history in the Distributed's database::

    $ curl -XDELETE http://localhost:9003/node/localhost
    {
        "success": true
    }

.. _task_root_get:

GET /api/task
-------------

Get a list of all tasks in the database. In order to limit the amount of
results, there's an ``offset``, ``limit``, ``finished``, and ``owner`` field
available::

    $ curl http://localhost:9003/api/task?limit=1
    {
        "success": true,
        "tasks": {
            "1": {
                "clock": null,
                "custom": null,
                "owner": "",
                "enforce_timeout": null,
                "machine": null,
                "memory": null,
                "options": null,
                "package": null,
                "path": "/tmp/dist-samples/tmphal8mS",
                "platform": "windows",
                "priority": 1,
                "tags": null,
                "task_id": 1,
                "timeout": null
            }
        }
    }

.. _task_root_post:

POST /api/task
--------------

Submit a new file or URL to be analyzed::

    $ curl http://localhost:9003/api/task -F file=@sample.exe
    {
        "success": true,
        "task_id": 2
    }

.. _task_get:

GET /api/task/<id>
------------------

Get basic information about a particular task::

    $ curl http://localhost:9003/api/task/2
    {
        "success": true,
        "tasks": {
            "2": {
                "id": 2,
                "clock": null,
                "custom": null,
                "owner": "",
                "enforce_timeout": null,
                "machine": null,
                "memory": null,
                "options": null,
                "package": null,
                "path": "/tmp/tmpPwUeXm",
                "platform": "windows",
                "priority": 1,
                "tags": null,
                "timeout": null,
                "task_id": 1,
                "node_id": 2,
                "finished": false
            }
        }
    }

.. _task_delete:

DELETE /api/task/<id>
---------------------

Delete all associated data of a task, namely the binary and the reports::

    $ curl -XDELETE http://localhost:9003/api/task/2
    {
        "success": true
    }

.. _report_get:

GET /api/report/<id>/<format>
-----------------------------

Fetch a report for the given task in the specified format::

    # Defaults to the JSON report.
    $ curl http://localhost:9003/report/2
    ...

.. _quick-usage:

Quick usage
===========

For practical usage the following few commands will be most interesting.

Register a Cuckoo node - a Cuckoo API running on the same machine in this
case::

    $ curl http://localhost:9003/api/node \
        -F name=localhost -F url=http://localhost:8090/

Disable a Cuckoo node::

    $ curl -XDELETE http://localhost:9003/api/node/localhost

Submit a new analysis task without any special requirements (e.g., using
Cuckoo ``tags``, a particular machine, etc)::

    $ curl http://localhost:9003/api/task -F file=@/path/to/sample.exe

Get the report of a task has been finished (if it hasn't finished you'll get
an error with code 420). Following example will default to the ``JSON``
report::

    $ curl http://localhost:9003/api/report/1

Proposed setup
==============

The following description depicts a Distributed Cuckoo setup with two Cuckoo
machines, **cuckoo0** and **cuckoo1**. In this setup the first machine,
cuckoo0, also hosts the Distributed Cuckoo REST API.

Configuration settings
----------------------

Our setup will require a couple of updates with regards to the configuration
files.

conf/cuckoo.conf
^^^^^^^^^^^^^^^^

Update ``process_results`` to ``off`` as we will be running our own results
processing script (for performance reasons).

Update ``tmppath`` to something that holds enough storage to store a few
hundred binaries. On some servers or setups ``/tmp`` may have a limited amount
of space and thus this wouldn't suffice.

Update ``connection`` to use something *not* sqlite3. Preferably PostgreSQL or
MySQL. SQLite3 doesn't support multi-threaded applications that well and this
will give errors at random if used.

You should create your own empty database for the distributed cuckoo setup. Do not be tempted to use any existing cuckoo database in order to avoid update problems with the DB scripts. In the config use the new database name, the remaining stuff like usernames , servers can be the same as for your cuckoo install.Don´t forget to use one DB per node and another one more for the first machine which run the distributed script (so the say the "management machine" ).

conf/processing.conf
^^^^^^^^^^^^^^^^^^^^

You may want to disable some processing modules, such as ``virustotal``.

conf/reporting.conf
^^^^^^^^^^^^^^^^^^^

Depending on which report(s) are required for integration with your system it
might make sense to only make those report(s) that you're going to use. Thus
disable the other ones.

conf/virtualbox.conf
^^^^^^^^^^^^^^^^^^^^

Assuming ``VirtualBox`` is the Virtual Machine manager of choice, the ``mode``
will have to be changed to ``headless`` or you will have some restless nights.

Setup Cuckoo
------------

On each machine the following three scripts should be ran::

    ./cuckoo.py
    ./utils/api.py -H 1.2.3.4  # IP accessible by the Distributed script.
    ./utils/process.py auto

One way to do this is by placing each script in its own ``screen(1)`` session
as follows, this allows one to check back on each script to ensure it's
(still) running successfully::

    $ screen -S cuckoo  ./cuckoo.py
    $ screen -S api     ./utils/api.py
    $ screen -S process ./utils/process.py auto

Setup Distributed Cuckoo
------------------------

On the first machine (so the say the "management machine" ) start a few separate ``screen(1)`` sessions for the
Distributed Cuckoo scripts with all the required parameters (see the rest of
the documentation on the parameters for this script)::

    $ screen -S distributed ./distributed/app.py
    $ SCREEN -S dist_scheduler ./distributed/instance.py dist.scheduler
    $ SCREEN -S dist_status ./distributed/instance.py dist.status
    $ SCREEN -S cuckoo0 ./distributed/instance.py -v cuckoo0
    $ SCREEN -S cuckoo1 ./distributed/instance.py -v cuckoo1

The -v parameter enables verbose output and the cuckoo1 parameter is the name assigned to the actual cuckoo instance running the virtual machine while registering the node as outlined below.It´s mandatory to register the nodes before run the instance.py due to the script check the DB.

Register Cuckoo nodes
---------------------

As outlined in :ref:`quick-usage` the Cuckoo nodes have to be registered with
the Distributed Cuckoo script::

    $ curl http://localhost:9003/api/node -F name=cuckoo0 -F url=http://localhost:8090/
    $ curl http://localhost:9003/api/node -F name=cuckoo1 -F url=http://1.2.3.4:8090/

Having registered the Cuckoo nodes all that's left to do now is to submit
tasks and fetch reports once finished. Documentation on these commands can be
found in the :ref:`quick-usage` section. In case you are not using localhost, replace localhost with the IP of the node where there distributed.py is running and the -F url parameter points to the nodes running the actual virtual machines.

If you want to experiment a real load balancing between the nodes you should use a lower value for the threshold parameter in the distributed/settings.py file, the default value is 500.

## 分析包
  =================
Analysis Packages
=================

The **analysis packages** are a core component of Cuckoo Sandbox.
They consist in structured Python classes which, when executed in the guest machines,
describe how Cuckoo's analyzer component should conduct the analysis.

Cuckoo provides some default analysis packages that you can use, but you are
able to create your own or modify the existing ones.
You can find them at *analyzer/windows/modules/packages/*.

As described in :doc:`../usage/submit`, you can specify some options to the
analysis packages in the form of ``key1=value1,key2=value2``. The existing analysis
packages already include some default options that can be enabled.

Following is the list of existing packages in alphabetical order:

    * ``applet``: used to analyze **Java applets**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``class``: specify the name of the class to be executed. This option is mandatory for a correct execution.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``bin``: used to analyze generic binary data, such as **shellcodes**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``cpl``: used to analyze **Control Panel Applets**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``dll``: used to run and analyze **Dynamically Linked Libraries**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``function``: specify the function to be executed. If none is specified, Cuckoo will try to run ``DllMain``.
            * ``arguments``: specify arguments to pass to the DLL through commandline.
            * ``loader``: specify a process name to use to fake the DLL launcher name instead of rundll32.exe (this is used to fool possible anti-sandboxing tricks of certain malware)
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``doc``: used to run and analyze **Microsoft Word documents**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``exe``: default analysis package used to analyze generic **Windows executables**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``arguments``: specify any command line argument to pass to the initial process of the submitted malware.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``generic``: used to run and analyze **generic samples** via cmd.exe.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``html``: used to analyze **Internet Explorer**'s behavior when opening the given HTML file.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``ie``: used to analyze **Internet Explorer**'s behavior when opening the given URL.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``jar``: used to analyze **Java JAR** containers.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``class``: specify the path of the class to be executed. If none is specified, Cuckoo will try to execute the main function specified in the Jar's MANIFEST file.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``msi``: used to run and analyze **MSI windows installer**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``pdf``: used to run and analyze **PDF documents**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``ppt``: used to run and analyze **Microsoft PowerPoint documents**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``ps1``: used to run and analyze **PowerShell scripts**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``python``: used to run and analyze **Python scripts**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``vbs``: used to run and analysis **VBScript files**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``xls``: used to run and analyze **Microsoft Excel documents**.

        **Options**:
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

    * ``zip``: used to run and analyze **Zip archives**.

        **Options**:
            * ``file``: specify the name of the file contained in the archive to execute. If none is specified, Cuckoo will try to execute *sample.exe*.
            * ``free`` *[yes/no]*: if enabled, no behavioral logs will be produced and the malware will be executed freely.
            * ``arguments``: specify any command line argument to pass to the initial process of the submitted malware.
            * ``password``: specify the password of the archive. If none is specified, Cuckoo will try to extract the archive without password or use the password "*infected*".
            * ``procmemdump`` *[yes/no]*: if enabled, take memory dumps of all actively monitored processes.

You can find more details on how to start creating new analysis packages in the
:doc:`../customization/packages` customization chapter.

As you already know, you can select which analysis package to use by specifying
its name at submission time (see :doc:`submit`) as follows::

    $ ./utils/submit.py --package <package name> /path/to/malware

If none is specified, Cuckoo will try to detect the file type and select
the correct analysis package accordingly. If the file type is not supported by
default the analysis will be aborted, therefore we encourage to
specify the package name whenever possible.

For example, to launch a malware and specify some options you can do::

    $ ./utils/submit.py --package dll --options function=FunctionName,loader=explorer.exe /path/to/malware.dll

## 分析结果
  ================
Analysis Results
================

Once an analysis is completed, several files are stored in a dedicated directory.
All the analyses are stored under the directory *storage/analyses/* inside a
subdirectory named after the incremental numerical ID that represents the analysis
task in the database.

Following is an example of an analysis directory structure::

    .
    |-- analysis.conf
    |-- analysis.log
    |-- binary
    |-- dump.pcap
    |-- memory.dmp
    |-- files
    |   |-- 1234567890
    |       `-- dropped.exe
    |-- logs
    |   |-- 1232.raw
    |   |-- 1540.raw
    |   `-- 1118.raw
    |-- reports
    |   |-- report.html
    |   |-- report.json
    `-- shots
        |-- 0001.jpg
        |-- 0002.jpg
        |-- 0003.jpg
        `-- 0004.jpg

analysis.conf
=============

This is a configuration file automatically generated by Cuckoo to give
its analyzer some details about the current analysis. It's generally of no
interest to the end-user, as it's used internally by the sandbox.

analysis.log
============

This is a log file generated by the analyzer and that contains a trace of
the analysis execution inside the guest environment. It will report the
creation of processes, files and eventual errors occurred during the
execution.

dump.pcap
=========

This is the network dump generated by tcpdump or any other corresponding
network sniffer.

memory.dmp
==========

In case you enabled it, this file contains the full memory dump of the analysis
machine.

files/
======

This directory contains all the files the malware operated on and that Cuckoo
was able to dump.

logs/
=====

This directory contains all the raw logs generated by Cuckoo's process monitoring.

reports/
========

This directory contains all the reports generated by Cuckoo as explained in the
:doc:`../installation/host/configuration` chapter.

shots/
======

This directory contains all the screenshots of the guest's desktop taken during
the malware execution.

## 清理所有任务和样本
.. _cuckoo-clean:

===========================
Clean all Tasks and Samples
===========================

Since Cuckoo 1.2 a built-in **--clean** feature has been added, it
drops all associated information of the tasks and samples in the
database. If you submit a task after running
**--clean** then you'll start with ``Task #1`` again.

To clean your setup, run::

    $ ./cuckoo.py --clean

To sum up, this command does the following:

* Delete analysis results.
* Delete submitted binaries.
* Delete all associated information of the tasks and samples in the configured database.
* Delete all data in the configured MongoDB (if configured and enabled in reporting.conf).

.. warning::
   If you use this command you will delete permanently all data stored by Cuckoo in all
   storages: file system, SQL database and MongoDB database. Use it only if you are sure
   you would clean up all the data.

