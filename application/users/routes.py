from flask import (
    flash, render_template, redirect, 
    session, url_for, Blueprint)
from werkzeug.security import check_password_hash
from application.models import User
from application.users.forms import RegistrationForm, LoginForm, UpdateProfileForm


users = Blueprint('users', __name__, template_folder="templates")


# --------------- Register page ----------------
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

        # Create an instance of User with the info the user submitter on the form
        user = User(username, email, password, location, role)
        user.insert_into_database()
        flash("You are registered successfully")
        return redirect(url_for("main.home"))

    return render_template("register.html", form=form)


# --------------- Login page ----------------
@users.route("/login", methods=["GET", "POST"])
def login():
    # Instantiate the login form
    form = LoginForm()

    # Check if user has submitted the form and all inputs are valid
    if form.validate_on_submit():
        email    = form.email.data.lower()
        password = form.password.data

        # Check if user exists in MongoDB
        user = User.find_user_by_email(email)

        if user:
            # Check if password is correct
            correct_password = user["password"]
            if check_password_hash(correct_password, password):
                # Put user's info in session
                session["email"] = email
                session["role"] = user["role"]
                session["username"] = user["username"]
                return redirect(url_for("main.home"))
            else:
                form.password.errors.append("Incorrect password")
        else:
            flash("Incorrect email and/or password")
            return redirect(url_for("users.login"))

    return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    # Remove user's info from session cookie
    session.pop("email", None)
    session.pop("role", None)
    session.pop("username", None)
    flash("You are logged out")
    return redirect(url_for("main.home"))


@users.route("/profile", methods=["GET", "POST"])
def profile():
    # Find user in MongoDB
    user = User.find_user_by_email(session["email"])
    if user:
        return render_template("profile.html", user=user)

    return render_template("login.html")


@users.route("/profile/update", methods=["GET", "POST"])
def update_profile():
    # Instantiate the updateprofile form
    form = UpdateProfileForm()

    # Check if user has submitted the form and all inputs are valid
    if form.validate_on_submit():
        username    = form.username.data.lower()
        email       = form.email.data.lower()
        location    = form.location.data
        picture     = form.picture.data

        updated_info = {
            "username" : username,
            "email"    : email,
            "location" : location,
            "picture"  : picture
        }

        # Find user in MongoDB and update their info based on the submitted form
        user = User.find_user_by_email(session["email"])
        User.edit_user(user["_id"], updated_info)
        session["email"] = email
        session["username"] = username
        flash("Your profile has been updated!")
        return redirect(url_for("users.profile", user=user))

    return render_template("update_profile.html", form=form)
