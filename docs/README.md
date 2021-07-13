```shell
                  ____        _     _       _____     _                 
                 | __ )  ___ | | __| |     |  ___|_ _| | ___ ___  _ __  
                 |  _ \ / _ \| |/ _` |_____| |_ / _` | |/ __/ _ \| '_ \ 
                 | |_) | (_) | | (_| |_____|  _| (_| | | (_| (_) | | | |
                 |____/ \___/|_|\__,_|     |_|  \__,_|_|\___\___/|_| |_|
```

<img src="pics/logo.png" align="right" width="256px" height="176px">

# 毕方智能云沙箱

毕方智能云沙箱(***Bold-Falcon***)是一个开源的自动化恶意软件分析系统。
它用于自动运行和分析文件，并收集全面的分析结果，概述恶意软件在独立操作系统中运行时所做的工作。
我们的工作是二次开发开源cuckoo沙箱，包括**更新项目结构**，**重写整个前端的用户交互**和**添加基于机器学习的检测模块**，
使恶意软件分析系统可以**思考**。

![](https://img.shields.io/badge/GitHub-Bold--Falcon-000000)

**`说明文档`** https://powerlzy.github.io/Bold-Falcon/

**`开发文档`** https://boldfalcon.readthedocs.io

#### 获取项目

```shell
git clone https://github.com/PowerLZY/Bold-Falcon
```

```shell
pip install Bold-Falcon
```

#### 开源资料

+ [cuckoo](https://github.com/cuckoosandbox/cuckoo) Cuckoo Sandbox is an automated dynamic malware analysis system
+ [cuckoo-modified](https://github.com/spender-sandbox/cuckoo-modified) Modified edition of cuckoo
+ [cuckooDroid](https://github.com/idanr1986/cuckoo-droid) CuckooDroid - Automated Android Malware Analysis with Cuckoo Sandbox.
+ [docker-cuckoo](https://github.com/blacktop/docker-cuckoo) Cuckoo Sandbox Dockerfile
+ [cuckooautoinstall](https://github.com/buguroo/cuckooautoinstall) Auto Installer Script for Cuckoo Sandbox
+ [cuckooML](https://github.com/honeynet/cuckooml) CuckooML: Machine Learning for Cuckoo Sandbox
+ [Panda-Sandbox](https://github.com/PowerLZY/Panda-Sandbox) Cuckoo python3 (Unfinished)
+ [HaboMalHunter](https://github.com/Tencent/HaboMalHunter#readme_cn) HaboMalHunter is a sub-project of Habo Malware Analysis System

#### 源码分析
+ [cuckoo技术分析全景图](https://cloud.tencent.com/developer/article/1597020)
+ [cuckoo沙箱源码分析上](https://bbs.pediy.com/thread-260038.htm)
+ [cuckoo沙箱源码分析中](https://bbs.pediy.com/thread-260087.htm)
+ [cuckoo沙箱源码分析后](https://bbs.pediy.com/thread-260252.htm)
+ [腾讯哈勃Linux沙箱源码分析上](https://zhuanlan.zhihu.com/p/54756592)
+ [腾讯哈勃Linux沙箱源码分析下](https://zhuanlan.zhihu.com/p/54756845)

#### 项目结构更新
  - [x] 整理工程目录打包lib：（common，core），Modules（辅助功能、虚拟机、处理、签名、机器学习模型检测）
  - [x] 省略\CWD目录：添加 analyzer、db、examples、Mal_sample、sample_data、storage、log等目录
  - [x] 编写[说明文档](https://powerlzy.github.io/Bold-Falcon/)和[开发文档](https://boldfalcon.readthedocs.io)

#### 后期需求

+ [ ] 环境打包，Docker\shells安装
+ [ ] 虚拟机管理：libvirt+高并发虚拟机
+ [ ] 沙箱内存管理：MemScrimper: Time- and Space-Efficient Storage of *Malware* Sandbox Memory Dumps （2018 DIVMA）
+ [ ] 搭建Elasticsearch数据库实现全局搜索
+ [ ] 搭建moloch工具流量收集和索引

#### 常见问题
+ Machine * status gurumeditation
  -  找到虚拟机安装目录下VBox.log日志文件
  -  在日志文件中找到ProcessID, ```kill - 9 ProcessID```
+ python 2/3 joblib.dump() 和 joblib.load()
  - 不同python版本的pickle.dump()和pickle.load()是可以相互转换和支持的
  - 在python3中，您应该使用较低的协议号来编写pickle数据 ```pickle.dump(your_object, your_file, protocol=2)```
+ Pytorch Cpu 导入 Gpu 训练的模型
  - `model.load(model_path, map_location='cpu')`
+ Sphinx-readthedocs 开发文档自动生成
  - `sphinx-quickstart`
  - `sphinx-apidoc -o ./source ../Bold-Falcon`
  - `python -m sphinx -T -E -b html -d _build/doctrees -D language=en . _build/html`



























