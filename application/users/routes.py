from flask import (
    flash, render_template, redirect, 
    request, session, url_for, Blueprint)
from application import mongo
from application.models import User
from application.users.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash


users = Blueprint('users', __name__)


# --------------- Register page ----------------
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit:
            username    = form.username.data.lower()
            email       = form.email.data.lower()
            password    = form.password.data
            location    = form.location.data
            description = form.description.data


            user = User(username, email, password, location, description)
            user.insert_into_database()


            # put the new user into 'session' cookie
            session['email'] = email
            flash("You have been registered successfully!")

            
            return redirect(url_for("profile", info=user.get_user_info))

        
    return render_template("register.html", form=form)


# --------------- Login page ----------------
@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.find_user_by_email(email=form.email.data)
            session["user"] = request.form.get("username").lower()
            flash("Welcome, {}".format(form.username.data))
            return redirect(url_for("profile", info=user.get_user_info))


        else:
            # username or password don't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("users.login"))


    return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("users.login"))


@users.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))
