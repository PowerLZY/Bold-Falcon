---
sort: 2

---

# 安装

Bold-Falcon的主机安装过程推荐在*GNU/Linux*（最好是Debian或Ubuntu）上进行，当然在*Max OS X*和*Microsoft Windows 7*上也可以正常使用。对于客户机安装过程，Windows分析任务推荐在*Windows XP*或*64位Windows 7*系统上进行，Mac OS X分析任务推荐在*Mac OS X Yosemite*上进行，Linux分析任务推荐在Debian上进行，尽管Bold-Falcon理论上也可以与其他版本的客户机操作系统配合使用。不要使用Windows Linux子系统（WLS）运行Bold-Falcon.

## 2.1 准备主机(HOST)

主机是指运行Bold-Falcon的底层操作系统（通常为GNU/Linux发行版），在本文档中我们使用Ubuntu LTS 16.04为例进行介绍。

### 2.1.1 环境配置要求

在安装和配置Bold-Falcon之前，需要安装一些必需的软件包和依赖库。

#### 基于Ubuntu/Debian发行版

Bold-Falcon的主机组件完全基于Python 2.7编写。为了确保Bold-Falcon能够正确安装并运行，需要从apt软件库中安装以下软件包：

```shell
$ sudo apt-get install python python-pip python-dev libffi-dev libssl-dev
$ sudo apt-get install python-virtualenv python-setuptools
$ sudo apt-get install libjpeg-dev zlib1g-dev swig
```

为了使用基于Django的Web界面，需要安装MongoDB：

```shell
$ sudo apt-get install mongodb
```

建议使用PostgreSQL作为数据库，需要安装PostgreSQL：

```shell
$ sudo apt-get install postgresql libpq-dev
```

还有一些可选插件或Python库，以实现特定的功能：

- Pydeep - pydeep
- KVM - KVM
- XenServer - XenAPI
- mitm - mitmproxy

#### 基于Mac OS X

这与基于Ubuntu/Debian的安装与配置过程基本相同，只是在当前环境中将使用brew包管理工具来安装所需的依赖：

```shell
$ brew install libmagic cairo pango openssl
```

此外，如果希望在GCC/Clang包含目录中公开openssl头文件，从而使得yara-python能够成功编译，可以按以下步骤操作：

```shell
$ cd /usr/local/include
$ ln -s ../opt/openssl/include/openssl
```

#### 虚拟化软件

Bold-Falcon支持大多数虚拟化软件解决方案，并已经尽可能地保持模块化。这使得沙箱在丢失与软件集成的情况下，仍然可以被很容易地添加。在本文档中我们默认安装VirtualBox，使用以下命令可以在Ubuntu LTS上安装最新版本的VirtualBox：

```shell
$ echo deb http://download.virtualbox.org/virtualbox/debian xenial contrib | sudo tee -a /etc/apt/sources.list.d/virtualbox.list
$ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install virtualbox-5.2
```

#### Tcpdump安装

为了转储恶意软件在执行过程中进行的网络活动，需要安装网络嗅探器tcpdump，该嗅探器经过适当配置可以捕获流量并将其转储到一个文件中。在Ubuntu上安装tcpdump的命令如下：

```shell
$ sudo apt-get install tcpdump apparmor-utils
$ sudo aa-disable /usr/sbin/tcpdump
```

必须将特定的Linux capabilities设置为二进制，以保证tcpdump无法以root权限运行。建议在允许tcpdump运行的专用系统或可信环境中运行Bold-Falcon.

```shell
$ sudo groupadd pcap
$ sudo usermod -a -G pcap cuckoo
$ sudo chgrp pcap /usr/sbin/tcpdump
$ sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
```

#### Volatility安装

Volatility是对内存转储进行取证分析的可选工具。通过与沙箱结合，它可以自动提供额外的可见信息，帮助使用者深入操作系统，并检测rootkit技术的存在。为了保证Bold-Falcon的正常工作，Volatility的版本至少应为2.3，建议使用最新版本，可以从[Volatility官方仓库](https://github.com/volatilityfoundation)下载。

#### M2Crypto安装

目前只有在安装了SWIG之后才能够支持M2Crypto库。在诸如Ubuntu/Debian的系统上，安装命令如下：

```shell
$ sudo apt-get install swig
$ sudo pip install m2crypto==0.24.0
```

#### guacd安装

guacd是一个可选的能够为前端web界面中的远程控制功能提供RDP、VNC和SSH的转换层服务。为了保证远程控制功能正常使用，guacd的版本至少应为0.9.9，建议使用最新版本。在Ubuntu 17.04系统上，安装0.9.9-2版本的命令如下：

```shell
$ sudo apt install libguac-client-rdp0 libguac-client-vnc0 libguac-client-ssh0 guacd
```

如果只需要RDP支持，可以跳过libguac-client-vnc0和libguac-client-ssh0包的安装。如果只想使用最新版本，则可以通过以下命令从源代码生成最新版本（0.9.14）：

```shell
$ sudo apt -y install libcairo2-dev libjpeg-turbo8-dev libpng-dev libossp-uuid-dev libfreerdp-dev
$ mkdir /tmp/guac-build && cd /tmp/guac-build
$ wget https://www.apache.org/dist/guacamole/0.9.14/source/guacamole-server-0.9.14. tar.gz
$ tar xvf guacamole-server-0.9.14.tar.gz && cd guacamole-server-0.9.14
$ ./configure --with-init-dir=/etc/init.d
$ make && sudo make install && cd ..
$ sudo ldconfig
$ sudo /etc/init.d/guacd start
```

从源代码安装时，需确保没有从包管理器安装任何libguac库的其他版本，否则可能会遇到由于版本不兼容而导致guacd奔溃的问题。

此外，还必须安装VituralBox扩展包，以利用Guacamole公开的沙箱控制功能。

#### Cuckoo安装

创建一个新用户，确保运行Cuckoo沙箱的用户与用于创建和运行VituralBox虚拟机的用户相同，否则沙箱将无法识别和启动这些虚拟机。创建新用户，并确保新用户属于当前用于运行VirtualBox的组。命令如下：

```shell
$ sudo adduser cuckoo
$ sudo usermod -a -G vboxusers cuckoo
```

如果在启动沙箱之前打开了过多的文件，可能导致某些进程无法正确处理报告，此时可能需要提升文件计数限制。

首先升级pip和setuptools库，然后安装最新版本的Cuckoo，推荐在虚拟环境中执行安装过程。原因有以下几点：

- Cuckoo的依赖项可能不完全是最新的，而是固定到已知的能够支持正常运行的版本
- 由于不兼容的版本要求，对于系统中安装的其他软件，其依赖关系可能与Cuckoo要求的软件冲突
- 使用虚拟环境允许非root用户在稍后安装其他软件包或进行升级

```shell
$ virtualenv venv
$ . venv/bin/activate
(venv)$ pip install -U pip setuptools
(venv)$ pip install -U cuckoo
```

还可以通过下载Cuckoo软件包文件离线安装，或者直接从[Cuckoo官方仓库](https://github.com/cuckoosandbox/cuckoo)克隆源代码进行安装。

#### 工作目录（CWD）

所有可配置组件、生成的数据和分析的结果都存储在此目录中。这些文件包括但不仅限于以下内容：

- 配置
- 签名
- 分析组件
- 代理
- Yara规则
- 分析结果存储文件
- ......

当第一次运行沙箱时，CWD会自动创建，默认为`/home/cuckoo/.cuckoo`. 所有配置文件都可以在`$CWD/conf`目录中找到。主要的配置文件如下：

- cuckoo.conf：用于配置常规行为和分析选项
- auxiliary.conf：用于启用和配置辅助模块
- <machinery>.conf：用于定义虚拟化软件的选项
- memory.conf：用于Volatility配置
- processing.conf：用于启用和配置处理模块
- reporting.conf：用于启用或禁用报告格式

## 2.2 准备客户机(Guest)

首先要在``Ubuntu``的``vitrualbox``中创建一个虚拟机，设定为``windows 7 64``位操作系统。

### 2.2.1 关闭防火墙、自动更新、UAC

+ [关闭防火墙](https://jingyan.baidu.com/article/dca1fa6f0953bbf1a44052d7.html)
+ [关闭自动更新](https://jingyan.baidu.com/article/03b2f78c4ce2ad5ea337ae5b.html)
+ [关闭UAC](http://www.win7zhijia.cn/jiaocheng/win7_26850.html)

### 2.2.2 安装PIL

``PIL``用于截屏，``cuckoo``生成报告中会有``windows 7``的截图。
首先进到``C:\Python27\Scripts``路径下，在此路径下安装``pillow``。

    >cd C:\Python27\Scripts
    >pip install Pillow
    Collecting Pillow
    Downloading Pillow-4.3.0-cp27-cp27m-win32.whl (1.3MB
      100% |################################| 1.3MB 114k
    Collecting olefile (from Pillow)
    Downloading olefile-0.44.zip (74kB)
      100% |################################| 81kB 145kB
    Installing collected packages: olefile, Pillow
    Running setup.py install for olefile ... done
    Successfully installed Pillow-4.3.0 olefile-0.44

### 2.2.3 agent.py设置开机自启动

前面主机中找到的``agent.py``文件上传到``windows 7``中，建议用``send anywhere``比较快速。把上传成功的``agent.py``文件放进``C:\Users[USER]\AppData\Roaming\MicroSoft\Windows\Start Menu\Programs\Startup\ ``下，并把后缀名改为``.pyw``。其中``users``是指用户名。

### 2.2.4 配置系统开机自动登录

使用``Administrator``权限启动``cmd``,并依序在cmd中输入以下指令
``[USERNAME]``和``[PASSWORD]``需替换为登入的``Windows user``与对应的``password``

    >reg add "hklm\software\Microsoft\Windows NT\CurrentVersion\WinLogon" /v DefaultUserName /d [USERNAME] /t REG_SZ /f
    >reg add "hklm\software\Microsoft\Windows NT\CurrentVersion\WinLogon" /v DefaultPassword /d [PASSWORD] /t REG_SZ /f
    >reg add "hklm\software\Microsoft\Windows NT\CurrentVersion\WinLogon" /v AutoAdminLogon /d 1 /t REG_SZ /f
    >reg add "hklm\system\CurrentControlSet\Control\TerminalServer" /v AllowRemoteRPC /d 0x01 /t REG_DWORD /f
    >reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v    LocalAccountTokenFilterPolicy /d 0x01 /t REG_DWORD /f

### 2.2.5 配置连接网络

在``virtualbox``中添加一块网卡，管理——主机网络管理器，按照下面信息进行设置。

<img src="https://user-images.githubusercontent.com/16918550/124224460-43f95f80-db38-11eb-8a0b-f365f4f00b50.png"  alt="网卡配置" style="zoom:67%;"/>

设置windows 7网络，设置为Host-Only。界面名称为刚刚设置的网卡。

<img src="https://user-images.githubusercontent.com/16918550/124224491-51164e80-db38-11eb-9348-66ac2cb4c6c7.png"  alt="网卡配置" style="zoom:67%;"/>

进入Windows 7 系统，设置win7 ip网络

<img src="https://user-images.githubusercontent.com/16918550/124224523-5c697a00-db38-11eb-93fb-a5b48d6577d5.png"  alt="网卡配置" style="zoom:67%;"/>

检查是否配置成功，主机和客机是否能通信。
主机中操作：

    $ ping 192.168.56.101

客机中操作：

    >ping 192.168.56.1

设置``IP``报文转发

这是在``Ubuntu``中的操作，因为``win7``无法上网，所以要通过主机才能访问网络，所以需要以下操作;流量转发服务：

    $ sudo vim /etc/sysctl.conf
    net.ipv4.ip_forward=1
    sudo sysctl -p /etc/systl.conf

使用``iptables``提供``NAT``机制
注意：其中``eth0``为``Ubuntu``中的网卡名称，需要提前查看自己``Ubuntu``中的网卡名称然后修改``eth0``

    $ sudo iptables -A FORWARD -o eth0 -i vboxnet0 -s 192.168.56.0/24 -m conntrack --ctstate NEW -j ACCEPT
    $ sudo iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    $ sudo iptables -A POSTROUTING -t nat -j MASQUERADE
    $ sudo vim /etc/network/interfaces
    #文件最终新增下面两行
    pre-up iptables-restore < /etc/iptables.rules 
    post-down iptables-save > /etc/iptables.rules

执行：

    sudo apt-get install iptables=persistent
    sudo netfilter-persistent save

``DNS``服务

    $ sudo apt-get install -y dnsmasq
    $ sudo service dnsmasq start

在``win7``中查看是否有网络：

    ping www.baidu.com

### 2.2.6 快照

要保证``agent.py``文件时运行状态，可以在``cmd``控制台启动，成功后对``win7``进行快照 名字取为``snapshot``。

### 2.2.7 设置cuckoo配置文件

配置``virtualbox.conf``：

    $ vim virtualbox.conf
    machines = cuckoo1 # 指定VirtualBox中Geust OS的虛擬機名稱
    [cuckoo1] # 對應machines
    label = cuckoo1  .
    platform = windows
    ip = 192.168.56.101 # 指定VirtualBox中Geust OS的IP位置
    snapshot =snapshot

配置``reporting.conf``：

    $ vim reporting.conf
    [jsondump]
    enabled = yes # no -> yes
    indent = 4
    calls = yes
    [singlefile]
    # Enable creation of report.html and/or report.pdf?
    enabled = yes # no -> yes
    # Enable creation of report.html?
    html = yes # no -> yes
    # Enable creation of report.pdf?
    pdf = yes # no -> yes
    [mongodb]
    enabled = yes # no -> yes
    host = 127.0.0.1
    port = 27017
    db = cuckoo
    store_memdump = yes 
    paginate = 100

配置``cuckoo.conf``：

    version_check = no
    machinery = virtualbox
    memory_dump = yes
    [resultserver]
    ip = 192.168.56.1
    port = 2042
