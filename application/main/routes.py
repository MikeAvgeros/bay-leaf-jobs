from flask import render_template, Blueprint, flash, redirect, url_for
from application.main.forms import ContactForm
from application.models import Job, Contact


main = Blueprint('main', __name__, template_folder="templates")


# ------------ Index / Home page -------------
@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    jobs = Job.find_all_jobs()
    return render_template("home.html", jobs=jobs)


# --------------- Contact page ----------------
@main.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        name        = form.name.data.lower()
        email       = form.email.data.lower()
        message     = form.message.data
        user_id     = form.user_id.data

        contact = Contact(name, email, message, user_id)
        contact.insert_into_database()

        flash("Request submitted successfully")
        return redirect(url_for("main.home"))

    return render_template("contact.html", form=form)


# --------------- FAQ page ----------------
@main.route("/faq")
def faq():
    return render_template("faq.html")
