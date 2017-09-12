from flask import Flask, request, jsonify
from rq import Queue
from rq.job import Job

from workers.worker import conn, create_app

app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/app', methods=['POST'])
def create_app():
    content = request.json
    job = q.enqueue_call(func=create_app, args=(content['app_name'], content['project'], content['repo'], content['owner_email']))
    return jsonify({"task_id": job.get_id()})


@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202

if __name__ == "__main__":
    app.run()
