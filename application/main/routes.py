from config import Config
from flask import render_template, Blueprint, flash, redirect, url_for
from application.main.forms import ContactForm
import smtplib


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
        name        = form.name.data
        email       = form.email.data
        body        = form.body.data

        sender_mail = Config.MAIL_USERNAME
        password = Config.MAIL_PASSWORD
        recipients = [sender_mail, email]
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(sender_mail, password)
        for recipient in recipients:
            if recipient == sender_mail:
                message = f"""
                You have a new message from the website.

                Name: {name}

                Email: {email}

                Message: {body}
                """
                server.sendmail(sender_mail, recipient, message)

            elif recipient == email:
                message = f"""
                Hello {name}.

                Thank you for getting in touch with bayleafjobs.
                
                We'll aim to reply within the next 2 working days.
                """
                server.sendmail(sender_mail, recipient, message)

        flash("Your message was submitted successfully")
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
