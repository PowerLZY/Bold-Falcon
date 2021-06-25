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
