import logging
import os
from io import StringIO as StringBuffer

import redis
from rq import Worker, Queue, Connection

from consts import redis_url
import runner_api


logging.getLogger().setLevel(logging.INFO)


def capture_logs():
    """Setups a StringBuffer to capture foremast logs"""
    logger = logging.getLogger("foremast")
    log_capture_string = StringBuffer()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    return log_capture_string

def run_runner(action, **kwargs):
    log_capture_string = capture_logs()    
    runner = runner_api.RunnerApi(**kwargs)
    runner.write_configs()
    for resource in kwargs.get("resources"):
        func_name = "{}_{}".format(action, resource)
        runner_func = getattr(runner, func_name)
        runner_func()
    runner.cleanup()
    log_contents = log_capture_string.getvalue()
    log_capture_string.close()
    return(log_contents)

if __name__ == '__main__':
    conn = redis.from_url(redis_url)
    with Connection(conn):
        listen = ['default']
        worker = Worker(list(map(Queue, listen)))
        worker.work()
