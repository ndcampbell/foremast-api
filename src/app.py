import logging
logging.getLogger().setLevel(logging.INFO)

from flask import Flask, request, jsonify
from rq import Queue
from rq.job import Job

from worker import conn, run_runner

app = Flask(__name__)
q = Queue(connection=conn)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"up": True}), 200

@app.route('/runner', methods=['POST'])
def runner():
    job = q.enqueue_call(func=run_runner, kwargs=request.json)
    return jsonify({"task_id": job.get_id()})

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    elif job.is_failed:
        return str("failed"), 400
    else:
        return "Job still running", 202

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
