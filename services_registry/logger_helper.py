# -*- coding:utf-8 -*-

import os
import sys
import logging
from datetime import *
from singleton_helper import Singleton

@Singleton
class LoggerHelper:
    def __init__(self):
        self.log = self.getlog()

    def info(self, message):
        self.log.info(message)

    def error(self, message):
        self.log.error(message)

    def getlog(self):
        logger = logging.getLogger("logger_helper")
        formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S', )
        logpath = self.getcurrpath() + "/log"
        if not os.path.exists(logpath):
            os.mkdir(logpath)
        file_handler = logging.FileHandler(logpath + "/%s.log" % date.today())
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def getcurrpath(self):
        path = sys.path[0]
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)


if __name__ == "__main__":
    LoggerHelper().info("hello world11111")
