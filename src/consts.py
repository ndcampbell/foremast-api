import os
import logging

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379')
logging_level = logging.DEBUG 