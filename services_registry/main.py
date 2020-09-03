# -*- coding:utf-8 -*-
import os
from logger_helper import LoggerHelper
from config_helper import ConfigHelper
from register_service import RegisterCenter

if __name__ == "__main__":
    host = ConfigHelper().getConfig("zookeeper", "host")
    port = ConfigHelper().getConfig("zookeeper", "port")
    rs = RegisterCenter("{}:{}".format(host, port))
    rs.connect();
    try:
        rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8000})
        rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8001})
        rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8002})
        LoggerHelper().info(rs.get_register("hello_provider", "provider"))
        LoggerHelper().info("****")
        LoggerHelper().info(rs.get("/hello_provider/provider/ID0000000002"))
        rs.set("/hello_provider/provider/ID0000000002", b"123")
        LoggerHelper().info(rs.get("/hello_provider/provider/ID0000000002"))
        LoggerHelper().info(rs.get_children("/hello_provider/provider"))
        os.system("pause")
    except Exception as e:
        LoggerHelper().error(e)
    finally:
        rs.delete("/hello_provider")
    rs.close();