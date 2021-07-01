---
sort: 2
---

# 安装

## 安装Host

### 安装必需的软件包和库

#### 安装Python库(在基于Ubuntu/Debian的发行版上)
Cuckoo主机组件完全用Python编写，因此需要安装适当版本的Python。在这一点上，我们只是全力支持Python 2.7。我们不支持Python和Python3的旧版本(尽管Python3支持在我们的Todo列表中是低优先级的)。
要使Cuckoo正确安装和运行，需要来自APT存储库的以下软件包：

    $ sudo apt-get install python python-pip python-dev libffi-dev libssl-dev
    $ sudo apt-get install python-virtualenv python-setuptools
    $ sudo apt-get install libjpeg-dev zlib1g-dev swig

为了使用基于Django的Web接口，需要使用MongoDB：
   
    $ sudo apt-get install mongodb
为了将PostgreSQL用作数据库(我们的建议)，还必须安装PostgreSQL：

    $ sudo apt-get install postgresql libpq-dev
  
如果要使用KVM作为机器模块，则必须安装KVM：
  
    $ sudo apt-get install qemu-kvm libvirt-bin ubuntu-vm-builder bridge-utils python-libvirt
如果要使用XenServer，则必须安装XenAPIPython包：
  
    $ sudo pip install XenAPI
#### 安装Python库(在MacOSX上)

这与Ubuntu/Debian上的安装基本相同，只不过我们将使用brew包裹经理。按以下方式安装所有必需的依赖项(此列表为WIP)：

    $ brew install libmagic cairo pango openssl
此外，您还希望公开标准GCC/Clang包含目录中的OpenSSL头文件，以便yara-python可以成功编译。这是可以做到的如下:

    $ cd /usr/local/include
    $ ln -s ../opt/openssl/include/openssl .

#### 安装Python库(在Windows 7上)

#### 虚拟化软件
假设您决定选择VirtualBox，则可以在官方下载页面。请在您的UbuntuLTS计算机上找到安装VirtualBox最新版本的命令。注意，Cuckoo支持VirtualBox 4.3、5.0、5.1和5.2：

    $ echo deb http://download.virtualbox.org/virtualbox/debian xenial contrib | sudo tee -a /etc/apt/sources.list.d/virtualbox.list
    $ wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -
    $ sudo apt-get update
    $ sudo apt-get install virtualbox-5.2
####  安装TCPdump

为了转储恶意软件在执行过程中执行的网络活动，您需要一个适当配置的网络嗅探器来捕获流量并将其转储到文件中。

默认情况下布谷鸟采取TCPdump，著名的开源解决方案。

将其安装在Ubuntu上：

    $ sudo apt-get install tcpdump apparmor-utils
    $ sudo aa-disable /usr/sbin/tcpdump
注意，AppArmor配置文件禁用(aa-disable命令)仅在使用默认值时才是必需的。CWD否则，目录作为AppArmor将阻止实际PCAP文件的创建(请参见拒绝tcpdump的权限).

对于禁用AppArmor的Linux平台(例如Debian)，下面的命令就足以安装TCPdump:

    $ sudo apt-get install tcpdump
TCPdump需要根权限，但是由于不希望Cuckoo作为root运行，所以必须将特定的Linux功能设置为二进制文件：

    $ sudo groupadd pcap
    $ sudo usermod -a -G pcap cuckoo
    $ sudo chgrp pcap /usr/sbin/tcpdump
    $ sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
您可以使用以下方法验证最后一个命令的结果：

    $ getcap /usr/sbin/tcpdump
    /usr/sbin/tcpdump = cap_net_admin,cap_net_raw+eip
如果你没有套帽安装后，您可以使用：

    $ sudo apt-get install libcap2-bin
或其他(不建议)做：

    $ sudo chmod +s /usr/sbin/tcpdump
#### 安装M2Crypto
目前M2Crypto只有在下列情况下才支持库大口已经安装好了。在Ubuntu/Debian类系统上，可以这样做：

    $ sudo apt-get install swig
如果SWIG是否存在于可安装的系统上？M2Crypto详情如下：

    $ sudo pip install m2crypto==0.24.0
#### 安装guacd
guacd是一个可选服务，它为RDP、VNC和SSH提供转换层，用于Cuckoo Web接口中的远程控制功能。

没有它，遥控器就无法工作。版本0.9.9和更高版本将有效，但我们建议安装最新版本。在Ubuntu17.04机器上，下面的命令将安装版本0.9.9-2:

    $ sudo apt install libguac-client-rdp0 libguac-client-vnc0 libguac-client-ssh0 guacd
如果只需要RDP支持，则可以跳过安装libguac-client-vnc0和libguac-client-ssh0包裹。

如果您使用的是旧版本或只想使用最新版本(我们的建议)，下面将生成最新版本(0.9.14)来源：

    $ sudo apt -y install libcairo2-dev libjpeg-turbo8-dev libpng-dev libossp-uuid-dev libfreerdp-dev
    $ mkdir /tmp/guac-build && cd /tmp/guac-build
    $ wget https://www.apache.org/dist/guacamole/0.9.14/source/guacamole-server-0.9.14.tar.gz
    $ tar xvf guacamole-server-0.9.14.tar.gz && cd guacamole-server-0.9.14
    $ ./configure --with-init-dir=/etc/init.d
    $ make && sudo make install && cd ..
    $ sudo ldconfig
    $ sudo /etc/init.d/guacd start
 
 
### 安装cuckoo
#### 创建用户
您可以从自己的用户中运行Cuckoo，也可以创建一个专门用于沙箱设置的新用户。确保运行Cuckoo的用户与创建和运行虚拟机的用户相同(至少在VirtualBox中是这样)，否则Cuckoo将无法识别和启动这些虚拟机。

创建一个新用户：

    $ sudo adduser cuckoo
如果使用VirtualBox，请确保新用户属于“vboxuser”组(或用于运行VirtualBox的组)：

    $ sudo usermod -a -G vboxusers cuckoo
如果您正在使用KVM或任何其他基于libvirt的模块，请确保新用户属于“libvirtd”组(或者您的Linux发行版用于运行libvirt的组)：

    $ sudo usermod -a -G libvirtd cuckoo
 
#### 安装布谷鸟
    $ sudo pip install -U pip setuptools
    $ sudo pip install -U cuckoo
 
尽管如此，全球在您的操作系统中安装Cuckoo大部分都很好，我们极力推荐将布谷鸟安装在virtualenv，大致如下：

    $ virtualenv venv
    $ . venv/bin/activate
    (venv)$ pip install -U pip setuptools
    (venv)$ pip install -U cuckoo

使用virtualenv:

 - 布谷鸟的依赖可能并不完全是最新的，而是一个已知的工作正确的版本。
 - 由于版本要求不兼容，您的系统上安装的其他软件的依赖性可能与Cuckoo所要求的软件相冲突(是的，当Cuckoo支持最新版本时，这也是可能的，因为其他软件可能被固定在旧版本上)。
 - 使用Virtualenv允许非根用户安装额外的软件包或在以后的某个时候升级Cuckoo。
 - 简单地说，Virtualenv被认为是一种最佳实践。
 
 #### 从文件中安装cuckoo
 
 下载布谷鸟软件包的硬拷贝并安装离线，您可以使用缓存副本和/或将来拥有当前Cuckoo版本的备份副本来设置Cuckoo。我们还提供了在我们的网站上下载这样一个tarball的选项。

手动获取布谷鸟的tarball及其所有依赖项的步骤如下：

    $ pip download cuckoo
你最终会得到一个文件Cuckoo-2.0.0.tar.gz(或更高的数目，取决于最新发布的稳定版本)以及它的所有依赖项(例如，alembic-0.8.8.tar.gz).

安装Cuckoo的确切版本可能会像您熟悉的那样，使用pip直接，除了现在使用tarball的文件名：

    $ pip install Cuckoo-2.0.0.tar.gz
在没有互联网连接的系统上，$ pip download cuckoo命令可用于获取所有所需的依赖项，因此理论上应该能够使用这些文件完全脱机安装Cuckoo，即通过执行以下内容：

    $ pip install *.tar.gz
 
 ### cuckoo工作目录
 
 新版本2.0.0。

一个新概念是Cuckoo Working Directory。从这一点开始，所有可配置的组件、生成的数据和Cuckoo的结果都将存储在这个目录中。这些文件包括但不限于以下内容：

 - Configuration
 - Cuckoo Signatures
 - Cuckoo Analyzer
 - Cuckoo Agent
 - Yara rules
 - Cuckoo Storage (where analysis results go)
 - 还有更多..。
与Cuckoo使用的遗留方法相比，CuckoWorkDirectory具有一些优点。接下来我们将研究Cuckoo Working Directory (CWD(从现在起)每天克服各种障碍。
 #### 配置
 如果您曾经将您的布谷鸟安装程序更新到更高的版本，您就会遇到这样的问题：您必须对您的配置进行备份，更新您的Cuckoo实例，或者恢复您的配置，或者完全重新应用它。

引入CWD我们已经摆脱了这个更新的噩梦。

你第一次跑Cuckoo a CWD结帐将自动为您创建，大致如下所示：
    $ cuckoo -d

            _       _                   _             _              _            _
            /\ \     /\_\               /\ \           /\_\           /\ \         /\ \
            /  \ \   / / /         _    /  \ \         / / /  _       /  \ \       /  \ \
            / /\ \ \  \ \ \__      /\_\ / /\ \ \       / / /  /\_\    / /\ \ \     / /\ \ \
        / / /\ \ \  \ \___\    / / // / /\ \ \     / / /__/ / /   / / /\ \ \   / / /\ \ \
        / / /  \ \_\  \__  /   / / // / /  \ \_\   / /\_____/ /   / / /  \ \_\ / / /  \ \_\
        / / /    \/_/  / / /   / / // / /    \/_/  / /\_______/   / / /   / / // / /   / / /
        / / /          / / /   / / // / /          / / /\ \ \     / / /   / / // / /   / / /
    / / /________  / / /___/ / // / /________  / / /  \ \ \   / / /___/ / // / /___/ / /
    / / /_________\/ / /____\/ // / /_________\/ / /    \ \ \ / / /____\/ // / /____\/ /
    \/____________/\/_________/ \/____________/\/_/      \_\_\\/_________/ \/_________/

    Cuckoo Sandbox 2.0.0
    www.cuckoosandbox.org
    Copyright (c) 2010-2017

    =======================================================================
        Welcome to Cuckoo Sandbox, this appears to be your first run!
        We will now set you up with our default configuration.
        You will be able to modify the configuration to your likings
        by exploring the /home/cuckoo/.cuckoo directory.

        Among other configurable things of most interest is the
        new location for your Cuckoo configuration:
                /home/cuckoo/.cuckoo/conf
    =======================================================================

    Cuckoo has finished setting up the default configuration.
    Please modify the default settings where required and
    start Cuckoo again (by running `cuckoo` or `cuckoo -d`).
正如信息消息所指出的，您现在可以找到CWD在…/home/cuckoo/.cuckoo因为它默认为~/.cuckoo。您所知道的所有配置文件都可以在$CWD/conf目录。也就是说，$CWD/conf/cuckoo.conf, $CWD/conf/virtualbox.conf等

现在因为CWD目录本身并不是cuckoo的一部分，即git存储库，或者作为最新版本的一部分，可以升级cuckoo，而不必访问CWD。(当然，如果安装了需要更新配置的更新，那么Cuckoo将引导用户完成更新，而不是覆盖配置文件本身)。
#### CWD路径
即使CWD默认为~/.cuckoo此路径是完全可配置的。下面列出了布谷鸟确定CWD.

 - 通过--cwd命令行选项(例如，--cwd ~/.cuckoo).
 - 通过CUCKOO环境变量(例如，export CUCKOO=~/.cuckoo).
 - 通过CUCKOO_CWD环境变量
 - 如果当前目录是CWD(例如，cd ~/.cuckoo假设CWD已在该目录中创建)。
 - 通过默认情况下，~/.cuckoo.
通过使用替代CWD它是一条路可以使用相同的Cuckoo设置运行具有不同配置的多个Cuckoo实例。如果出于某种原因，一个需要两个或三个独立的布谷鸟设置，例如，在您希望并行运行Windows分析和Android分析的情况下，那么每次更新时不必一个一个地升级每个实例，这无疑是一个很大的进步。

下面的一些示例演示如何配置CWD.

    # Places the CWD in /opt/cuckoo. Note that Cuckoo will normally create the
    # CWD itself, but in order to create a directory in /opt root capabilities
    # are usually required.
    $ sudo mkdir /opt/cuckoo
    $ sudo chown cuckoo:cuckoo /opt/cuckoo
    $ cuckoo --cwd /opt/cuckoo

    # You could place this line in your .bashrc, for example.
    $ export CUCKOO=/opt/cuckoo
    $ cuckoo
多个布谷鸟装置的实验现在就像创建多个布谷鸟一样简单。CWD并相应地配置它们。
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
