# -*- coding:utf-8 -*-
from logger_helper import LoggerHelper
from config_helper import ConfigHelper
from register_service import RegisterCenter

if __name__ == "__main__":
    host = ConfigHelper().getConfig("zookeeper", "host")
    port = ConfigHelper().getConfig("zookeeper", "port")
    rs = RegisterCenter("{}:{}".format(host, port))
    rs.connect();
    try:
        rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8000}, False)
        rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8001}, False)
        rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8002}, False)
        LoggerHelper().info(rs.get_register("hello_provider", "provider"))
        LoggerHelper().info("****")
        LoggerHelper().info(rs.get("/hello_provider/provider/ID0000000002"))
        rs.set("/hello_provider/provider/ID0000000002", b"123")
        LoggerHelper().info(rs.get("/hello_provider/provider/ID0000000002"))
    except Exception as e:
        LoggerHelper().error(e)
    finally:
        rs.delete("/hello_provider")
    rs.close();