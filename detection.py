import sys

import cv2
import time
import os
import threading
from ctypes import windll
from hook import hook  # 引入新封装的类
from login import login  # 引入新封装的类
from Logger import log


class loginSystem:
    def __init__(self, db_dir):

        self.db_dir = db_dir

        self.camera = cv2.VideoCapture(0)
        self.success_count = 0
        self.lose_count = 0
        self.hook = hook()
        self.login = login(db_dir)

    def lock_screen(self):
        user32 = windll.LoadLibrary('user32.dll')
        user32.LockWorkStation()

    def process_frame(self):
        print("开始检测")
        log.info("开始检测")
        if self.success_count >= 1 or self.lose_count >= 10:
            return
        ret, frame = self.camera.read()
        if not ret:
            return False

        result = self.login.login(frame)
        if result == 0:
            self.lose_count += 1
        else:
            self.success_count += 1

        return True

    def start(self):

        # 启动程序控制
        threading.Thread(target=self.hook.start_program).start()
        while True:
            # self.hook.kill_program()
            if self.hook.status == 0:
                # 快捷键退出
                break
            if self.success_count >= 1:
                self.hook.kill_program()
                try:
                    self.hook.kill_program()
                except:
                    pass
                print("ok")
                log.info("ok")

                break

            if self.lose_count >= 120:
                try:
                    self.hook.kill_program()
                except:
                    pass
                self.lock_screen()
                print("shit")
                log.info("shit")
                break

            threading.Thread(target=self.process_frame).start()
            time.sleep(0.5)


if __name__ == "__main__":
    db_dir = "./db"
    frs = loginSystem(db_dir)
    frs.start()
