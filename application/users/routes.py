from flask import (
    flash, render_template, redirect, 
    request, session, url_for, Blueprint)
from werkzeug.security import check_password_hash
from application import mongo
from application.models import User
from application.users.forms import RegistrationForm, LoginForm


users = Blueprint('users', __name__, template_folder="templates")


# --------------- Register page ----------------
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit:
            username    = form.username.data.lower()
            email       = form.email.data.lower()
            password    = form.password.data
            location    = form.location.data.lower()
            experience  = form.experience.data

            user = User(username, email, password, location, experience)
            user.insert_into_database()

            flash("You are registered successfully")
            session['email'] = email
            return redirect(url_for("main.home"))

    return render_template("register.html", form=form)


# --------------- Login page ----------------
@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            email    = form.email.data
            password = form.password.data

            # Check if user exists in DB
            user = User.find_user_by_email(email.lower())

            if user:
                correct_password = user["password"]
                if check_password_hash(correct_password, password):
                    # put user in session
                    session["email"] = email.lower()
                    flash("You are successfully logged in.")
                    return redirect(url_for("main.home"))
                else:
                    form.password.errors.append("Incorrect password")
            else:
                flash("Incorrect email and/or password")
                return redirect(url_for("users.login"))

    return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    # remove user from session cookie
    session.pop("email", None)
    flash("You are logged out")
    return redirect(url_for("main.home"))


@users.route("/profile", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))
