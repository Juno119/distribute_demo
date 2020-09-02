# -*- coding:utf-8 -*-
import json
from kazoo.client import KazooClient
from logger_helper import LoggerHelper
from config_helper import ConfigHelper


class RegisterCenter(object):
    def __init__(self, hosts="127.0.0.1:2181"):
        self.hosts = hosts

    def connection_listener(self):
        if self.state == "LOST":
            LoggerHelper().warning("zookeeper connect lost!")
        # Register somewhere that the session was lost
        elif self.state == "SUSPENDED":
            LoggerHelper().warning("zookeeper connect disconnected!")
        # Handle being disconnected from Zookeeper
        else:
            LoggerHelper().info("zookeeper connect connected!")
            # Handle being connected/reconnected to Zookeeper

    def connect(self):
        if self.hosts:
            zk = KazooClient(hosts=self.hosts)
        else:
            zk = KazooClient()
        zk.start()
        zk.add_listener(self.connection_listener)
        return zk

    def return_service_type(self, type):
        if type not in ["provider", "consumer"]:
            LoggerHelper().warning("type is not provider or consumer!")
            raise Exception("type must be provider or consumer!")
        return 1

    def service_register(self, servicename, type, address, ephemeral=True, sequence=True):
        if self.return_service_type(type):
            zk = self.connect()
            zk.ensure_path("/%s/%s" % (servicename, type))
            zk.create("/%s/%s/ID" % (servicename, type), json.dumps(address).encode('utf-8'), ephemeral=ephemeral, sequence=sequence)

    def get_register(self, servicename, type):
        if self.return_service_type(type):
            zk = self.connect()
            result = zk.get_children("/%s/%s" % (servicename, type))
            register = []
            if result:
                for i in result:
                    data, stat = zk.get("/%s/%s/%s" % (servicename, type, i))
                    register.append(data.decode("utf-8"))
            return register
        return []


if __name__ == "__main__":
    host = ConfigHelper().getConfig("zookeeper", "host")
    port = ConfigHelper().getConfig("zookeeper", "port")
    rs = RegisterCenter("{}:{}".format(host, port))
    rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8002})
    LoggerHelper().info("============get_register:")
    LoggerHelper().info(rs.get_register("hello_provider", "provider"))
