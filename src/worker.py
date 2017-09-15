import logging
logging.getLogger().setLevel(logging.INFO)

import os

import redis
from rq import Worker, Queue, Connection

from worker_utils import runner_api

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')

conn = redis.from_url(redis_url)


def run_runner(**kwargs):
    runner = runner_api.RunnerApi(**kwargs)
    runner.write_configs()
    runner.create_app()
    return("Runner Complete")

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
