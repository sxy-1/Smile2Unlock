









<p align="center">
  <img width="18%" align="center" src="https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406050530509.jpg" alt="logo">
</p>
  <h1 align="center">
  Smile2Unlock
</h1>
<p align="center">
  帮助无"windows Hello"摄像头的电脑，在开机/解锁时，进行人脸识别
</p>
<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win-blue?color=#4ec820" alt="Platform Win"/>
  </a>
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
    </a>
    <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/version-1.0.0-blue?color=#4ec820" alt="v1.0.0"/>
  </a>
</p>

### 支持

- [x] 人脸识别

- [x] 侧脸识别

- [x] 活体检测（防止照片解锁）

- [x] 备用解锁方式（可关闭）

- [x] 数据持久化

- [x] 开机自启/解锁自启

- [x] 多用户识别
  
  
  
  
  
  

<img src="https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406101920647.png" alt="image-20240610192029932" style="zoom: 33%;" />

运行时，键鼠将禁止使用（防止任务管理器退出），必须在一分钟内人脸识别成功（每0.5秒一次检测，共120次），自动解锁，否则锁定计算机。

上图为透明度为0.5时，显示屏状态，透明度可调。

此外，本程序在人脸识别时并不会展示当前人脸，正如上图，您可以根据需求自行修改代码。





### 如何使用

本程序没有release打包（因为打包出错），需要手动git clone本项目，并按以下步骤安装必备库

### 1.安装

由于环境错综复杂，本项目也不提供requirements.txt 

推荐按照以下步骤使用

1.创建conda环境

```
conda create -n Smile2Unlock_last
```

2.安装 cmake（可能不需要指定镜像）

```
pip install cmake==3.29.3 -i https://pypi.mirrors.ustc.edu.cn/simple/
```

3.安装 dlib 

```
conda install -c https://conda.anaconda.org/conda-forge dlib 
```

4.安装 face_recognition

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple face_recognition
```

5.安装其他必要库

```
pip install opencv-contrib-python==4.9.0.80
pip install pynput 
pip install screeninfo
```

该版本测试成功，仅供参考：

```
python=3.11.9		创建conda指定版本
cmake=3.29.3
dlib=19.24.4		特殊的，只有此库使用conda安装
face-recognition=1.3.0
opencv-contrib-python=4.9.0.80
pynput=1.7.7
screeninfo=0.8.1
```

### 2. 导入自身人脸数据

在进入conda环境后，运行 python generate_db.py 在gui界面录入即可

本流程仅需一次，如改人脸需要删除，在db文件夹下直接删除即可。



### 3. 尝试启动

编辑detetion.bat 文件

 可以直接运行，查看效果

### 4. 加入开机自启

参考[windows锁屏时启动某个程序（使用win任务计划库）_windows 计划任务 用户登录时运行 锁屏状态执行吗-CSDN博客](https://blog.csdn.net/weixin_45285564/article/details/133299981)

![](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406102010831.png)

值得注意的是 请务必指定bat文件夹路径（在“起始于”中填写文件夹）

![image-20240610200531469](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406102005548.png)

完成后，您可以在右侧运行中尝试运行。



### 5. 其他

您可以在config.json中启动特殊按键，1为启动（默认），0为关闭，当开启时，你可以按下“分钟的十分位”来强制关闭人脸识别，比如“20:13”可以按数字“1”。

您可以在config,json中设置透明度，1为完全透明，0为完全不透明，默认0.5



### 6.打包

 本程序曾尝试pyinstaller打包为exe，但失败，以下为部分解决办法，如果您成功打包，欢迎与我联系。



#### 1

```
shape_predictor_68_face_landmarks.dat
[24320] Failed to execute script 'main' due to unhandled exception!
```

请手动在  **_internal**  文件夹中添加 face_recognition_models 文件夹（在源conda的lib库中）

#### 2.
```
FAILED: ReadProtoFromTextFile(param_file, param). Failed to parse NetParameter file: ./resources/detection_model/deploy.prototxt in function 'cv::dnn::ReadNetParamsFromTextFileOrDie'
```

复制resource文件夹至根目录



#### 3. 无法解决的报错

Could not locate cudnn_ops_infer64_8.dll. Please make sure it is in your library path!

无法继续打包

### 项目结构

    |----config.json			配置json，自动生成
    |----config.py				配置程序
    |----db\					人脸数据库
    |----detection.bat			最后导入计划库的可执行程序
    |----detection.py			检测程序，项目核心程序
    |----generate_db.py			录入程序，项目核心程序
    |----hook.py				使用tk生成透明白布，并禁用键鼠	
    |----log\ 					日志文件
    |----Logger.py				生成日志程序
    |----login.py				登录程序
    |----README.md				README
    |----resources\				第三方人脸识别资源文件
    |----src\					第三方人脸识别资源文件
    |----test.py				第三方人脸识别资源文件
    |----train.py				第三方人脸识别资源文件
    |----util.py				第三方人脸识别资源文件

### 流程图

1.generate_db.py

![image-20240610202326514](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406102023562.png)



2.detection.py

![image-20240610202418306](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406102024455.png)





### 参考

•https://github.com/Yiqingde/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition-Opencv-Tensorflow

•[saksham-jain](https://github.com/saksham-jain/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition)[/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition (github.com)](https://github.com/saksham-jain/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition)

•[computervisioneng](https://github.com/computervisioneng/face-attendance-system/tree/master)[/face-attendance-system (github.com)](https://github.com/computervisioneng/face-attendance-system/tree/master)

•[minivision](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[-ai/Silent-Face-Anti-Spoofing: ](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[静默活体检测（](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[） ](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[(github.com)](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)