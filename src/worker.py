import logging
import os
from io import StringIO as StringBuffer

import redis
from rq import Worker, Queue, Connection

from consts import redis_url, logging_level
import runner_api


logging.getLogger().setLevel(logging_level)


def capture_logs():
    """Setups a StringBuffer to capture foremast logs"""
    logger = logging.getLogger("foremast")
    log_capture_string = StringBuffer()
    ch = logging.StreamHandler(log_capture_string)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    ch.setLevel(logging_level)
    logger.addHandler(ch)
    return log_capture_string

def run_runner(action, **kwargs):
    log_capture_string = capture_logs()    
    try:
        runner = runner_api.RunnerApi(**kwargs)
        runner.write_configs()
        for resource in kwargs.get("resources"):
            func_name = "{}_{}".format(action, resource)
            runner_func = getattr(runner, func_name)
            runner_func()
        runner.cleanup()
    except:
        log_contents = log_capture_string.getvalue()
        log_capture_string.close()
        raise ForemastException(log_contents)
    log_contents = log_capture_string.getvalue()
    log_capture_string.close()
    return(log_contents)

class ForemastException(Exception):
    def __init__(self, tb):
        Exception.__init__(self, tb)

if __name__ == '__main__':
    conn = redis.from_url(redis_url)
    with Connection(conn):
        listen = ['default']
        worker = Worker(list(map(Queue, listen)))
        worker.work()
