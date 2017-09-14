import logging
logging.getLogger().setLevel(logging.INFO)

import os

import redis
from rq import Worker, Queue, Connection

import foremast

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')

conn = redis.from_url(redis_url)


def handle_foremast_logging():
    for key in logging.Logger.manager.loggerDict:
        if key.startswith('foremast.'):
            logging.getLogger(key).setLevel(logging.CRITICAL)

def setup_configs(git_short):
    app_configs = foremast.configs.process_git_configs(git_short=git_short)
    all_configs = foremast.configs.write_variables(app_configs=app_configs, out_file="/tmp/out", git_short=git_short)
    return all_configs

def create_app(appname, project, repo, email):
    short = project + "/" + repo
    app_configs = setup_configs(short)
    spinnakerapp = foremast.app.SpinnakerApp(app=appname, email=email, project=project, repo=repo,
 				    pipeline_config=app_configs['pipeline'])
    spinnakerapp.create_app()
    return("Application created successfully application")

if __name__ == '__main__':
    handle_foremast_logging()
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
