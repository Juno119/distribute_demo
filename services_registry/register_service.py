# -*- coding:utf-8 -*-
import json
from kazoo.client import KazooClient
from logger_helper import LoggerHelper
from config_helper import ConfigHelper

class RegisterCenter(object):
    def __init__(self, hosts="127.0.0.1:2181"):
        self.hosts = hosts

    def connection_listener(self, state):
        if state == "LOST":
            LoggerHelper().info("zookeeper connect lost!")
            # Register somewhere that the session was lost
        elif state == "SUSPENDED":
            LoggerHelper().info("zookeeper connect disconnected!")
            # Handle being disconnected from Zookeeper
        else:
            LoggerHelper().info("zookeeper connect connected!")
            # Handle being connected/reconnected to Zookeeper

    def connect(self):
        if self.hosts:
            self.zk = KazooClient(hosts=self.hosts)
        else:
            self.zk = KazooClient()
        self.zk.add_listener(self.connection_listener)
        self.zk.start()


    def close(self):
        self.zk.stop()
        self.zk.close()

    def get(self, node):
        return self.zk.get(node)

    def get_children(self, node):
        return self.zk.get_children(node)

    def delete(self, node, recursive=True):
        self.zk.delete(node, recursive=recursive)

    def set(self, node, value):
        self.zk.set(node, value)

    def return_service_type(self, type):
        if type not in ["provider", "consumer"]:
            LoggerHelper().warning("type is not provider or consumer!")
            raise Exception("type must be provider or consumer!")
        return 1

    def service_register(self, servicename, type, address, ephemeral=True, sequence=True):
        if self.return_service_type(type):
            self.zk.ensure_path("/%s/%s" % (servicename, type))
            self.zk.create("/%s/%s/ID" % (servicename, type), json.dumps(address).encode('utf-8'), ephemeral=ephemeral, sequence=sequence)

    def get_register(self, servicename, type):
        if self.return_service_type(type):
            result = self.zk.get_children("/%s/%s" % (servicename, type))
            register = []
            if result:
                for i in result:
                    data, stat = self.zk.get("/%s/%s/%s" % (servicename, type, i))
                    register.append(data.decode("utf-8"))
        return register


if __name__ == "__main__":
    host = ConfigHelper().getConfig("zookeeper", "host")
    port = ConfigHelper().getConfig("zookeeper", "port")
    rs = RegisterCenter("{}:{}".format(host, port))
    rs.connect();
    rs.service_register("hello_provider", "provider", {"host": "127.0.0.1", "port": 8002})
    LoggerHelper().info("============get_register:")
    LoggerHelper().info(rs.get_register("hello_provider", "provider"))
    rs.close();
