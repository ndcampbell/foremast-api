import logging
logging.getLogger().setLevel(logging.INFO)

from flask import Flask, request, jsonify
import redis
from rq import Queue
from rq.job import Job

from consts import redis_url
from worker import run_runner

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
    return jsonify({"task_id": job.get_id()})

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    """Gets results of task with task ID"""
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return jsonify({"result": "success", "return": job.result}), 200
    elif job.is_failed:
        return jsonify({"result": "failed", "exception": job.exc_info}), 400
    else:
        return "Job still running", 202

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
