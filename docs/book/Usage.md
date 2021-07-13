---
sort: 3

---

# 3.使用

这部分解释如何使用Bold-Falcon沙箱

### 3.1 启动沙箱

使用如下命令启动 Bold-Falcon沙箱：

```shell
$ cuckoo
```

你会得到如下类似的输出：

```shell
     ____        _     _       _____     _                 
    | __ )  ___ | | __| |     |  ___|_ _| | ___ ___  _ __  
    |  _ \ / _ \| |/ _` |_____| |_ / _` | |/ __/ _ \| '_ \ 
    | |_) | (_) | | (_| |_____|  _| (_| | | (_| (_) | | | |
    |____/ \___/|_|\__,_|     |_|  \__,_|_|\___\___/|_| |_|
    

 Bold-Falcon Sandbox 2.0-dev
 https://github.com/PowerLZY/Bold-Falcon
 Copyright (c) 2020-2021

2021-07-12 21:58:45,841 [lib.cuckoo.core.resultserver] WARNING: Cannot bind ResultServer on port 2042, trying another port.
2021-07-12 21:58:45,843 [lib.cuckoo.core.scheduler] INFO: Using "virtualbox" as machine manager
2021-07-12 21:58:47,256 [lib.cuckoo.core.scheduler] INFO: Loaded 1 machine/s
2021-07-12 21:58:47,270 [lib.cuckoo.core.scheduler] INFO: Waiting for analysis tasks.
```

你可以使用一些命令行选项用过`cuckoo --help`

```shell
$ cuckoo --help
usage: cuckoo.py [-h] [-q] [-d] [-v] [-a] [-t] [-m MAX_ANALYSIS_COUNT]
                 [-u USER] [--ml] [--clean]

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
  --ml                  CuckooML: cluster reports and compare new samples
  --clean               Remove all tasks and samples and their associated data

```

### 3.2 样本提交

Bold-Falcon沙箱有`Django Web`、`Submit`and`API`三种分析样本的方法。

#### 3.2.1 Django Web

Bold-Falcon以Django应用程序的形式提供了一个完整的web界面。此界面将允许您提交文件、浏览报告以及统计所有分析结果。

##### **配置**

Web界面从`Mongo`数据库中提取数据，因此在`reporting`模块中启用了`Mongo` 模块。配置文件是Web界面运行所必需的。`Bold-Falcon/web/local_settings.py`配置文件中存在一些其他配置选项。

##### **启动Web界面**

要启动web界面，只需从`Bold-Falcon/web`目录运行以下命令：

```shell
$  manage.py 
```

如果要将web界面配置为侦听指定端口上的任何IP，可以使用以下命令启动它（用所需的端口号替换端口）：

```shell
$  manage.py 0.0.0.0:PORT
```

#### 3.2.2 Submit脚本

提交分析的最简单方法是在`utils\submit.py` 使用`Bold-Falcon submit`实用程序。它目前有以下可用选项：

```shell
$  submit --help
usage: submit.py [-h] [-d] [--remote REMOTE] [--url] [--package PACKAGE]
                 [--custom CUSTOM] [--owner OWNER] [--timeout TIMEOUT]
                 [-o OPTIONS] [--priority PRIORITY] [--machine MACHINE]
                 [--platform PLATFORM] [--memory] [--enforce-timeout]
                 [--clock CLOCK] [--tags TAGS] [--baseline] [--max MAX]
                 [--pattern PATTERN] [--shuffle] [--unique] [--quiet]
                 [target]

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
  --baseline            Run a baseline analysis
  --max MAX             Maximum samples to add in a row
  --pattern PATTERN     Pattern of files to submit
  --shuffle             Shuffle samples before submitting them
  --unique              Only submit new samples, ignore duplicates
  --quiet               Only print text on failure
```

##### 以下是一些用法示例：

##### (1) 提交一个本地文件

```shell
$  submit /path/to/binary
```

##### (2) 提交一个本地文件并明确优先级

```shell
$  submit --priority 5 /path/to/binary
```

##### (3) 提交一个本地文件并明确分析60s

```shell
$  submit --timeout 60 /path/to/binary
```

#### 3.2.2  API访问

正如提交分析中所提到的，Bold-Falcon沙箱兼容cuckoo沙箱提供了一个简单而轻量级的restapi服务器，它是使用Flask实现的。

##### 开启API服务器

在`Bold-Falcon\utils`使用如下命令启动 API服务：

```shell
$  api
$  * Running on http://localhost:8090/ (Press CTRL+C to quit)
```

默认情况下，它绑定的服务是`localhost:8090`,如果你想要的去改变这些值，可以使用如下语法：

```shell
$  cuckoo api --host 0.0.0.0 --port 1337
$  cuckoo api -H 0.0.0.0 -p 1337
```

使用API需要进行身份验证，必须将``cuckoo.conf``的``api_token``的值填充在``Authorization: Bearer <token>``中。

#### 资源

以下是当前可用资源的列表以及每个资源的简要说明。有关详细信息，请单击资源名称。

| 访问方式                    | 描述                                          |
| --------------------------- | --------------------------------------------- |
| `POST /tasks/create/file`   | 将文件添加到待处理任务列表中并分析            |
| `POST /tasks/create/url`    | 将URL添加到待处理任务列表中并分析             |
| `POST /tasks/create/submit` | 将一个或多个文件添加到待分析的任务列表中      |
| `GET /tasks/list`           | 返回一个存储在内部Bold-Falcon数据库的任务列表 |
| `GET /tasks/sample`         | 返回一个存储在内部Bold-Falcon数据库的样本列表 |
| `GET /tasks/view`           | 返回一个对应ID的任务信息                      |
| `GET /tasks/delete`         | 删除一个数据库中的任务信息                    |
| `GET /tasks/report`         | 返回一个对应ID任务生成的json报告              |
| `GET /tasks/summary`        | 返回一个对应ID任务生成的摘要json报告          |
| `GET /tasks/screenshots`    | 返回一个对应ID任务生成的所有截图文件          |
| `GET /files/view`           | 返回一个对应ID的MD5、SHA256等标识             |
| `GET /files/get`            | 返回二进制样本内容和对应SHA256                |
| `GET /pcap/get`             | 返回相关任务的PCAP网络流量包                  |
| `GET  /machines/list`       | 返回目前Bold-Falcon依赖的虚拟机列表           |
| `GET /cuckoo/status`        | 返回目前Bold-Falcon的版本和状态               |
| `GET /exit`                 | 关闭API服务器                                 |

**以下是一些用法示例：**                                                       

##### （1）POST /tasks/create/file

将文件添加到待处理任务列表中并分析

**请求示例**:

```shell
curl -H "Authorization: Bearer S4MPL3" -F file=@/path/to/file http://localhost:8090/tasks/create/file
```

##### 使用Python的请求示例


```python
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
```

**响应示例**

```json
{
    "task_id" : 1
}
```

##### **（2）POST /tasks/create/url**

将URL添加到待处理任务列表中并分析

**请求示例**


```shell
curl -H "Authorization: Bearer S4MPL3" -F url="http://www.malicious.site" http://localhost:8090/tasks/create/url
```

##### 使用Python的请求示例

```python
import requests

REST_URL = "http://localhost:8090/tasks/create/url"
SAMPLE_URL = "http://example.org/malwr.exe"
HEADERS = {"Authorization": "Bearer S4MPL3"}

data = {"url": SAMPLE_URL}
r = requests.post(REST_URL, headers=HEADERS, data=data)

# Add your code to error checking for r.status_code.

task_id = r.json()["task_id"]

# Add your code to error checking if task_id is None.
```

**（3）POST /tasks/create/submit**

将一个或多个文件添加到待分析的任务列表中

**请求示例**.


```shell
# Submit two executables.
curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/create/submit -F files=@1.exe -F files=@2.exe

# Submit http://google.com
curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/create/submit -F strings=google.com

# Submit http://google.com & http://facebook.com
curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/tasks/create/submit -F strings=$'google.com\nfacebook.com'
```

##### 使用Python的请求示例


```python
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
```

**响应事例** 


```json
{
    "submit_id": 1,
    "task_ids": [1, 2],
    "errors": []
}
```

##### （4） GET /files/get/ *(str: sha256)*

返回二进制样本内容和对应SHA256

**请求示例**.

```shell
curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/files/get/e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 > sample.exe
```

##### （5）GET /machines/list


返回目前Bold-Falcon依赖的虚拟机列表

**请求示例**.

```shell
curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/machines/list
```

**响应示例**.

```json
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
```

##### （6）GET /exit

如果处于调试模式并使用werkzeug服务器，则关闭服务器。

**请求示例**.

```shell
curl -H "Authorization: Bearer S4MPL3" http://localhost:8090/exit
```

### 3.3 社区

Bold-Falcon沙箱兼容Cuckoo沙箱的[开源社区](https://github.com/cuckoosandbox/community),它是一个致力于社区贡献的开放存储库。在这里，您可以提交为布谷鸟沙盒设置编写的自定义模块，并希望与社区的其他成员共享这些模块。其中包括代理agent、分析脚本analzyer和各种功能模块。

如果想要从[开源社区](https://github.com/cuckoosandbox/community)下载对应数据到`Bold-Falcon\data`下，可以使用`Bold-Falcon\utils\community`：

```shell
$  cummunity -h
usage: community.py [-h] [-a] [-s] [-p] [-m] [-n] [-M] [-g] [-r] [-f] [-w]
                    [-b BRANCH]
                    [archive]

positional arguments:
  archive               Install a stored archive

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             Download everything
  -s, --signatures      Download Cuckoo signatures
  -p, --processing      Download processing modules
  -m, --machinery       Download machine managers
  -n, --analyzer        Download analyzer modules
  -M, --monitor         Download monitoring binaries
  -g, --agent           Download agent modules
  -r, --reporting       Download reporting modules
  -f, --force           Install files without confirmation
  -w, --rewrite         Rewrite existing files
  -b BRANCH, --branch BRANCH
```

##### 例：重写所有开源数据到最新版

```shell
$  cummunity -waf
```

### 3.4 分析样本获取

##### 样本分享

Bold-Falcon沙箱分享了200个已经分析完成的json报告在`百度云盘`如下链接：

```html
https://pan.baidu.com/s/19TRWbQSRWJHetUBpNtMj_w 提取码: r7gk 
```

Bold-Falcon沙箱分享了一些32bit的windows样本在`百度云盘`如下链接：

```
https://pan.baidu.com/s/1x6a9j7D7Ktp242fcJhT5aA 提取码: qxbp 
```

##### 开源样本

如果你想要获取更多的`恶意样本`请访问查询：

**推荐：**

-   [Blue Hexagon Open Dataset for Malware AnalysiS (BODMAS)](https://whyisyoung.github.io/BODMAS/)
-   [EMBER](https://github.com/elastic/ember) - Endgame Malware BEnchmark for Research
-   [Malware Training Sets: A machine learning dataset for everyone](http://marcoramilli.blogspot.cz/2016/12/malware-training-sets-machine-learning.html) ([data](https://github.com/marcoramilli/MalwareTrainingSets))
-   [SoReL-20M](https://github.com/sophos-ai/SOREL-20M) - Sophos-ReversingLabs 20 Million dataset.
-   [Virusshare](https://virusshare.com/)

**其他：**

+   [Samples of Security Related Dats](http://www.secrepo.com/)
+   [DARPA Intrusion Detection Data Sets](https://www.ll.mit.edu/ideval/data/)
+   [Stratosphere IPS Data Sets](https://stratosphereips.org/category/dataset.html)
+   [Open Data Sets](http://csr.lanl.gov/data/)
+   [Data Capture from National Security Agency](http://www.westpoint.edu/crc/SitePages/DataSets.aspx)
+   [The ADFA Intrusion Detection Data Sets](https://www.unsw.adfa.edu.au/australian-centre-for-cyber-security/cybersecurity/ADFA-IDS-Datasets)
+   [NSL-KDD Data Sets](https://github.com/defcom17/NSL_KDD)
+   [Malicious URLs Data Sets](https://sysnet.ucsd.edu/projects/url)
+   [Multi-Source Cyber-Security Events](http://csr.lanl.gov/data/cyber1/)
+   [Malware Training Sets: A machine learning dataset for everyone](http://marcoramilli.blogspot.cz/2016/12/malware-training-sets-machine-learning.html)

如果你想要获取更多的`良性样本`请在如下等网络自行爬取：

-   [portablefreeware](http://www.portablefreeware.com/)
-   [onlyfreewares](http://www.onlyfreewares.com/)
-   [snapfiles](https://www.snapfiles.com/new/list-whatsnew.html)
-   [downloadcrew](https://downloadcrew.com/)

