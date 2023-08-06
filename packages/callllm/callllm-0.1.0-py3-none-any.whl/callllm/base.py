#!/usr/bin/env python

import gevent

from .tasks import add_task, get_task, empty
from .worker import Worker

workers = []

def add_request(url, kwargs, callback=None):
    add_task(url, kwargs, callback)

def add_worker(api_key=None, api_hoster=None):
    worker = Worker(api_key=api_key, api_hoster=api_hoster)
    workers.append(worker)

def go():
    for worker in workers:
        worker.start()
    gevent.joinall(workers)
