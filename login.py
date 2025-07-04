import datetime
from src.fake_face_test import test
from src import util
from logger import log


class Login:
    def __init__(self, db_dir):
        self.db_dir = db_dir

    def login(self, img_arr):
        print("开始登录")
        log.info("开始登录")
        label = test(
            image=img_arr, model_dir="resources/anti_spoof_models", device_id=0
        )
        if label == 1:
            name = util.recognize(img_arr, self.db_dir)
            if name in ["unknown_person", "no_persons_found"]:
                log.info("失败")
                return 0
            else:
                log.info(f"{name},{datetime.datetime.now()},in")
                log.info("成功")
                return 1
        else:
            print("假脸")
            log.info("假脸")
            return 0
