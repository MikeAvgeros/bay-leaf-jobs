from flask import (render_template, request, redirect, 
                    url_for, flash, Blueprint)
from application import mongo

jobs = Blueprint('jobs', __name__, template_folder="templates")


# --------------- Jobs page ----------------
@jobs.route("/view_jobs")
def view_jobs():
    jobs_db = mongo.db.jobs.find()
    return render_template("jobs.html", jobs_db=jobs_db)

@jobs.route("/search", methods=["GET", "POST"])
def filtered_jobs():
    if request.method == "POST":
        query = request.form.get("search")
        jobs_db = mongo.db.jobs.find({"position": query})
    return render_template("jobs.html", jobs_db=jobs_db)


# --------------- Edit Job page ----------------
@jobs.route("/edit_job")
def edit_job():
    return render_template("edit_job.html")


# --------------- Upload New Job page ----------------
@jobs.route("/upload_job", methods=["GET", "POST"])
def upload_job():
    if request.method == "POST":
        job = {
            "company": request.form.get("company"),
            "position": request.form.get("position"),
            "location": request.form.get("location"),
            "salary": request.form.get("salary"),
            "contract": request.form.get("contract"),
            "level": request.form.get("level"),
            "description": request.form.get("description")
        }
        mongo.db.jobs.insert_one(job)
        flash("Job Successfully Uploaded")
        return redirect(url_for("jobs.upload_job"))

    return render_template("upload_job.html")

