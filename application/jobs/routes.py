from flask import (render_template, request, redirect, session, 
                    url_for, flash, Blueprint)
from application import mongo
from functools import wraps
from application.models import Application, Job
from application.jobs.forms import CreateJobForm, UpdateJobForm, ApplicationForm
import smtplib
from config import Config


jobs = Blueprint('jobs', __name__, template_folder="templates")


# ---------- Login required security -----------
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # Checks if email is in session to verify is user has signed in
        if "email" in session:
            return f(*args, **kwargs)

        else:
            flash("You must sign in to access this page!")
            return redirect(url_for("users.login"))

    return wrap


# --------------- All jobs -----------------

@jobs.route("/jobs")
@login_required
def view_jobs():
    # Find all jobs in MongoDB 
    jobs = Job.find_all_jobs()
    return render_template("view_jobs.html", jobs=jobs)


# --------------- Single job ----------------
@jobs.route("/job/<job_id>")
@login_required
def view_job(job_id):
    # Find job in MongoDB by its id
    job = Job.find_job_by_id(job_id)
    return render_template("view_job.html", job=job)


# --------------- Filter jobs ----------------
@jobs.route("/jobs/search", methods=["GET", "POST"])
@login_required
def filter_jobs():
    # Check if user submitted the form
    if request.method == "POST":
        # Get the input from the form and search in MongoDB
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


# --------------- Update job ----------------
@jobs.route("/job/<job_id>/update", methods=["GET", "POST"])
@login_required
def update_job(job_id):
    # Find job in MongoDB by its id
    job = Job.find_job_by_id(job_id)

    # Check if job exists in MongoDB
    if job:
        # Check if job was posted by this user
        if job["posted_by"] == session["username"]:
            # Instantiate the update profile form
            form = UpdateJobForm()

            # Check if user has submitted the form and all inputs are valid
            if form.validate_on_submit():
                company          = form.company.data.lower()
                position	     = form.position.data.lower()
                stack            = form.stack.data.lower()
                description      = form.description.data
                responsibilities = form.responsibilities.data
                requirements     = form.requirements.data
                salary		     = form.salary.data
                location	     = form.location.data.lower()
                contract         = form.contract.data.lower()
                level            = form.level.data.lower()

                # Register info based on what the user submitted on the form
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
                    "level"            : level,
                    "posted_by"        : session["username"],
                    "email"            : session["email"]
                }

                # Update job's info using the registered updated info.
                Job.edit_job(job["_id"], updated_info)
                flash("The job has been updated!")
                return redirect(url_for("users.profile", username=session["username"]))

            # Populate form data based on existing job info        
            form.company.data          = job["company"].capitalize()
            form.position.data         = job["position"].capitalize()
            form.stack.data            = job["stack"].capitalize()
            form.description.data      = job["description"]
            form.responsibilities.data = job["responsibilities"]
            form.requirements.data     = job["requirements"]
            form.salary.data           = job["salary"]
            form.location.data         = job["location"].capitalize()
            form.contract.data         = job["contract"].capitalize()
            form.level.data            = job["level"].capitalize()

            return render_template("update_job.html", form=form)

        flash("This job does not exist.")
        return redirect(url_for("main.home"))

    flash("This page can only be accessed by recruiters.")
    return redirect(url_for("main.home"))


# --------------- Delete job ----------------
@jobs.route("/job/<job_id>/delete", methods=["POST"])
@login_required
def delete_job(job_id):
    # Find job in MongoDB by its id
    job = Job.find_job_by_id(job_id)

    # Check if the job exists
    if job:
        # Check if job was posted by this user
        if job["posted_by"] == session["username"]:
            # Delete job from MongoDB
            Job.delete_job(job_id)
            flash("Job successfully deleted")
            return redirect(url_for("users.profile", username=session["username"]))

        flash("This page can only be accessed by recruiters.")
        return redirect(url_for("main.home"))

    flash("This job does not exist")
    return redirect(url_for("main.home"))


# --------------- Apply to job ----------------
@jobs.route("/job/<job_id>/apply", methods=["GET", "POST"])
@login_required
def apply_to_job(job_id):
    # Find job in MongoDB by its id
    job = Job.find_job_by_id(job_id)

    # Check if job exists
    if job:
        # Check if the user is a developer
        if session["role"] == "Developer":
            # Instantiate the application form
            form = ApplicationForm()

            # Check if user has submitted the form and all inputs are valid
            if form.validate_on_submit():
                notice_period   = form.notice_period.data
                current_salary  = form.current_salary.data
                desired_salary  = form.desired_salary.data
                resume          = form.resume.data
                cover_letter    = form.cover_letter.data
                applicant       = session["username"]
                email           = session["email"]

                # Create an instance of Application with the info the user submitter on the form
                application = Application(notice_period, current_salary, 
                                        desired_salary, resume, cover_letter, 
                                        job_id, applicant, email)
                # Add application to MongoDB
                application.insert_into_database()

                # Send confirmation email
                sender_mail = Config.MAIL_USERNAME
                password = Config.MAIL_PASSWORD
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(sender_mail, password)
                message = f"""
                Hello {applicant},

                We have received your application for the position of {job["position"]} at {job["company"]}.
                
                Your details have been forwarded to the recruiter and they will be in touch should you meet their criteria.
                """
                server.sendmail(sender_mail, email, message)
                flash("Congratulations! You have applied to the job.")
                return redirect(url_for("main.home"))

            return render_template("job_application.html", form=form)

        flash("This page can only be accessed by recruiters.")
        return redirect(url_for("main.home"))

    flash("This job not longer exists")
    return redirect(url_for("main.home"))

    
# --------------- Create new job ----------------
@jobs.route("/create_job", methods=["GET", "POST"])
@login_required
def create_job():
    # Instantiate the Create Job form
    form = CreateJobForm()

    # Check if the user is a recruiter
    if session["role"] == "Recruiter":
        # Check if user has submitted the form and all inputs are valid
        if form.validate_on_submit():
            company          = form.company.data.lower()
            position	     = form.position.data.lower()
            stack            = form.stack.data.lower()
            description      = form.description.data
            responsibilities = form.responsibilities.data
            requirements     = form.requirements.data
            salary		     = form.salary.data
            location	     = form.location.data.lower()
            contract         = form.contract.data.lower()
            level            = form.level.data.lower()
            posted_by        = session["username"]
            email            = session["email"]

            # Create an job instance using the form and insert into MongoDB
            job = Job(company, position, stack, description, responsibilities,
            requirements, salary, location, contract, level, posted_by, email)
            job.insert_into_database()

            flash("Congratulations! You have created a new job.")
            return redirect(url_for("main.home"))

        return render_template("create_job.html", form=form)

    flash("This page can only be accessed by recruiters.")
    return redirect(url_for("main.home"))


# --------------- View Applicants -----------------
@jobs.route("/<job_id>/applicants", methods=["GET", "POST"])
@login_required
def view_applicants(job_id):
    # Find job in MongoDB by its id
    job = Job.find_job_by_id(job_id)

    # Check if job exists
    if job:
        # Check if job was posted by this user
        if job["posted_by"] == session["username"]:
            #Find all applications in Mongo DB
            applications = Application.find_all_applications()
            return render_template("view_applicants.html", job=job, applications=applications)

        flash("This page can only be accessed by the poster.")
        return redirect(url_for("main.home"))

    flash("This job does not exist.")
    return redirect(url_for("main.home"))
