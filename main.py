# main.py

import os
import sys

# 您需要修改一下两个路劲，分别为您的conda环境的site-packages路径和smile2unlock_cp的路径
sys.path.append("C:\\Users\\sxy\\.conda\\envs\\smile2unlock_cp\\Lib\\site-packages\\")
sys.path.append("D:\\py_project\\smile2unlock_cp\\")


import cv2
from login import login
from Logger import log
import config




def capture_and_login():
    log.info("main is running")
    config.load_config('config.json')
    camera = cv2.VideoCapture(0)
    login_class = login("./db")
    success_count = 0
    loss_count = 0
    while True:
        if loss_count >= 20:
            camera.release()  # 释放摄像头
            return "000000"  # 错误值
        ret, frame = camera.read()

        if not ret:
            loss_count += 1
        result = login_class.login(frame)
        if result == 0:
            loss_count += 1
        else:
            success_count += 1
            camera.release()  # 释放摄像头
            return config.get_config_value("password")  # 返回值

if __name__ == '__main__':
    capture_and_login()