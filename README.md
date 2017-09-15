# Foremast-API

This is an API layer for Foremast. The idea is to make it easily callable from Spinnaker Webhook stages

It will manage a task queue and report on the status of Foremast tasks.


## Task Queue

Only uses Redis for the task queue. While something like celery or SQS is great, Spinnaker
already has a dependency on Redis and I would like to not introduce any more infrastructure 

Will use RQ: http://python-rq.org/

## Running

Uses docker-compose to run the API and Redis containers (need to add worker logic still)

`docker-compose up`

## API

### POST /runner
Data: `{"group": "forrest", "repo": "edge", "owner_email": "d@example.com", "resources": ["app", "pipeline"]}`

`"resources"` is a list of resources for Foremast to create. Foremast will create these resources in the order provided

Return: `{"task_id": $taskID}`

### GET /results/$taskID

Return: Status of the task

## To Do:

- Swagger for API
- Handle logging better (send Foremast logs as return of task)
- Error handling
- Parameter checking for posted data