from flask import Flask

from rq import Queue
from rq.job import Job
from workers.worker import conn, create_app

app = Flask(__name__)
q = Queue(connection=conn)


@app.route('/', methods=['GET', 'POST'])
def index():
    job = q.enqueue_call(func=create_app, args=("edgeforrest", "test@example.com", "forrest", "edge"))
    return job.get_id()

@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202

if __name__ == "__main__":
    app.run()
