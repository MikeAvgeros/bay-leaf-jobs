import os
from flask import render_template, Blueprint, flash, redirect, url_for
from application.main.forms import ContactForm
from application.models import Job
from application import mail
from flask_mail import Message


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
        body        = form.body.data

        sender_email = os.environ.get('MAIL_DEFAULT_SENDER')
        recipients = [sender_email, email]
        for recipient in recipients:
            if recipient == sender_email:
                message = (f"<h3>Hello</h3>"
                            "<p>Message from the website:</p>"
                            f"<p><b>Name:</b> {name}</p> "
                            f"<p><b>Email:</b> {email}</p> "
                            f"<p><b>Message:</b> {body} </p>")
                subject = f"New query from: {name}"

            elif recipient == email:
                message = (f"<h3>Hello {name},</h3>"
                            "<p>We have received your message and aim"
                            " to respond within the next 3 working days."
                            "</p>"
                            "<p>All the best,</p>"
                            "<p>The team at bayleafjobs</p>"
                            )
                subject = 'Thank your for getting in touch!'

            msg = Message(recipients=[recipient],
                        html=message,
                        subject=subject)

            mail.send(msg)

        flash("Request submitted successfully")
        return redirect(url_for("main.home"))

    return render_template("contact.html", form=form)


# --------------- FAQ page ----------------
@main.route("/faq")
def faq():
    return render_template("faq.html")


# --------------- Privacy page ----------------
@main.route("/privacy")
def privacy():
    return render_template("privacy.html")


# --------------- Terms & Conditions page ----------------
@main.route("/terms")
def terms():
    return render_template("terms.html")
