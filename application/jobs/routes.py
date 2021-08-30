from flask import (render_template, request, redirect, session, 
                    url_for, flash, Blueprint)
from application import mongo
from application.models import User, Job
from werkzeug.utils import escape
from application.jobs.forms import CreateJobForm, UpdateJobForm

jobs = Blueprint('jobs', __name__, template_folder="templates")


# --------------- Jobs page ----------------
@jobs.route("/view")
def view_jobs():
    jobs = Job.find_all_jobs()
    return render_template("jobs.html", jobs=jobs)


@jobs.route("/search", methods=["GET", "POST"])
def filtered_jobs():
    if request.method == "POST":
        query = request.form.get("search")
        jobs = mongo.db.jobs.find({"position": query})
    return render_template("jobs.html", jobs=jobs)


# --------------- Edit Job page ----------------
@jobs.route("/edit", methods=["GET", "POST"])
def edit_job():
    return render_template("edit_job.html")


# --------------- Upload New Job page ----------------
@jobs.route("/create", methods=["GET", "POST"])
def create_job():
    form = CreateJobForm()
    
    if form.validate_on_submit():
        company     = escape(form.company.data)
        position	= escape(form.position.data)
        description = escape(form.description.data)
        salary		= form.salary.data
        location	= escape(form.location.data)
        contract    = form.contract.data
        level       = form.level.data
        employer_id = User.get_user_id(session["email"])

        job = Job(company, position, description, salary, location, 
                contract, level, employer_id)
        job.insert_into_database()

        flash("You have added a new job!")
        return redirect(url_for("main.home"))

    return render_template("create_job.html", form=form)
