from flask import (render_template, request, redirect, 
                    url_for, flash, Blueprint)
from application import mongo
from application.models import User, Role, Job
from werkzeug.utils import escape, unescape
from application.jobs.forms import CreateJobForm, UpdateJobForm

jobs = Blueprint('jobs', __name__, template_folder="templates")


# --------------- Jobs page ----------------
@jobs.route("/view")
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
@jobs.route("/edit", methods=["GET", "POST"])
def edit_job():
    return render_template("edit_job.html")


# --------------- Upload New Job page ----------------
@jobs.route("/create", methods=["GET", "POST"])
def create_job():
    form = CreateJobForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            company     = escape(form.company.data)
            position	= escape(form.position.data)
            description = escape(form.description.data)
            salary		= form.salary.data
            location	= escape(form.location.data)
            contract    = form.contract.data
            level       = form.level.data

            job = Job(company, position, description, salary, location, contract, level)
            job.insert_into_database()

            flash("You have added a new job!")
            return redirect(url_for("main.home"))
        if form.errors:
            flash("{}".format(form.errors))

    return render_template("create_job.html", form=form)
