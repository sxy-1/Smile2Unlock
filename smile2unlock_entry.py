import sys
import threading
import time
from ctypes import windll

import cv2

import src.config as config
from src import util
from src.auto_relock import RelockWatcher
from src.hook import Hook
from src.logger import log
from src.login import Login


def _acquire_single_instance_mutex():
    """Create a named Windows mutex to prevent multiple instances from running simultaneously.
    Returns the mutex handle (must be kept alive). Returns None if another instance is already running.
    """
    mutex = windll.kernel32.CreateMutexW(None, True, "Smile2UnlockMutex")
    if windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        return None
    return mutex


class LoginSystem:
    def __init__(self, db_dir):
        log.info("smile2unlock_entry")
        self.db_dir = db_dir

        self.camera = cv2.VideoCapture(0)
        self.success_count = 0
        self.hook = Hook()
        self.login = Login(db_dir)

    def lock_screen(self):
        user32 = windll.LoadLibrary("user32.dll")
        user32.LockWorkStation()

    def process_frame(self):
        print("开始检测")
        log.info("开始检测")

        ret, frame = self.camera.read()
        if not ret:
            return False

        # 去除黑边
        frame = util.remove_black_borders(frame)

        result = self.login.login(frame)
        if result != 0:
            self.success_count += 1

        return True

    def _kill_and_lock(self):
        try:
            self.hook.kill_program()
        except Exception:
            pass
        self.lock_screen()

    def start(self):
        check_interval = config.get_config_value("check_interval") or 0.5
        total_duration = config.get_config_value("total_duration")
        if total_duration is None:
            total_duration = 60.0

        # 启动程序控制
        threading.Thread(target=self.hook.start_program).start()

        # total_duration == 0: 只检测一次
        if total_duration == 0:
            self.process_frame()
            if self.success_count >= 1:
                self.hook.kill_program()
                log.info("ok (single shot)")
            else:
                log.info("single shot failed, locking screen")
                self._kill_and_lock()
            return

        # total_duration < 0: 无限检测
        # total_duration > 0: 检测指定秒数后锁屏
        start_time = time.time()

        while True:
            if self.hook.status == 0:
                log.info("hook.status==0,try to break")
                break

            if self.success_count >= 1:
                self.hook.kill_program()
                log.info("success_count>=1,try to kill hook")
                try:
                    self.hook.kill_program()
                except Exception:
                    pass
                log.info("ok")
                print("ok")
                break

            if total_duration > 0 and (time.time() - start_time) >= total_duration:
                log.info(f"total_duration={total_duration}s reached, locking screen")
                self._kill_and_lock()
                break

            threading.Thread(target=self.process_frame).start()
            time.sleep(check_interval)


if __name__ == "__main__":
    _mutex = _acquire_single_instance_mutex()
    if _mutex is None:
        print("另一个 Smile2Unlock 实例已在运行，退出。")
        sys.exit(0)

    config.load_config(config.CONFIG_FILE)

    db_dir = "./db"
    timeout = config.get_config_value("relock_timeout")
    hotkey = config.get_config_value("lock_hotkey") or ""
    use_watcher = timeout is not None and timeout >= 0

    while True:
        frs = LoginSystem(db_dir)
        frs.start()
        frs.camera.release()  # start() 返回后摄像头不再需要，显式释放确保循环时可重新打开

        # 未成功解锁（超时锁屏路径），直接退出
        if frs.success_count < 1:
            break

        # 成功解锁但不启动 watcher，直接退出
        if not use_watcher:
            break

        watcher = RelockWatcher(timeout=float(timeout), hotkey=hotkey)
        watcher.start()
        watcher.wait()

        if watcher.relocked:
            # 真锁已触发，进程退出，smile2unlock 由外部自启机制重新拉起
            break
        # 快捷键触发：loop → 重新创建 LoginSystem，展示白屏
