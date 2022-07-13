from functools import wraps
from flask import redirect, session, render_template

def apology(message, code=400):
    #Render message as an apology to user.

    return render_template("error.html", code=code, message=message), code

# Code from: https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None: # This part is from CS50 finance
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function