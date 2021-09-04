from flask import (render_template, request, redirect, session, 
                    url_for, flash, Blueprint)
from application import mongo
from application.models import Application, User, Job
from application.jobs.forms import CreateJobForm, UpdateJobForm, ApplicationForm


jobs = Blueprint('jobs', __name__, template_folder="templates")


# --------------- All Jobs ----------------
@jobs.route("/jobs")
def view_jobs():
    jobs = Job.find_all_jobs()
    return render_template("view_jobs.html", jobs=jobs)


# --------------- Filter jobs ----------------
@jobs.route("/jobs/search", methods=["GET", "POST"])
def filter_jobs():
    if request.method == "POST":
        query = request.form.get("search").lower()
        jobs = mongo.db.jobs.find({
            "$or": [{
                "company"  : query
            }, {
                "position" : query
            }, {
                "stack"    : query
            }, {
                "level"    : query
            }, {
                "contract" : query
            }, {
                "location" : query
            }]
        })
    return render_template("view_jobs.html", jobs=jobs)


# --------------- Single Job ----------------
@jobs.route("/job/<int:job_id>")
def view_job(job_id):
    job = Job.find_job_by_id(job_id)
    return render_template("view_jobs.html", job=job)


# --------------- Update Job ----------------
@jobs.route("/job/<int:job_id>/update", methods=["GET", "POST"])
def update_job(job_id):
    # Check if job exists in MongoDB
    job = Job.find_job_by_id(job_id)

    if job:
        # Instantiate the updateprofile form
        form = UpdateJobForm()

        # Check if user has submitted the form and all inputs are valid
        if form.validate_on_submit():
            company          = form.company.data
            position	     = form.position.data
            stack            = form.stack.data
            description      = form.description.data
            responsibilities = form.responsibilities.data
            requirements     = form.requirements.data
            salary		     = form.salary.data
            location	     = form.location.data
            contract         = form.contract.data
            level            = form.level.data

            updated_info = {
                "company"          : company,
                "position"         : position,
                "stack"            : stack,
                "description"      : description,
                "responsibilities" : responsibilities,
                "requirements"     : requirements,
                "salary"           : salary,
                "location"         : location,
                "contract"         : contract,
                "level"            : level
            }

            # Find job in MongoDB and update its info based on the submitted form
            Job.edit_job(job["_id"], updated_info)
            flash("The job has been updated!")
            return redirect(url_for("jobs.view_job", job=job))

        form.company.data          = job["company"].capitalize()
        form.position.data         = job["position"].capitalize()
        form.stack.data            = job["stack"]
        form.description.data      = job["description"]
        form.responsibilities.data = job["responsibilities"]
        form.requirements.data     = job["requirements"]
        form.salary.data           = job["salary"]
        form.location.data         = job["location"]
        form.contract.data         = job["contract"]
        form.level.data            = job["level"]

    return render_template("update_job.html", form=form)


# --------------- Delete Job ----------------
@jobs.route("/job/<int:job_id>/delete", methods=["POST"])
def delete_job(job_id):
    # Check if job exists in MongoDB
    job = Job.find_job_by_id(job_id)

    if job:
        Job.delete_job(job_id)
        flash("Job successfully deleted")
        return redirect(url_for("main.home"))

    flash("This job does not exist")
    return redirect(url_for("main.home"))


# --------------- Apply to job ----------------
@jobs.route("/job/<int:job_id>/apply", methods=["GET", "POST"])
def apply_to_job(job_id):
    # Check if job exists
    job = Job.find_job_by_id(job_id)

    if job:
        # Instantiate the Application form
        form = ApplicationForm()

        if form.validate_on_submit():
            notice_period   = form.notice_period.data
            current_salary  = form.current_salary.data
            desired_salary  = form.desired_salary.data
            resume          = form.resume.data
            cover_letter    = form.cover_letter.data
            applied_for     = job_id
            developer       = session["username"]

            application = Application(notice_period, current_salary, desired_salary, 
                                    resume, cover_letter, applied_for, developer)
            application.insert_into_database()
            flash("Congratulations! You have applied to the job.")
            return redirect(url_for("main.home"))

        return render_template("job_application.html", form=form)

    flash("Job does not longer exist")
    return redirect(url_for("main.home"))

    
# --------------- Create New Job ----------------
@jobs.route("/create_job", methods=["GET", "POST"])
def create_job():
    form = CreateJobForm()
    
    if form.validate_on_submit():
        company          = form.company.data
        position	     = form.position.data
        stack            = form.stack.data
        description      = form.description.data
        responsibilities = form.responsibilities.data
        requirements     = form.requirements.data
        salary		     = form.salary.data
        location	     = form.location.data
        contract         = form.contract.data
        level            = form.level.data
        posted_by        = session["username"]

        job = Job(company, position, stack, description, responsibilities,
        requirements, salary, location, contract, level, posted_by)
        job.insert_into_database()

        flash("Congratulations! You have created a new job.")
        return redirect(url_for("main.home"))

    return render_template("create_job.html", form=form)
