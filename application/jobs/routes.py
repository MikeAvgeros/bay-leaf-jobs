from flask import (render_template, request, redirect, session, 
                    url_for, flash, Blueprint)
from application.models import Application, Job
from application.security import login_required
from application.jobs.forms import CreateJobForm, UpdateJobForm, ApplicationForm
from config import Config
from datetime import datetime
import smtplib


jobs = Blueprint('jobs', __name__, template_folder="templates")


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
        query = request.form.get("search")
        jobs = Job.filter_jobs(query)

    return render_template("view_jobs.html", jobs=jobs)


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
            company          = form.company.data
            company_logo     = form.company_logo.data
            position	     = form.position.data
            location	     = form.location.data
            salary		     = form.salary.data
            level            = form.level.data
            stack            = form.stack.data
            contract         = form.contract.data
            description      = form.description.data
            posted_by        = session["username"]
            email            = session["email"]
            date_posted      = datetime.today().strftime('%d-%m-%Y')

            # Create an job instance using the form and insert into MongoDB
            job = Job(company, company_logo, position, 
            location, salary, level, stack, contract, 
            description, posted_by, email, date_posted)

            # Add job in MongoDB
            job.insert_into_database()

            flash("Congratulations! You have created a new job.")
            return redirect(url_for("main.home"))

        return render_template("create_job.html", form=form)

    flash("This page can only be accessed by recruiters.")
    return redirect(url_for("main.home"))


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
                company          = form.company.data
                company_logo     = form.company_logo.data
                position	     = form.position.data
                location	     = form.location.data 
                salary		     = form.salary.data             
                level            = form.level.data
                stack            = form.stack.data
                contract         = form.contract.data
                description      = form.description.data

                # Register info based on what the user submitted on the form
                updated_info = {
                    "company"          : company,
                    "company_logo"     : company_logo,
                    "position"         : position,
                    "location"         : location,
                    "salary"           : salary,
                    "level"            : level,
                    "stack"            : stack,
                    "contract"         : contract,
                    "description"      : description,
                    "posted_by"        : session["username"],
                    "email"            : session["email"]
                }

                # Update job's info using the registered updated info.
                Job.edit_job(job["_id"], updated_info)
                flash("The job has been updated!")
                return redirect(url_for("users.profile", username=session["username"]))

            # Populate form data based on existing job info        
            form.company.data          = job["company"]
            form.company_logo.data     = job["company_logo"]
            form.position.data         = job["position"]
            form.location.data         = job["location"]
            form.salary.data           = job["salary"]
            form.level.data            = job["level"]
            form.stack.data            = job["stack"]
            form.contract.data         = job["contract"]
            form.description.data      = job["description"]

            return render_template("update_job.html", form=form)

        flash("This job does not exist.")
        return redirect(url_for("main.home"))

    flash("This page can only be accessed by recruiters.")
    return redirect(url_for("main.home"))


# --------------- Delete job ----------------
@jobs.route("/job/<job_id>/delete", methods=["GET", "POST"])
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
                date_applied    = datetime.today().strftime('%Y-%m-%d')

                # Create an instance of Application with the info the user submitter on the form
                application = Application(notice_period, current_salary, 
                                        desired_salary, resume, cover_letter, 
                                        job_id, applicant, email, date_applied)

                # Add application in MongoDB
                application.insert_into_database()

                # Send confirmation to developer and notification to recruiter
                sender_mail = Config.MAIL_USERNAME
                password = Config.MAIL_PASSWORD
                recruiter = job["email"]
                recipients = [recruiter, email]
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.ehlo()
                server.starttls()
                server.login(sender_mail, password)
                for recipient in recipients:
                    if recipient == recruiter:
                        message = f"""
                        Hello {job["posted_by"]},

                        You have received a new application for the position of {job["position"]} at {job["company"]} by {applicant}.

                        You can view the applicant's detail on your profile page.
                        """
                        server.sendmail(sender_mail, recipient, message)

                    elif recipient == email:
                        message = f"""
                        Hello {applicant},

                        We have received your application for the position of {job["position"]} at {job["company"]}.
                        
                        Your details have been forwarded to the recruiter and they will be in touch should you meet their criteria.
                        """
                        server.sendmail(sender_mail, email, message)
                flash("Congratulations! Your application was sent successfully.")
                return redirect(url_for("main.home"))

            return render_template("job_application.html", form=form)

        flash("This page can only be accessed by recruiters.")
        return redirect(url_for("main.home"))

    flash("This job not longer exists")
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

