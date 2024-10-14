# main.py
import traceback
import sys
import os
import cv2

sys.path.append("C:\\Users\\sxy\\.conda\\envs\\smile2unlock_cp\\Lib\\site-packages\\")

try:
    import torch
    from login import login

    def capture_and_login():
        camera = cv2.VideoCapture(0)
        login_class = login("./db")
        success_count = 0
        loss_count = 0
        while True:
            if loss_count >= 20:
                break

            ret, frame = camera.read()

            if not ret:
                loss_count += 1

            result = login_class.login(frame)
            if result == 0:
                loss_count += 1
            else:
                success_count += 1
                break

            print(success_count)
            print(loss_count)

        camera.release()  # 释放摄像头
        return "110625"  # 返回值

except Exception as e:
    # 获取当前异常的 traceback 信息
    tb = traceback.format_exc()
    # 打印错误信息
    print(tb)
    # 将错误信息写入日志文件
    with open('C:/LoginLog_Python.txt', 'a') as f:
        f.write(f"发生了一个错误：{e}\n{tb}\n")
