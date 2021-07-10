---
sort: 2
---

# 安装

## 2.1 准备主机(HOST)
## 2.2 准备客户机(Guest)
首先要在Ubuntu的vitrualbox中创建一个虚拟机，设定为windows 7 64位操作系统。

### 2.2.1 关闭防火墙、自动更新、UAC
关闭防火墙：https://jingyan.baidu.com/article/dca1fa6f0953bbf1a44052d7.html
关闭自动更新：https://jingyan.baidu.com/article/03b2f78c4ce2ad5ea337ae5b.html
关闭UAC:http://www.win7zhijia.cn/jiaocheng/win7_26850.html
### 2.2.2 安装PIL
PIL用于截屏，cuckoo生成报告中会有windows 7的截图。
首先进到C:\Python27\Scripts路径下，在此路径下安装pillow。

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
前面主机中找到的agent.py文件上传到windows 7中，建议用send anywhere比较快速。把上传成功的agent.py文件放进C:\Users[USER]\AppData\Roaming\MicroSoft\Windows\Start Menu\Programs\Startup\ 下，并把后缀名改为.pyw。其中users是指用户名。
### 2.2.4 配置系统开机自动登录
使用Administrator权限启动cmd,并依序在cmd中输入以下指令
[USERNAME]和[PASSWORD]需替换为登入的Windows user与对应的password

      >reg add "hklm\software\Microsoft\Windows NT\CurrentVersion\WinLogon" /v DefaultUserName /d [USERNAME] /t REG_SZ /f
      >reg add "hklm\software\Microsoft\Windows NT\CurrentVersion\WinLogon" /v DefaultPassword /d [PASSWORD] /t REG_SZ /f
      >reg add "hklm\software\Microsoft\Windows NT\CurrentVersion\WinLogon" /v AutoAdminLogon /d 1 /t REG_SZ /f
      >reg add "hklm\system\CurrentControlSet\Control\TerminalServer" /v AllowRemoteRPC /d 0x01 /t REG_DWORD /f
      >reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v    LocalAccountTokenFilterPolicy /d 0x01 /t REG_DWORD /f

#### 2.2.5 配置连接网络

在virtualbox中添加一块网卡，管理——主机网络管理器，按照下面信息进行设置。
![image](https://user-images.githubusercontent.com/16918550/124224460-43f95f80-db38-11eb-8a0b-f365f4f00b50.png)
设置windows 7网络，设置为Host-Only。界面名称为刚刚设置的网卡。
![image](https://user-images.githubusercontent.com/16918550/124224491-51164e80-db38-11eb-9348-66ac2cb4c6c7.png)
进入Windows 7 系统，设置win7 ip网络
![image](https://user-images.githubusercontent.com/16918550/124224523-5c697a00-db38-11eb-93fb-a5b48d6577d5.png)
检查是否配置成功，主机和客机是否能通信。
主机中操作

    $ ping 192.168.56.101

客机中操作：

    >ping 192.168.56.1
    
设置IP报文转发

这是在Ubuntu中的操作，因为win7无法上网，所以要通过主机才能访问网络，所以需要以下操作;流量转发服务：

    $ sudo vim /etc/sysctl.conf
    net.ipv4.ip_forward=1
    sudo sysctl -p /etc/systl.conf
    
使用iptables提供NAT机制
注意：其中eth0为Ubuntu中的网卡名称，需要提前查看自己Ubuntu中的网卡名称然后修改eth0

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

DNS服务

    $ sudo apt-get install -y dnsmasq
    $ sudo service dnsmasq start

在win7中查看是否有网络：

    ping www.baidu.com

#### 2.2.6 快照
要保证agent.py文件时运行状态，可以在cmd控制台启动，成功后对win7进行快照 名字取为snapshot。
#### 2.2.7 设置cuckoo配置文件
配置virtualbox.conf：

    $ vim virtualbox.conf
    machines = cuckoo1 # 指定VirtualBox中Geust OS的虛擬機名稱
    [cuckoo1] # 對應machines
    label = cuckoo1  .
    platform = windows
    ip = 192.168.56.101 # 指定VirtualBox中Geust OS的IP位置
    snapshot =snapshot

配置reporting.conf：

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

配置cuckoo.conf：

    version_check = no
    machinery = virtualbox
    memory_dump = yes
    [resultserver]
    ip = 192.168.56.1
    port = 2042
    
