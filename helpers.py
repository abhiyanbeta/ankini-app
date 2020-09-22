from flask import redirect, render_template, session
from functools import wraps

# Renders message as apology to user
def apology(message, code=400):
    def escape(s):
        # Escape special characters
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


# Redirects user to login page if not logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
