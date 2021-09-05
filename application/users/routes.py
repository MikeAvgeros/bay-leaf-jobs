from flask import (
    flash, render_template, redirect, 
    session, url_for, Blueprint)
from werkzeug.security import check_password_hash
from application.models import User, Job, Application
from functools import wraps
from application.users.forms import RegistrationForm, LoginForm, UpdateProfileForm


users = Blueprint('users', __name__, template_folder="templates")


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


# --------------- Register user ----------------
@users.route("/register", methods=["GET", "POST"])
def register():
    # Instantiate the registration form
    form = RegistrationForm()

    # Check if user has submitted the form and all inputs are valid
    if form.validate_on_submit():
        username    = form.username.data.lower()
        email       = form.email.data.lower()
        password    = form.password.data
        location    = form.location.data
        role        = form.role.data

        # Check if username exists
        existing_user = User.find_user_by_username(username)
        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("users.register"))

        # Create an instance of User with the info the user submitter on the form
        user = User(username, email, password, location, role)
        user.insert_into_database()
        flash("You are registered successfully. You can now sign in.")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


# --------------- Log in user ----------------
@users.route("/login", methods=["GET", "POST"])
def login():
    # Instantiate the login form
    form = LoginForm()

    # Check if user has submitted the form and all inputs are valid
    if form.validate_on_submit():
        email    = form.email.data.lower()
        password = form.password.data

        # Check if user exists in MongoDB using their email
        user = User.find_user_by_email(email)

        if user:
            # Check if password is correct
            correct_password = user["password"]
            if check_password_hash(correct_password, password):
                # Put user's info in session
                session["email"] = user["email"]
                session["role"] = user["role"]
                session["username"] = user["username"]
                return redirect(url_for("users.profile", username=session["username"]))
            else:
                form.password.errors.append("Incorrect password")
        else:
            flash("Incorrect email and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", form=form)


# --------------- Log out user ----------------
@users.route("/logout")
@login_required
def logout():
    # Remove user's info from session cookie
    session.pop("email", None)
    session.pop("role", None)
    session.pop("username", None)
    flash("You are logged out")
    return redirect(url_for("main.home"))


# --------------- Profile page ----------------
@users.route("/profile/<username>", methods=["GET", "POST"])
@login_required
def profile(username):
    # Find user in MongoDB by their username
    user = User.find_user_by_username(username)

    if user:
        # Find all jobs and applications and pass them to the profile page
        jobs = Job.find_all_jobs()
        applications = Application.find_all_applications()
        return render_template("profile.html", username=session["username"], 
                            user=user, jobs=jobs, applications=applications)

    flash("Please create an account.")
    return redirect(url_for("users.register"))


# --------------- Update profile ----------------
@users.route("/profile/<username>/update", methods=["GET", "POST"])
@login_required
def update_profile(username):
    # Find user in MongoDB by their username
    user = User.find_user_by_username(username)

    # Check if user exists in MongoDB
    if user:
        # Instantiate the updateprofile form
        form = UpdateProfileForm()

        # Check if user has submitted the form and all inputs are valid
        if form.validate_on_submit():
            username    = form.username.data.lower()
            email       = form.email.data.lower()
            location    = form.location.data
            picture     = form.picture.data

            # Register info based on what the user submitted on the form
            updated_info = {
                "username" : username,
                "email"    : email,
                "location" : location,
                "picture"  : picture
            }

            # Update user's info using the registered updated info.
            User.edit_user(user["_id"], updated_info)

            # Update email and username in session
            session["email"] = email
            session["username"] = username
            flash("Your profile has been updated!")

            return redirect(url_for("users.profile", username=session["username"]))
            
        # Populate form data based on existing user info
        form.username.data  = user["username"].capitalize()
        form.email.data     = user["email"]
        form.location.data  = user["location"].capitalize()

        return render_template("update_profile.html", form=form)

    flash("Please create an account.")
    return redirect(url_for("users.register"))


# --------------- Delete profile ----------------
@users.route("/profile/<username>/delete", methods=["GET", "POST"])
@login_required
def delete_profile(username):
    # Check if job exists in MongoDB
    user = User.find_user_by_username(username)

    if user:
        # Delete user from MongoDB and remove info from session
        user_id = user["_id"]
        User.delete_user(user_id)
        session.pop("email", None)
        session.pop("role", None)
        session.pop("username", None)
        flash("You profile had been successfully deleted")
        return redirect(url_for("main.home"))

    flash("This user does not exist")
    return redirect(url_for("main.home"))

