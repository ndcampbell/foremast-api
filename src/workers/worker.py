import os

import redis
from rq import Worker, Queue, Connection

import foremast

listen = ['default']

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')

conn = redis.from_url(redis_url)

def setup_configs(git_short):
    app_configs = configs.process_git_configs(git_short=git_short)
    return app_configs


def create_app(appname, project, repo, email):
    short = group + "/" + repo
    app_configs = setup_configs(short)
    spinnakerapp = foremast.app.SpinnakerApp(app=appname, email=email, project=group, repo=repo,
  				    pipeline_config=app_configs['pipeline'])
    spinnakerapp.create_app()

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
