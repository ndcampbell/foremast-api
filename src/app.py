import logging

from flask import Flask, request, jsonify
import redis
from rq import Queue, get_failed_queue
from rq.job import Job

from consts import redis_url, logging_level
from worker import run_runner

logging.getLogger().setLevel(logging_level)
app = Flask(__name__)
conn = redis.from_url(redis_url)
q = Queue(connection=conn)

@app.route('/health', methods=['GET'])
def health():
    """Basic healthcheck endpoint"""
    return jsonify({"up": True}), 200

@app.route('/runner/<action>', methods=['POST'])
def runner(action):
    """Runs Foremast Runner against posted resources"""
    job = q.enqueue_call(func=run_runner, args=[action], kwargs=request.json, timeout=600)
    status_url = "{}runner/status/{}".format(request.url_root, job.get_id())
    return jsonify({"task_id": job.get_id(), "status_url": status_url})

@app.route("/runner/status/<job_key>", methods=['GET'])
def get_status(job_key):
    """Gets results of task with task ID"""
    job = Job.fetch(job_key, connection=conn)

    logs_url = "{}runner/logs/{}".format(request.url_root, job_key)
    status_dict = {"status": "", "logs_url": logs_url}
    return_code = 200
    if job.is_finished:
        status_dict['status'] = "success"
        return_code = 200
        #finished = {"status": "complete", "logs": job.result}
    elif job.is_failed:
        status_dict['status'] = "terminal"
        return_code = 400
        #finished = {"status": "failure", "logs": job.exec_info}
    else:
        status_dict['status'] = "running"
        status_dict['logs_url'] = ""
        return_code = 202

    return jsonify(status_dict), return_code

@app.route("/runner/logs/<job_key>", methods=['GET'])
def get_logs(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        logs = job.result
    elif job.is_failed:
        logs = job.exc_info
    else:
        logs = "Task is still running"
    return str(logs), 200
    

@app.route("/runner/jobs", methods=['GET'])
def get_all_jobs():
    """Returns list of failed_jobs and list of queued_jobs"""
    fq = get_failed_queue(connection=conn)
    job_data = {'queued_jobs': q.job_ids,
                'failed_jobs': fq.job_ids}
    return jsonify(job_data), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
