from flask import render_template, request, Blueprint
from application import mongo

jobs = Blueprint('jobs', __name__)


# --------------- Jobs page ----------------
@jobs.route("/view_jobs")
def view_jobs():
    jobs_db = mongo.db.jobs.find()
    return render_template("jobs.html", jobs_db=jobs_db)


# --------------- Edit Job page ----------------
@jobs.route("/edit_job")
def edit_job():
    return render_template("edit_job.html")


# --------------- Upload New Job page ----------------
@jobs.route("/upload_job")
def upload_job():
    return render_template("upload_job.html")

