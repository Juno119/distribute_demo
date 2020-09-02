#!/usr/bin/env python
# -*- coding:utf-8 -*-

import redis

HOST="192.168.0.111"
PORT=30379

pool = redis.ConnectionPool(host=HOST, port=PORT)
r = redis.Redis(connection_pool=pool)
r.set('foo', 'Bar')
print(r.get('foo'))