import cv2
import time
import os
import threading
import datetime
from ctypes import windll
from test import test
import util
from Logger import log

class FaceRecognitionSystem:
    def __init__(self, exe_path, db_dir, image_path):
        self.exe_path = exe_path
        self.db_dir = db_dir
        self.image_path = image_path
        self.camera = cv2.VideoCapture(0)
        self.success_count = 0
        self.lose_count = 0

    def start_program(self):
        os.system(f"start {self.exe_path}")

    def kill_program(self):
        os.system('taskkill /f /im "Gasoft_topON_TopON2.exe"')

    def lock_screen(self):
        user32 = windll.LoadLibrary('user32.dll')
        user32.LockWorkStation()

    def display_image_fullscreen(self):
        def show_image():
            img = cv2.imread(self.image_path)
            cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow("Image", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # Start a thread to display the image
        threading.Thread(target=show_image).start()

    def login(self, img_arr):
        print("开始登录")
        log.info("开始登录")
        label = test(image=img_arr, model_dir='resources/anti_spoof_models', device_id=0)
        if label == 1:
            name = util.recognize(img_arr, self.db_dir)
            if name in ['unknown_person', 'no_persons_found']:
                print("失败")
                log.info("失败")
                return 0
            else:
                log.info(f'{name},{datetime.datetime.now()},in')
                print("成功")
                log.info("成功")
                return 1
        else:
            print("假脸")
            log.info("假脸")
            return 0

    def process_frame(self):
        print("开始检测")
        log.info("开始检测")
        ret, frame = self.camera.read()
        if not ret:
            return False

        result = self.login(frame)
        if result == 0:
            self.lose_count += 1
        else:
            self.success_count += 1

        return True

    def start(self):

        self.display_image_fullscreen()
        # self.start_program()
        while True:
            if self.success_count >= 1:
                self.kill_program()
                print("ok")
                log.info("ok")
                break

            if self.lose_count >= 10:
                self.kill_program()
                self.lock_screen()
                print("shit")
                log.info("shit")
                break

            threading.Thread(target=self.process_frame).start()
            time.sleep(30)

if __name__ == "__main__":
    exe_path = "./Gasoft_topON_TopON2.exe"
    db_dir = "./db"
    image_path = "./background.png"

    frs = FaceRecognitionSystem(exe_path, db_dir, image_path)
    frs.start()
