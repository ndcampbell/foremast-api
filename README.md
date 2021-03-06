# Foremast-API

This is an API layer for Foremast. The idea is to make it easily callable from Spinnaker Webhook stages

It will manage a task queue and report on the status of Foremast tasks.


## Task Queue

Only uses Redis for the task queue. While something like celery or SQS is great, Spinnaker
already has a dependency on Redis and I would like to not introduce any more infrastructure 

Will use RQ: http://python-rq.org/

## Foremast Configuration

Put all Foremast Extras (templates, certificats, etc) in a `foremast_extras` directory in the root level of the project

Put the Foremast `config.py` in the root level, looking at `foremast_extras/` for anything path based.

## Running

Uses docker-compose to run the API, Worker, and Redis containers

`docker-compose up`

## API

### POST /v1/runner/<action>
Data: `{"group": "forrest", "repo": "edge", "owner_email": "d@example.com", "resources": ["app", "pipeline"]}`

`"resources"` is a list of resources for Foremast to create. Foremast will run `<action>` on these resources in the order provided.

Return: `{"task_id": "5f52dca4-ded2-4d8e-8519-9dbdbb8c64c1", "status_url": "http://localhost:5000/runner/logs/5f52dca4-ded2-4d8e-8519-9dbdbb8c64c1"}`

### GET /v1/runner/status/$taskID

Return: Status of the task and URL to logs

Possible status: `success`, `terminal`, `running`

### GET /v1/runner/logs/$taskID

Return: Text of logs from the task

### GET /v1/runner/jobs

Return: A list of failed_jobs and queued_jobs

## To Do:

- Swagger for API
- Error handling
- Parameter checking for posted data
