# 毕方云沙箱（恶意软件检测平台）

#### 资料
+ https://bbs.pediy.com/thread-260252.htm
+ https://cuckoo.sh/docs/

#### 项目结构更新
 - [x] 整理工程目录打包lib：（common，core），Modules（辅助功能、虚拟机、处理、签名、机器学习模型检测）
 - [x] 省略\CWD目录：添加 analyzer、db、examples、Mal_sample、sample_data、storage、log等目录
#### 主要更新内容

+ 学习内容
  - [x] Yara规则、ssdeep
  - [x] DLL注入、动态信息提取原理
  - [x] 历届网络技术挑战赛调研
  - [x] [用Github Page快速创建项目文档网站](https://zhuanlan.zhihu.com/p/323457078)
  - [ ] 动态牌子
  - [ ] pypi上传模块，pip安装
  - [ ] requirements.txt 整理
  - [ ] Frog:create an image and add an image and a host to the Fog server

+ 设计文档
  + [x] 参考文献记录（设计依据）
  + [x] 国内沙箱深度调研
  + [ ] 图标+起名

+ 家族签名模块
  - [x] cuckoo 社区签名库 https://github.com/cuckoosandbox/community
  - [x] https://www.secpulse.com/archives/75180.html
  - [ ] 添加挖矿+使用自定义签名

+ 机器学习模块
  - [x] 数据集：kaggle microsoft 10000个软件、挖矿软件 6000个；
  - [ ] 报告显示内容：模型检测图展示、使用特征展示、预测威胁得分；
  - [x] 静态检测引擎: ember、string、Op-code、灰度图、malconv；
  - [x] 动态检测引擎：API调用序列；
  - [x] 家族聚类（hdbscan等）；
  - [ ] 定义基类Ml、loader等；
  - [ ] 定义模型命名规则
  - [ ] 添加Smaple——malware，200个json report样本；**gist.github.com**

+ 后期需求
  + [ ] 环境打包，Docker\shells安装
  + [ ] blog解析文档编写
  + [ ] 虚拟机管理：libvirt+高并发虚拟机
  + [ ] 沙箱内存管理：MemScrimper: Time- and Space-Efficient Storage of *Malware* Sandbox Memory Dumps （2018 DIVMA）
  + [ ] 3.3.5 REST API(Cuckoo docs) wsgi应用程序

#### 文档结构

+ 说明
+ 安装
+ 使用
+ 开发文档
+ 使用案例





























