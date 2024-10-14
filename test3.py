# capture_image.py

import sys
import os
import cv2
import datetime

# 获取当前工作目录
new_path = "D:\\py_project\\Smile2Unlock"

# # 更改当前工作目录
# os.chdir(new_path)

current_path = os.getcwd()
print(f"当前工作目录是: {current_path}")
# 将 b.py 的目录添加到模块搜索路径中
sys.path.append(new_path)
def capture_image():


    def log_event():
        with open('C:/LoginLog_Python.txt', 'a') as f:
            f.write(f'Login attempt on: {datetime.datetime.now()},{current_path}\n')

    log_event()
    try:
        import Logger
        Logger.log.info("5capture_image")
    except Exception as e:
        # print(f"发生了一个错误：{e}")
        with open('C:/LoginLog_Python.txt', 'a') as f:
            f.write("shit")
            f.write(f"发生了一个错误：{e}")
        # return True

    # 打开摄像头
    import time

    time.sleep(5)  # 程序会暂停执行 10 秒

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return False

    # 读取一帧
    ret, frame = cap.read()
    if not ret:
        print("无法捕捉图像")
        return False

    # 保存图片到当前目录
    image_path = os.path.join(os.getcwd(), "captured_image.jpg")
    cv2.imwrite(image_path, frame)

    # 释放摄像头资源
    cap.release()

    print(f"图片已保存到: {image_path}")
    return True

if __name__ == "__main__":
    capture_image()
