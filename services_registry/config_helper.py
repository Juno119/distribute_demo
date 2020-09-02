# -*- coding:utf-8 -*-

import os
from singleton_helper import Singleton
import configparser
from logger_helper import LoggerHelper

@Singleton
class ConfigHelper:
    def getConfig(self, section, key):
        config = configparser.ConfigParser()
        configpath = os.path.split(os.path.realpath(__file__))[0] + "/conf"
        config.read(configpath + "/service.conf")
        return config.get(section, key)

if __name__ == "__main__":
    LoggerHelper().info(ConfigHelper().getConfig("database", "dbname"))