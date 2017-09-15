import logging
logging.getLogger().setLevel(logging.INFO)

import os

import redis
from rq import Worker, Queue, Connection

from consts import redis_url
import runner_api


def run_runner(action, **kwargs):
    runner = runner_api.RunnerApi(**kwargs)
    runner.write_configs()
    for resource in kwargs.get("resources"):
        func_name = "{}_{}".format(action, resource)
        runner_func = getattr(runner, func_name)
        runner_func()
    runner.cleanup()
    return("Runner Complete")

if __name__ == '__main__':
    conn = redis.from_url(redis_url)
    with Connection(conn):
        listen = ['default']
        worker = Worker(list(map(Queue, listen)))
        worker.work()
