from flask import render_template, request, Blueprint


main = Blueprint('main', __name__, template_folder="templates")


# ------------ Index / Home page -------------
@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    return render_template("home.html")


# --------------- About page ----------------
@main.route("/about")
def about():
    return render_template("about.html")


# --------------- Contact page ----------------
@main.route("/contact")
def contact():
    return render_template("contact.html")


# --------------- FAQ page ----------------
@main.route("/faq")
def faq():
    return render_template("faq.html")
