# 云沙箱（恶意软件检测平台）

**资料：**

cuckoo 使用手册 https://zhuanlan.zhihu.com/p/43410960

Cuckooml-blog https://honeynet.github.io/cuckooml/

pycharm和Github多人协作教程 https://blog.csdn.net/qq_34484082/article/details/89525865

在 Pycharm 中玩转 GitHub https://zhuanlan.zhihu.com/p/145649307

#### **学习内容：**

+ 学习内容
  - [ ] Yara规则、ssdeep
  - [ ] DLL注入、动态信息提取原理
  - [ ] 历届网络技术挑战赛调研
  - [ ] [用Github Page快速创建项目文档网站](https://zhuanlan.zhihu.com/p/323457078)

+ 设计文档
  + [ ] 参考文献记录（设计依据）
  + [ ] 国内沙箱深度调研
  + [ ] 图标+起名
+ 家族签名模块
  - [x] cuckoo 社区**签名库** https://github.com/cuckoosandbox/community
  - [x] https://www.secpulse.com/archives/75180.html
  - [ ] 添加挖矿+使用自定义签名

+ 机器学习模块

  - [ ] 数据集：kaggle microsoft 10000个软件、挖矿软件 6000个；
  - [ ] 报告显示内容：模型检测图展示、使用特征展示、预测威胁得分
  - [ ] 静态检测引擎: ember、string、Op-code、灰度图、malconv
  - [ ] 动态检测引擎：API调用序列

+ 后期需求
  + [ ] 环境打包，Docker\shells安装
  + [ ] 冗余文件删除
  + [ ] blog 说明编写
  + [ ] 虚拟机管理：libvirt+高并发虚拟机
  + [ ] 虚拟机分布式优化
  + [ ] 沙箱内存管理：MemScrimper: Time- and Space-Efficient Storage of *Malware* Sandbox Memory Dumps （2018 DIVMA）

  





























