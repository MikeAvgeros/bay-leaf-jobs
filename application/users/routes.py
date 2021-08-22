from flask import (
    flash, render_template, redirect, 
    request, session, url_for, Blueprint)
from application import mongo
from werkzeug.security import generate_password_hash, check_password_hash


users = Blueprint('users', __name__)


# --------------- Check if user exists in DB ----------------
def existing_user():
    return mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})


# --------------- Check if password is valid ----------------
def password_is_valid(existing_user):
    return check_password_hash(
        existing_user["password"], request.form.get("password"))


# --------------- Register page ----------------
@users.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if existing_user():
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }

        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("You have been registered successfully!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# --------------- Login page ----------------
@users.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = existing_user()

        if user:
            # check if password matches
            if password_is_valid(user):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@users.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@users.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))
