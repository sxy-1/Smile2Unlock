# https://blog.csdn.net/gduuyu8/article/details/126525014
import sys
import time
from datetime import datetime
from tkinter import Tk
from pynput import keyboard
from screeninfo import get_monitors
import config


class hook:
    def __init__(self):
        self.status = 1
        self.roots = []
        self.keyboard_listener = None

    def on_closing(self):
        # 这个方法在窗口关闭时调用
        # 由于我们使用 overrideredirect(True)，用户不能直接关闭窗口，
        # 所以这个方法可能不会被调用。但保留它以备将来需要。
        pass

    def on_press(self, key):
        try:
            print(f'字母 {key.char} 被按下了')
            if self.unlock_by_special_key(key.char):
                self.kill_program()
                return False  # 停止监听
        except AttributeError:
            print(f'特殊的键 {key} 被按下了')
        return True

    def start_keyboard_listener(self):
        listener = keyboard.Listener(on_press=self.on_press, suppress=True)
        listener.start()
        return listener

    def start_program(self):
        # print("程序将在 3 秒后启动...")
        # time.sleep(3)
        monitors = get_monitors()
        self.roots = []

        for monitor in monitors:
            root = Tk()
            root.overrideredirect(True)
            v = 1-0.99*(config.get_config_value("transparency"))
            root.attributes("-alpha", v)
            root.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
            root.attributes("-topmost", 1)
            root.protocol('WM_DELETE_WINDOW', self.on_closing)

            # 30 秒后自动关闭窗口
            # root.after(30000, lambda r=root: self.close_window(r))

            self.roots.append(root)

        self.keyboard_listener = self.start_keyboard_listener()

        # 启动所有 Tkinter 窗口
        for root in self.roots:
            root.mainloop()

    def close_window(self, root):
        # 安全地关闭单个窗口
        try:
            root.destroy()
        except:
            pass
        try:
            # 如果所有窗口都关闭了，停止程序
            if not any(r.winfo_exists() for r in self.roots):
                self.kill_program()
        except:
            pass
    def kill_program(self):
        print("正在退出程序...")
        self.status = 0
        # 停止键盘监听器
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        print("1")
        # 关闭所有 Tkinter 窗口
        for root in self.roots:
            print("a")
            if root.winfo_exists():
                print("b")
                root.quit()  # 停止窗口的主循环
                print("c")
                # root.destroy()  # 销毁窗口部件
                print("d")
        print("2")

        # 确保程序退出
        sys.exit(0)
        print("3")

    def unlock_by_special_key(self, key):
        if config.get_config_value("special_key") == 0:
            return False

        # 获取当前时间的分钟部分
        minutes = datetime.now().minute

        # 获取分钟的十分位作为特殊键
        special_key = str(minutes // 10)
        print(f"当前特殊键: {special_key}")

        if key == special_key:
            print("特殊键被按下，程序将退出。")
            self.status = 0
            return True
        return False


if __name__ == '__main__':
    h = hook()
    h.start_program()