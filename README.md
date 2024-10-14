









<p align="center">
  <img width="18%" align="center" src="https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406050530509.jpg" alt="logo">
</p>
  <h1 align="center">
  Smile2Unlock(cp凭据分支)
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

- [x] 数据持久化

- [x] 多用户识别
  
  
  
  
  
  



在windows登录界面选择本凭据，直接登录，便会启动程序，进行人脸识别，若10秒内未出现预设人脸，则退回，使用密码登录。





### 如何使用

本程序没有release打包（因为打包出错），需要手动git clone本项目，并按以下步骤安装必备库

### 1.安装

由于环境错综复杂，本项目也不提供requirements.txt 

请注意，本项目强烈推荐使用conda环境，但不要使用conda install,只使用pip install，否则将在凭据生成后产生引用问题

推荐按照以下步骤使用

1.创建conda环境

```
conda create --name smile2unlock_cp python=3.11.9
```

2.安装 cmake（可能不需要指定镜像）

```
pip install cmake==3.29.3 -i https://pypi.tuna.tsinghua.edu.cn/simple 
```

3.安装 dlib  推荐使用pip安装轮子文件

```
https://blog.csdn.net/AI_dataloads/article/details/134063212
```

4.安装 face_recognition

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple face_recognition
```

5.安装其他必要库

```
pip install opencv-contrib-python==4.9.0.80 pynput screeninfo numpy==1.26.4 torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2 face_recognition -i https://pypi.tuna.tsinghua.edu.cn/simple

```

总结：该版本测试成功，仅供参考：

```
python=3.11.9		创建conda指定版本，推荐该版本
cmake=3.29.3		最新版皆可，无严格版本限制
dlib=19.24.4		特殊的，只有此库使用conda安装
face-recognition=1.3.0
opencv-contrib-python=4.9.0.80
pynput=1.7.7
screeninfo=0.8.1
torch=2.2.2
torchaudio=2.2.2
torchvision=0.17.2
numpy=1.26.4
```

### 2. 导入至系统凭据

1.在进入conda环境后，运行 python generate_db.py 在gui界面录入,

2.随后在config.json中，修改您的password.

3.在main.py中，修改您的conda路径和项目路径

4.从visual studio中，修改您的引用库

参考 [C++调用python文件]https://blog.csdn.net/larryysw/article/details/106215035)  以及[C++调用Python第2讲 _哔哩哔哩_](https://www.bilibili.com/video/BV1Ze411h7vA/?spm_id_from=333.788.videopod.sections&vd_source=df034c933ea08326f3a58a38fa1c7fce)

5.修改cpp->Source Files->CSampleCredential.cpp->GetSerialization中的项目路径

6.生成dll，移动至system32,运行cpp根目录下的register.reg



### 3. 交流

笔者并不期望读者仅根据以上文字便能成功注册凭证系统，如果您有任何不理解的地方，请加入QQ群：702645243



### 4. 流程图

1.generate_db.py

![image-20240610202326514](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406102023562.png)



2.detection.py

![image-20240610202418306](https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406102024455.png)





### 参考

•https://github.com/Yiqingde/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition-Opencv-Tensorflow

•[saksham-jain](https://github.com/saksham-jain/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition)[/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition (github.com)](https://github.com/saksham-jain/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition)

•[computervisioneng](https://github.com/computervisioneng/face-attendance-system/tree/master)[/face-attendance-system (github.com)](https://github.com/computervisioneng/face-attendance-system/tree/master)

•[minivision](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[-ai/Silent-Face-Anti-Spoofing: ](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[静默活体检测（](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[） ](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[(github.com)](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)

[探秘Windows认证新境界——windows-Credential-Provider-library-CSDN博客](https://blog.csdn.net/gitblog_00069/article/details/139403431)

[Credential Provider_credential provider 眼睛-CSDN博客](https://blog.csdn.net/patdz/article/details/7522195)

[微软 Credential Providers 详解-CSDN博客](https://blog.csdn.net/lionzl/article/details/103279954)

[credential Provider 简易改写攻略_csamplecredential-CSDN博客](https://blog.csdn.net/lionzl/article/details/103279845?spm=1001.2014.3001.5502)
