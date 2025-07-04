# https://blog.csdn.net/weixin_43840640/article/details/130881763

import logging
import os
from logging import handlers
from pathlib import Path


class Logger:
    def __init__(self,loggername = None):
        self.logger = logging.getLogger(loggername)

        _level = "INFO"

        try:
            self.logger.setLevel(_level.upper())
        except ValueError:
            self.logger.setLevel(logging.INFO)

        # 指定日志输出格式
        self.formatter = logging.Formatter(
            fmt = "%(asctime)s - [%(filename)s] -[%(funcName)s:%(lineno)s] - %(levelname)s - %(name)s - : %(message)s",
            datefmt = "%Y-%m-%d %H:%M:%S"
        )

        # 指定日志输出路径
        self.log_path = "./log/"
        if not Path(self.log_path).is_dir():
            os.makedirs(self.log_path)

        # 指定日志输出文件
        #_rq = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        _rq = "log"

        self.log_info_file = self.log_path + _rq + '.txt'

        # 控制台输出
        self.set_console_logger()
        # 文件输出
        self.set_file_logger()

    def set_file_logger(self):
        """
        将日志输出到文件
        :return:
        """
        log_handler_info = logging.FileHandler(self.log_info_file, mode='a', encoding='utf-8')
        log_handler_info = handlers.RotatingFileHandler(filename=self.log_info_file, maxBytes=1024 * 1024 * 300,backupCount=3)
        # 设置日志输出格式
        log_handler_info.setFormatter(self.formatter)
        # 设置过滤条件
        info_filter = logging.Filter()
        info_filter.filter = lambda record: record.levelno >= logging.INFO
        # 将文件输出日志添加过滤条件
        log_handler_info.addFilter(info_filter)
        # 对logger增加handler日志处理器
        self.logger.addHandler(log_handler_info)

    def set_console_logger(self):
        """
        将日志输出到控制台
        """
        _ch = logging.StreamHandler()
        _ch.setLevel(logging.INFO)
        _ch.setFormatter(self.formatter)
        self.logger.addHandler(_ch)

    def get_logger(self):
        return self.logger


log = Logger("Smile2Unlock").get_logger()

if __name__ == '__main__':
    log.info("123")

