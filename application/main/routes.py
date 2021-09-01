from flask import render_template, Blueprint, flash, redirect, url_for
from application.main.forms import ContactForm
from application.models import Contact


main = Blueprint('main', __name__, template_folder="templates")


# ------------ Index / Home page -------------
@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    return render_template("home.html")


# --------------- Contact page ----------------
@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name        = form.name.data.lower()
        email       = form.email.data.lower()
        description = form.description.data

        contact = Contact(name, email, description)
        contact.insert_into_database()

        flash("Request submitted successfully")
        return redirect(url_for("main.home"))

    return render_template("contact.html", form=form)


# --------------- FAQ page ----------------
@main.route("/faq")
def faq():
    return render_template("faq.html")
