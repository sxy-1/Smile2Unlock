"""
auto_relock — 解锁后空闲自动重锁 + 快捷键回白屏

由 smile2unlock_entry.py 在成功解锁后启动，与主进程同进程运行，不产生独立 exe。

配置（config.json）：
    relock_timeout : float  超时秒数，-1 表示不启动（默认）
    lock_hotkey    : str    pynput GlobalHotKeys 格式，如 "<ctrl>+<shift>+l"，空串表示不注册

触发行为：
    超时          → LockWorkStation()（真锁），relocked=True
    快捷键        → 不真锁，直接回白屏，relocked=False
"""

import threading
import time
from ctypes import windll

from pynput import keyboard, mouse

from src.logger import log


def _lock_workstation():
    ret = windll.LoadLibrary("user32.dll").LockWorkStation()
    if not ret:
        log.warning("auto_relock: LockWorkStation() 调用失败")


class RelockWatcher:
    def __init__(self, timeout: float, hotkey: str = ""):
        self.timeout = timeout
        self.hotkey = hotkey
        self.relocked = False  # True=真锁触发，False=快捷键触发（回白屏）
        self._last_activity = time.monotonic()
        self._activity_lock = threading.Lock()
        self._stop_event = threading.Event()

    def _record_activity(self, *args, **kwargs):
        with self._activity_lock:
            self._last_activity = time.monotonic()

    def _trigger_real_lock(self, reason: str):
        log.info(f"auto_relock: {reason}，真锁")
        self.relocked = True
        _lock_workstation()
        self._stop_event.set()

    def _trigger_overlay(self, reason: str):
        log.info(f"auto_relock: {reason}，回白屏")
        self.relocked = False
        self._stop_event.set()

    def _watch_loop(self):
        log.info(f"auto_relock: 启动，超时 {self.timeout}s，快捷键「{self.hotkey or '未配置'}」")
        while not self._stop_event.is_set():
            time.sleep(1)
            with self._activity_lock:
                elapsed = time.monotonic() - self._last_activity
            if elapsed < self.timeout:
                continue
            self._trigger_real_lock(f"无操作 {elapsed:.0f}s")

    def start(self):
        mouse.Listener(
            on_move=self._record_activity,
            on_click=self._record_activity,
            on_scroll=self._record_activity,
        ).start()
        keyboard.Listener(on_press=self._record_activity).start()

        if self.hotkey:
            try:
                keyboard.GlobalHotKeys(
                    {self.hotkey: lambda: self._trigger_overlay(f"快捷键 {self.hotkey}")}
                ).start()
                log.info(f"auto_relock: 快捷键 {self.hotkey} 已注册")
            except Exception as e:
                log.warning(f"auto_relock: 快捷键注册失败: {e}")

        threading.Thread(target=self._watch_loop, daemon=True).start()

    def wait(self):
        """阻塞调用方，直到触发（真锁或快捷键）。"""
        self._stop_event.wait()
