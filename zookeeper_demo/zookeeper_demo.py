# -*- coding: UTF-8 -*-
from kazoo.client import KazooClient

HOSTS="192.168.0.111:30100"

zk = KazooClient(hosts=HOSTS)
zk.start()
nodes = zk.get_children('/')
print(nodes)
value, stat = zk.get('/test')
print(value, stat)
zk.stop()