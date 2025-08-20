import sys
import os

# 您需要修改一下路径，为您的conda环境的site-packages路径和
sys.path.append("C:\\Users\\sxy\\.conda\\envs\\smile2unlock_cp\\Lib\\site-packages\\")
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)  # 如果不加这一行，当前目录会被错误认为system32

import cv2
from login import Login
from logger import log
import config


def capture_and_login():
    log.info("main is running")
    config.load_config("config.json")

    camera = cv2.VideoCapture(0)

    login_class = Login("./db")

    success_count = 0
    loss_count = 0
    while True:
        if loss_count >= 20:
            camera.release()  # 释放摄像头
            return "000000"  # 错误值
        ret, frame = camera.read()
        if not ret:
            loss_count += 1
        try:
            result = login_class.login(frame)
        except Exception as e:
            log.error(f"Login failed: {e}")
        if result == 0:
            loss_count += 1
        else:
            success_count += 1
            camera.release()  # 释放摄像头
            return config.get_config_value("password")  # 返回值


if __name__ == "__main__":
    res = capture_and_login()
    print(res)
