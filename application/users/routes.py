from flask import (
    flash, render_template, redirect, 
    session, url_for, Blueprint)
from werkzeug.security import check_password_hash
from application.models import User, Job, Application
from application.security import login_required
from application.email import send_email
from config import Config
from application.users.forms import RegistrationForm, LoginForm, UpdateProfileForm


users = Blueprint('users', __name__, template_folder="templates")


# --------------- Register user ----------------
@users.route("/register", methods=["GET", "POST"])
def register():
    # Instantiate the registration form
    form = RegistrationForm()

    # Check if user hasn't already signed in
    if "username" not in session:
        # Check if user has submitted the form and all inputs are valid
        if form.validate_on_submit():
            username    = form.username.data
            email       = form.email.data
            password    = form.password.data
            location    = form.location.data
            role        = form.role.data
            picture     = ""

            # Find user in MongoDB by their username
            existing_user = User.find_user_by_username(username)

            # Check if username exists
            if existing_user:
                flash("Username already exists.")
                return redirect(url_for("users.register"))

            # Create an instance of User with the info the user submitter on the form
            user = User(username, email, password, location, role, picture)
            # Add user to MongoDB
            user.insert_into_database()

            # Send welcome email to user and notification to website owner
            sender_mail = Config.MAIL_USERNAME
            recipients = [sender_mail, email]
            for recipient in recipients:
                if recipient == sender_mail:
                    message = f"""
                    A new user has registered on the website.

                    Name: {username}

                    Email: {email}

                    Location: {location}

                    Role: {role}
                    """
                    send_email(recipient, message)

                elif recipient == email:
                    message = f"""
                    Hello {username}.
                    
                    Thank you for registering with bayleafjobs.

                    We are excited to have you join us and hope you have success in finding your perfect job!

                    The Team at bayleafjobs!
                    """
                    send_email(recipient, message)

            flash("You are registered successfully. You can now sign in.")
            return redirect(url_for("users.login"))

        return render_template("register.html", form=form)

    return redirect(url_for("users.profile", username=session["username"]))


# --------------- Log in user ----------------
@users.route("/login", methods=["GET", "POST"])
def login():
    # Instantiate the login form
    form = LoginForm()

    # Check if user hasn't already signed in
    if "username" not in session:
        # Check if user has submitted the form and all inputs are valid
        if form.validate_on_submit():
            email    = form.email.data
            password = form.password.data

            # Find user in MongoDB by their email
            user = User.find_user_by_email(email)

            # Check if user exists in MongoDB 
            if user:
                # Check if password is correct
                correct_password = user["password"]
                if check_password_hash(correct_password, password):
                    # Put user's info in session to be easily accessed
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

    return redirect(url_for("users.profile", username=session["username"]))


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

    # Check if user exists
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
        # Instantiate the update profile form
        form = UpdateProfileForm()

        # Check if user has submitted the form and all inputs are valid
        if form.validate_on_submit():
            username    = form.username.data
            email       = form.email.data
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
        form.username.data  = user["username"]
        form.email.data     = user["email"]
        form.location.data  = user["location"]
        form.picture.data  = user["picture"]

        return render_template("update_profile.html", form=form)

    flash("Please create an account.")
    return redirect(url_for("users.register"))


# --------------- Delete profile ----------------
@users.route("/profile/<username>/delete", methods=["GET", "POST"])
@login_required
def delete_profile(username):
    # Find user in MongoDB by their username
    user = User.find_user_by_username(username)
    
    # Check if user exists
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
