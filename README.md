





<img src="https://obssh.obs.cn-east-3.myhuaweicloud.com/img_sxy/202406050530509.jpg" alt="myedit_ai_image_0605052902" style="zoom: 25%;" />



### 如何使用

暂时只推荐自编译

#### 1.安装必备库

```
conda install --yes --file requirements.txt
```

#### 2.打包(可选)

```
pyinstaller -w main.py
pyinstaller -w detection.py
```

请注意打包由于face_recognition模型问题会导致失败，请自行查阅方法

#### 3.使用

##### 3.1 导入数据

运行main.py 进行导入

##### 3.2 人脸识别

添加detection.py 进windows运行任务计划程序库（可能需要自行编写进入环境变量等脚本）

当触发时（开机/睡眠解锁等），会打开一张背景图片（可自行更改），然后锁定键鼠。此时后台进行扫脸，10次机会若成功，则自动解锁，按任意键关闭背景图片，否则锁定计算机。



### 可参考的部分第三方库下载

用于安装 requirements.txt 失败参考

安装 cmake

```
pip install cmake -i https://pypi.mirrors.ustc.edu.cn/simple/
```

安装 dlib

```
conda install -c https://conda.anaconda.org/conda-forge dlib  
```

安装 face_recognition

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple face_recognition
```



```Mermaid
graph TD
    A[打开录入程序] --> B[拍照]
    B --> C[输入用户名]
    C --> D[录入]
```





```flow


st=>start: 开机自动运行
op1=>operation: 强制关闭键鼠输入（TopON）
op2=>operation: 每隔5秒拍照识别
cond1=>condition: 活体检测(Silent-Face-Anti-Spoofing)
cond3=>condition: 人脸识别(face_recognition)
cond2=>condition: 检测次数超过10次？
op4=>operation: 锁定计算机
op3=>operation: 打印“成功”
e=>end: 退出

st->op1->op2->cond1
cond1(yes)->cond3
cond1(no)->cond2
cond3(yes)->op3->e
cond3(no)->cond2
cond2(no)->op2
cond2(yes)->op4->e




```







### 功能

- [x] 数据持久化

- [x] 开机自启/解锁自启

- [x] 多用户识别

- [x] 可识别打印照片/手机相册

- [x] 未识别完成强制禁用键鼠，更安全

- [x] 自定义解锁时背景图片

  

  

  

### 参考

•https://github.com/Yiqingde/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition-Opencv-Tensorflow

•[saksham-jain](https://github.com/saksham-jain/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition)[/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition (github.com)](https://github.com/saksham-jain/Lock-Unlock-Laptop-PC-Screen-Using-Face-Recognition)

•[computervisioneng](https://github.com/computervisioneng/face-attendance-system/tree/master)[/face-attendance-system (github.com)](https://github.com/computervisioneng/face-attendance-system/tree/master)

•[minivision](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[-ai/Silent-Face-Anti-Spoofing: ](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[静默活体检测（](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[） ](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)[(github.com)](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing/tree/master)