---
sort: 2
---
# 使用


## REST API


### 启动API服务器

为了启动API服务器，您只需:

    $ cuckoo api

默认情况下，它绑定的服务是**localhost:8090**,如果你想要的去改变这些值，可以使用如下语法：

    $ cuckoo api --host 0.0.0.0 --port 1337
    $ cuckoo api -H 0.0.0.0 -p 1337

使用API需要进行身份验证，必须将``cuckoo.conf``的``api_token``的值填充在``Authorization: Bearer <token>``中。


### 资源

以下是当前可用资源的列表。
| 资源                           | 描述                                                                                                     |
| ------                           |------|
|  `POST tasks_create_file`  | 将文件添加到待处理和分析的挂起任务列表中。                                           |
|  `POST tasks_create_url`    | 将URL添加到待处理和分析的挂起任务列表中。                                          |
| `POST tasks_create_submit` |   将一个或多个文件和/或嵌入存档中的文件添加到挂起任务列表中。                        |
| ` GET tasks_list`           |      返回存在是数据库中的任务列表，可以选择指定要返回的条目的限制。                                            |
| ` GET tasks_view`           |         返回分配给指定ID的任务的详细信息。                                            |
| `GET tasks_reschedule`     | 重新安排分配给指定ID的任务。                                                                |
| `GET tasks_delete`         | 从数据库中删除给定任务并删除结果。                                               |
| `GET tasks_report`         | 返回通过分析与指定ID关联的任务而生成的报告，可以选择指定要返回的报告格式，如果未指定任何格式，则将返回JSON报告。|
| `GET tasks_summary`        | 返回JSON格式的压缩报表。                                                                   |
| `GET tasks_shots`          |  检索与给定分析任务ID关联的一个或所有屏幕截图。                                      |
| `GET tasks_rereport`       |     为与给定分析任务ID关联的任务重新运行报告。                                          |
| `GET tasks_reboot`         |    重新启动给定的分析任务ID。                                                                             |
| `GET memory_list`          | 返回与给定分析任务ID关联的内存转储文件列表。                                  |
| `GET  memory_get`           |   检索一个与给定分析任务ID关联的内存转储文件。                                       |
| `GET files_view`           | 按MD5 hash、SHA256 hash或内部ID（由任务详细信息引用）搜索分析的二进制文件。       |
| `GET files_get`            |  返回具有指定SHA256哈希的二进制文件的内容。                                              |
| `GET api_pcap_get`         |   返回与给定任务关联的PCAP的内容。                                             |
| `GET machines_list`        |   返回杜鹃可用的分析机器列表。                                                     |
| `GET machines_view`        |    返回与指定名称关联的分析计算机的详细信息。                                   |
| `GET cuckoo_status`        |       返回基本的沙箱状态，包括版本和任务概述。                                     |
| `GET vpn_status`           | 返回VPN的状态                                                                                             |
| `GET exit`                 | 关闭API服务器                                                                                     |


#### /tasks/create/file
**POST /tasks/create/file**

将文件添加到挂起任务的列表中。返回新创建任务的ID。

**请求示例**:

    curl -H "Authorization: Bearer S4MPL3" -F file=@/path/to/file http://localhost:8090/tasks/create/file

**使用Python的请求示例**..


    import requests

    REST_URL = "http://localhost:8090/tasks/create/file"
    SAMPLE_FILE = "/path/to/malwr.exe"
    HEADERS = {"Authorization": "Bearer S4MPL3"}

    with open(SAMPLE_FILE, "rb") as sample:
        files = {"file": ("temp_file_name", sample)}
        r = requests.post(REST_URL, headers=HEADERS, files=files)

    # Add your code to error checking for r.status_code.

    task_id = r.json()["task_id"]

    # Add your code for error checking if task_id is None.

**响应示例**.

    {
        "task_id" : 1
    }

**参数**:

* ``file`` *(required)* - sample file (multipart encoded file content)
* ``package`` *(optional)* - analysis package to be used for the analysis
* ``timeout`` *(optional)* *(int)* - analysis timeout (in seconds)
* ``priority`` *(optional)* *(int)* - priority to assign to the task (1-3)
* ``options`` *(optional)* - options to pass to the analysis package
* ``machine`` *(optional)* - label of the analysis machine to use for the analysis
* ``platform`` *(optional)* - name of the platform to select the analysis machine from (e.g. "windows")
* ``tags`` *(optional)* - define machine to start by tags. Platform must be set to use that. Tags are comma separated
* ``custom`` *(optional)* - custom string to pass over the analysis and the processing/reporting modules
* ``owner`` *(optional)* - task owner in case multiple users can submit files to the same cuckoo instance
* ``clock`` *(optional)* - set virtual machine clock (format %m-%d-%Y %H:%M:%S)
* ``memory`` *(optional)* - enable the creation of a full memory dump of the analysis machine
* ``unique`` *(optional)* - only submit samples that have not been analyzed before
* ``enforce_timeout`` *(optional)* - enable to enforce the execution for the full timeout value

**状态码**:

* ``200`` - no error
* ``400`` - duplicated file detected (when using unique option)


#### /tasks/create/url

**POST /tasks/create/url**

Adds a file to the list of pending tasks. Returns the ID of the newly created task.

**请求示例**.


    curl -H "Authorization: Bearer S4MPL3" -F url="http://www.malicious.site" http://localhost:8090/tasks/create/url

**Example request using Python**.

    import requests

    REST_URL = "http://localhost:8090/tasks/create/url"
    SAMPLE_URL = "http://example.org/malwr.exe"
    HEADERS = {"Authorization": "Bearer S4MPL3"}

    data = {"url": SAMPLE_URL}
    r = requests.post(REST_URL, headers=HEADERS, data=data)

    # Add your code to error checking for r.status_code.

    task_id = r.json()["task_id"]

    # Add your code to error checking if task_id is None.

**Example response**.


    {
        "task_id" : 1
    }

**Form parameters**:

* ``url`` *(required)* - URL to analyze (multipart encoded content)
* ``package`` *(optional)* - analysis package to be used for the analysis
* ``timeout`` *(optional)* *(int)* - analysis timeout (in seconds)
* ``priority`` *(optional)* *(int)* - priority to assign to the task (1-3)
* ``options`` *(optional)* - options to pass to the analysis package
* ``machine`` *(optional)* - label of the analysis machine to use for the analysis
* ``platform`` *(optional)* - name of the platform to select the analysis machine from (e.g. "windows")
* ``tags`` *(optional)* - define machine to start by tags. Platform must be set to use that. Tags are comma separated
* ``custom`` *(optional)* - custom string to pass over the analysis and the processing/reporting modules
* ``owner`` *(optional)* - task owner in case multiple users can submit files to the same cuckoo instance
* ``memory`` *(optional)* - enable the creation of a full memory dump of the analysis machine
* ``enforce_timeout`` *(optional)* - enable to enforce the execution for the full timeout value
* ``clock`` *(optional)* - set virtual machine clock (format %m-%d-%Y %H:%M:%S)

**Status codes**:

* ``200`` - no error

.. _tasks_create_submit:

#### /tasks/create/submit

**POST /tasks/create/submit**

Adds one or more files and/or files embedded in archives *or* a newline
separated list of URLs/hashes to the list of pending tasks. Returns the
submit ID as well as the task IDs of the newly created task(s).

**请求示例**.


    # Submit two executables.
    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/create/submit -F files=@1.exe -F files=@2.exe

    # Submit http://google.com
    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/create/submit -F strings=google.com

    # Submit http://google.com & http://facebook.com
    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/create/submit -F strings=$'google.com\nfacebook.com'

**Example request using Python**.


    import requests

    HEADERS = {"Authorization": "Bearer S4MPL3"}

    # Submit one or more files.
    r = requests.post("http://localhost:8090/tasks/create/submit", files=[
        ("files", open("1.exe", "rb")),
        ("files", open("2.exe", "rb")),
    ], headers=HEADERS)

    # Add your code to error checking for r.status_code.

    submit_id = r.json()["submit_id"]
    task_ids = r.json()["task_ids"]
    errors = r.json()["errors"]

    # Add your code to error checking on "errors".

    # Submit one or more URLs or hashes.
    urls = [
        "google.com", "facebook.com", "cuckoosandbox.org",
    ]
    r = requests.post(
        "http://localhost:8090/tasks/create/submit",
        headers=HEADERS,
        data={"strings": "\n".join(urls)}
    )

**Example response** from the executable submission.


    {
        "submit_id": 1,
        "task_ids": [1, 2],
        "errors": []
    }

**Form parameters**:

* ``file`` *(optional)* - backwards compatibility with naming scheme for :ref:`tasks_create_file`
* ``files`` *(optional)* - sample(s) to inspect and add to our pending queue
* ``strings`` *(optional)* - newline separated list of URLs and/or hashes (to be obtained using your VirusTotal API key)
* ``timeout`` *(optional)* *(int)* - analysis timeout (in seconds)
* ``priority`` *(optional)* *(int)* - priority to assign to the task (1-3)
* ``options`` *(optional)* - options to pass to the analysis package
* ``tags`` *(optional)* - define machine to start by tags. Platform must be set to use that. Tags are comma separated
* ``custom`` *(optional)* - custom string to pass over the analysis and the processing/reporting modules
* ``owner`` *(optional)* - task owner in case multiple users can submit files to the same cuckoo instance
* ``memory`` *(optional)* - enable the creation of a full memory dump of the analysis machine
* ``enforce_timeout`` *(optional)* - enable to enforce the execution for the full timeout value
* ``clock`` *(optional)* - set virtual machine clock (format %m-%d-%Y %H:%M:%S)

**Status codes**:

* ``200`` - no error


#### /tasks/list

**GET /tasks/list/** *(int: limit)* **/** *(int: offset)*

Returns list of tasks.

**请求示例**.


    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/list

**Example response**.

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

.. _tasks_sample:

#### /tasks/sample

**GET /tasks/sample/** *(int: sample_id)*

Returns list of tasks for sample.

**请求示例**.


    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/sample/1

**Example response**.


    {
        "tasks": [
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

* ``sample_id`` *(required)* *(int)* - sample id to list tasks for

**Status codes**:

* ``200`` - no error

#### /tasks/view

**GET /tasks/view/** *(int: id)*

Returns details on the task associated with the specified ID.

**请求示例**.


    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/view/1

**Example response**.


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


#### /tasks/reschedule

**GET /tasks/reschedule/** *(int: id)* **/** *(int: priority)*

Reschedule a task with the specified ID and priority (default priority
is 1).

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/reschedule/1

**Example response**.


    {
        "status": "OK"
    }

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to reschedule
* ``priority`` *(optional)* *(int)* - Task priority

**Status codes**:

* ``200`` - no error
* ``404`` - task not found


#### /tasks/delete

**GET /tasks/delete/** *(int: id)*

Removes the given task from the database and deletes the results.

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/delete/1

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to delete

**Status codes**:

* ``200`` - no error
* ``404`` - task not found
* ``500`` - unable to delete the task

#### /tasks/report

**GET /tasks/report/** *(int: id)* **/** *(str: format)*

Returns the report associated with the specified task ID.

**请求示例t**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/report/1

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to get the report for
* ``format`` *(optional)* - format of the report to retrieve [json/html/all/dropped/package_files]. If none is specified the JSON report will be returned. ``all`` returns all the result files as tar.bz2, ``dropped`` the dropped files as tar.bz2, ``package_files`` files uploaded to host by analysis packages.

**Status codes**:

* ``200`` - no error
* ``400`` - invalid report format
* ``404`` - report not found

.. _tasks_summary:

#### /tasks/summary

**GET /tasks/summary/** *(int: id)*

Returns a condensed report associated with the specified task ID in JSON format.

**请求示例**.


    curl http://localhost:8090/tasks/summary/1

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to get the report for

**Status codes**:

* ``200`` - no error
* ``404`` - report not found

#### /tasks/screenshots


**GET /tasks/screenshots/** *(int: id)* **/** *(str: number)*

Returns one or all screenshots associated with the specified task ID.

**请求示例**.
    wget http://localhost:8090/tasks/screenshots/1

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to get the report for
* ``screenshot`` *(optional)* - numerical identifier of a single screenshot (e.g. 0001, 0002)

**Status codes**:

* ``404`` - file or folder not found


#### /tasks/rereport

**GET /tasks/rereport/** *(int: id)*

Re-run reporting for task associated with the specified task ID.

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/rereport/1

**Example response**.

    {
        "success": true
    }

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to re-run report

**Status codes**:

* ``200`` - no error
* ``404`` - task not found


#### /tasks/reboot

**GET /tasks/reboot/** *(int: id)* **

Add a reboot task to database from an existing analysis ID.

**请求示例**.


    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/reboot/1

**Example response**.


    {
        "task_id": 1,
        "reboot_id": 3
    }

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task

**Status codes**:

* ``200`` - success
* ``404`` - error creating reboot task

#### /memory/list
**GET /memory/list/** *(int: id)*

Returns a list of memory dump files or one memory dump file associated with the specified task ID.

**请求示例**.

    wget http://localhost:8090/memory/list/1

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to get the report for

**Status codes**:

* ``404`` - file or folder not found


#### /memory/get


**GET /memory/get/** *(int: id)* **/** *(str: number)*

Returns one memory dump file associated with the specified task ID.

**Example request**.


    wget http://localhost:8090/memory/get/1/1908

**Parameters**:

* ``id`` *(required)* *(int)* - ID of the task to get the report for
* ``pid`` *(required)* - numerical identifier (pid) of a single memory dump file (e.g. 205, 1908)

**Status codes**:

* ``404`` - file or folder not found


#### /files/view

**GET /files/view/md5/** *(str: md5)*

**GET /files/view/sha256/** *(str: sha256)*

**GET /files/view/id/** *(int: id)*

Returns details on the file matching either the specified MD5 hash, SHA256 hash or ID.

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/files/view/id/1

**Example response**.

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

**参数**:

* ``md5`` *(optional)* - MD5 hash of the file to lookup
* ``sha256`` *(optional)* - SHA256 hash of the file to lookup
* ``id`` *(optional)* *(int)* - ID of the file to lookup

**状态码**:

* ``200`` - 成功
* ``400`` - 无效的查找项
* ``404`` - 文件找不到

#### /files/get

**GET /files/get/** *(str: sha256)*

返回与指定SHA256哈希匹配的文件的二进制内容。

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/files/get/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 > sample.exe

**状态码**:

* ``200`` - 成功
* ``404`` - 文件找不到


#### /pcap/get

**GET /pcap/get/** *(int: task)*

返回与给定任务关联的PCAP的内容。

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/pcap/get/1 > dump.pcap

**状态码**:

* ``200`` - 成功
* ``404`` - 文件找不到


#### /machines/list

**GET /machines/list**


返回一个列表，其中包含沙箱可以使用的分析机器的详细信息。

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/machines/list

**响应示例**.

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

**状态码**:

* ``200`` - 成功

#### /machines/view

**GET /machines/view/** *(str: name)*
返回与给定名称关联的分析计算机的详细信息。
**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/machines/view/cuckoo1

**响应示例**.

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

**状态码**:

* ``200`` - 成功
* ``404`` - 机器找不到


#### /cuckoo/status
--------------

**GET /cuckoo/status/**

返回布谷鸟服务器的状态。

**磁盘空间目录**:

* ``analyses`` - $CUCKOO/storage/analyses/
* ``binaries`` - $CUCKOO/storage/binaries/
* ``temporary`` - ``tmppath`` as specified in ``conf/cuckoo.conf``

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/cuckoo/status

**响应示例**.

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

**状态码**:

* ``200`` - 成功
* ``404`` - 机器找不到


#### /vpn/status

**GET /vpn/status**

返回VPN状态

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/vpn/status

**状态码**:

* ``200`` - 成功
* ``500`` - 不可得


#### /exit

**GET /exit**

如果处于调试模式并使用werkzeug服务器，则关闭服务器。

**请求示例**.

    curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/exit

**状态码**:

* ``200`` - 成功
* ``403`` - 此调用只能在调试模式下使用
* ``500`` - 错误
