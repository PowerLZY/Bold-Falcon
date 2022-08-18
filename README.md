```shell
                  ____        _     _       _____     _                 
                 | __ )  ___ | | __| |     |  ___|_ _| | ___ ___  _ __  
                 |  _ \ / _ \| |/ _` |_____| |_ / _` | |/ __/ _ \| '_ \ 
                 | |_) | (_) | | (_| |_____|  _| (_| | | (_| (_) | | | |
                 |____/ \___/|_|\__,_|     |_|  \__,_|_|\___\___/|_| |_|
```

<img src="resources/test.png" align="right" width="256px" height="176px">

# 毕方智能云沙箱

毕方智能云沙箱(***Bold-Falcon***)是一个开源的自动化恶意软件分析系统。它用于自动运行和分析文件，并收集全面的分析结果，概述恶意软件在独立操作系统中运行时所做的工作。我们的工作是二次开发开源cuckoo沙箱，包括**更新项目结构**，**重写整个前端的用户交互**和**添加基于机器学习的检测模块**，
使恶意软件分析系统可以**思考**。

![](https://img.shields.io/badge/GitHub-Bold--Falcon-000000)

**`说明文档`** https://powerlzy.github.io/Bold-Falcon/

**`开发文档`** https://boldfalcon.readthedocs.io

#### 下载源码

```shell
$ git clone https://github.com/PowerLZY/Bold-Falcon
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
+ [cuckoosegg](https://github.com/chrisante/cuckoosegg)

#### 源码分析
+ [cuckoo技术分析全景图](https://cloud.tencent.com/developer/article/1597020)
+ [cuckoo沙箱源码分析上](https://bbs.pediy.com/thread-260038.htm)
+ [cuckoo沙箱源码分析中](https://bbs.pediy.com/thread-260087.htm)
+ [cuckoo沙箱源码分析后](https://bbs.pediy.com/thread-260252.htm)
+ [腾讯哈勃Linux沙箱源码分析上](https://zhuanlan.zhihu.com/p/54756592)
+ [腾讯哈勃Linux沙箱源码分析下](https://zhuanlan.zhihu.com/p/54756845)

### 开源样本

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
-   [chocolatey](https://chocolatey.org/)

#### 项目结构更新
  - [x] 整理工程目录打包lib：（common，core），Modules（辅助功能、虚拟机、处理、签名、机器学习模型检测）
  - [x] 省略\CWD目录：添加 analyzer、db、examples、Mal_sample、sample_data、storage、log等目录

#### 最近更新

+ 学习内容
  - [x] [预训练TF-IDF模型加载优化 100s -> 2s](https://thiagomarzagao.com/2015/12/08/saving-TfidfVectorizer-without-pickles/)
  - [ ] Linux沙箱及检测方案
  - [ ] ATT&CK Navigator layer for Cuckoo's TTPs.pyattack

+ 设计文档
  + [x] 参考文献记录（设计依据）
  + [x] 国内沙箱深度调研
  + [x] 图标+起名

+ 家族签名模块
  - [x] [cuckoo 社区签名库](https://github.com/cuckoosandbox/community)
  - [x] [cuckoo的行为签名](https://www.secpulse.com/archives/75180.html)
  - [ ] 添加挖矿+使用自定义签名
+ 机器学习模块
  - [x] 数据集：kaggle microsoft 10000个软件、挖矿软件 6000个；
  - [x] 报告显示内容：模型检测图展示、使用特征展示、预测威胁得分；
  - [x] 静态检测引擎：string、malconv；
  - [x] 动态检测引擎：API调用序列；
  - [x] 定义基类Dectection、Instance等；
  - [x] 添加Smaple——malware，200个json report样本；
  - [ ] 添加 《Dynamic Malware Analysis with Feature Engineering and Feature Learning》 动态分析检测模型
+ 后期需求
  + [ ] 环境打包，Docker\shells安装
  + [ ] blog解析文档编写
  + [ ] 虚拟机管理：libvirt+高并发虚拟机
  + [ ] 沙箱内存管理：MemScrimper: Time- and Space-Efficient Storage of *Malware* Sandbox Memory Dumps （2018 DIVMA）
  + [ ] 3.3.5 REST API(Cuckoo docs) wsgi应用程序
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



























