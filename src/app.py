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
    results_url = "{}runner/results/{}".format(request.url_root, job.get_id())
    return jsonify({"task_id": job.get_id(), "results_url": results_url})

@app.route("/runner/results/<job_key>", methods=['GET'])
def get_results(job_key):
    """Gets results of task with task ID"""
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        finished = {"status": "success", "logs": job.result}
        return jsonify(finished), 200
    elif job.is_failed:
        finished = {"status": "terminal", "logs": job.exc_info}
        return jsonify(finished), 400
    else:
        running = {"status": "running", "logs": ""}
        return jsonify(running), 202

@app.route("/runner/jobs", methods=['GET'])
def get_all_jobs():
    """Returns list of failed_jobs and list of queued_jobs"""
    fq = get_failed_queue(connection=conn)
    job_data = {'queued_jobs': q.job_ids,
                'failed_jobs': fq.job_ids}
    return jsonify(job_data), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
