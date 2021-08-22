from flask import render_template, request, Blueprint


jobs = Blueprint('jobs', __name__)


# --------------- Jobs page ----------------
@jobs.route("/view_jobs")
def view_jobs():
    return render_template("jobs.html")


# --------------- Edit Job page ----------------
@jobs.route("/edit_job")
def edit_job():
    return render_template("edit_job.html")


# --------------- Upload New Job page ----------------
@jobs.route("/upload_job")
def upload_job():
    return render_template("upload_job.html")

