# -*- coding:utf-8 -*-
from logger_helper import LoggerHelper
from config_helper import ConfigHelper
from register_service import RegisterCenter

if __name__ == "__main__":
    host = ConfigHelper().getConfig("zookeeper", "host")
    port = ConfigHelper().getConfig("zookeeper", "port")
    rs = RegisterCenter("{}:{}".format(host, port))
    rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8000}, False)
    rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8001}, False)
    rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8002}, False)
    LoggerHelper().info("============get_register:")
    LoggerHelper().info(rs.get_register("hello_provider", "provider"))
    LoggerHelper().info(rs.get_register("hello_provider", "provider"))
    LoggerHelper().info(rs.get_register("hello_provider", "provider"))