# Foremast-API

This is an API layer for Foremast. The idea is to make it easily callable from Spinnaker Webhook stages

It will manage a task queue and report on the status of Foremast tasks.


## Task Queue

Should only use Redis for the task queue. While something like celery or SQS is great, Spinnaker
already has a dependency on Redis and I would like to not introduce any more infrastructure 

Will use RQ: http://python-rq.org/


