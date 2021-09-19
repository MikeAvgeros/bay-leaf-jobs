from functools import wraps
from flask import (flash, redirect,
                   session, url_for)


# ---------- Login required security -----------
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # Checks if email is in session to verify is user has signed in
        if "email" in session:
            return f(*args, **kwargs)
        else:
            flash("You must sign in to access this page!")
            return redirect(url_for("users.login"))

    return wrap
