import re
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
from help import apology, login_required


app = Flask(__name__)

# Auto-reload templates from: https://stackoverflow.com/questions/9508667/reload-flask-app-when-template-file-changes

app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configure Session from: https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database from: CS50 finance

#db = SQL("sqlite:///mood.db")

uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://qszzqwqlolsjdz:00bfaa225eb84e60ab689eeefeb0ef5637fa7d018503168605e63a326d83f873@ec2-54-77-40-202.eu-west-1.compute.amazonaws.com:5432/d5vnsnmdjj7n00"):
    uri = uri.replace("postgres://qszzqwqlolsjdz:00bfaa225eb84e60ab689eeefeb0ef5637fa7d018503168605e63a326d83f873@ec2-54-77-40-202.eu-west-1.compute.amazonaws.com:5432/d5vnsnmdjj7n00", "postgresql://qszzqwqlolsjdz:00bfaa225eb84e60ab689eeefeb0ef5637fa7d018503168605e63a326d83f873@ec2-54-77-40-202.eu-west-1.compute.amazonaws.com:5432/d5vnsnmdjj7n00")
db = SQL(uri)

''' Making sure responses are no-cache. More info at: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
code from: https://stackoverflow.com/questions/34066804/disabling-caching-in-flask '''

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


# Rendering the home page
@app.route("/")
def home():

    return render_template("home.html")

# Rendering advice page
@app.route("/advice")
@login_required
def advice():

    # Making sure the user is logged in
    user_id = session["user_id"]

    if not user_id:
        return redirect("/login")
    else:
        return render_template("advice.html")

# rendering the graph page
@app.route("/graph")
@login_required
def graph():

    user_id = session["user_id"]

    # Query for selecting the score and date from tracking table
    user_info = db.execute("SELECT info FROM tracking WHERE user_id = ?", user_id)
    time = db.execute("SELECT date FROM tracking WHERE user_id = ?", user_id)

    # Making the graph
    value = [row["info"] for row in user_info]
    label = [row["date"] for row in time]

    # Putting a label on the score
    for row in user_info:
        row = row["info"]
        if row == 0 and row <= 9:
            score = "POOR"
        elif row >= 9 and row <= 27:
            score = "AVERAGE"
        elif row >= 27 and row < 45:
            score = "GOOD"
        else:
            score = "EXCELLENT"

    # Flashing the score with the label
    flash("My mood is " + score + "! I've got " + str(row) + " out of 45. ")

    # Render graph
    return render_template("graph.html", label=label, value=value, score=score)

@app.route("/mood", methods=["GET", "POST"])
@login_required
def mood():

    # User reached route via POST
    if request.method == "POST":
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        option5 = request.form.get("option5")
        option6 = request.form.get("option6")
        option7 = request.form.get("option7")
        option8 = request.form.get("option8")
        option9 = request.form.get("option9")

        # Putting the info into a list for better access
        options = [option1, option2, option3, option4, option5, option6, option7, option8, option9]

        # Making sure all the questions are answered
        if not option1:
            return apology("Please answer all the questions!", 400)
        if not option2:
            return apology("Please answer all the questions!", 400)
        if not option3:
            return apology("Please answer all the questions!", 400)
        if not option4:
            return apology("Please answer all the questions!", 400)
        if not option5:
            return apology("Please answer all the questions!", 400)
        if not option6:
            return apology("Please answer all the questions!", 400)
        if not option7:
            return apology("Please answer all the questions!", 400)
        if not option8:
            return apology("Please answer all the questions!", 400)
        if not option9:
            return apology("Please answer all the questions!", 400)

        # Variable for counting the score
        counter = 0

        # Variable for current date
        dates = date.today()
        # Variable for printing date as a string
        date_today = dates.strftime("%m/%d/%Y")

        # String variables for counting the score
        response1 = 'excellent' #45
        response2 = 'good' #27
        response3 = 'average' #9
        response4 = 'poor' #0

        # Counting the score
        for item in options:
            if item == response1:
                counter += 5
            elif item == response2:
                counter += 3
            elif item == response3:
                counter += 1
            elif item == response4:
                counter += 0

        # Creating tracking table:
        '''CREATE TABLE 'tracking' ('id' INTEGER PRIMARY KEY NOT NULL,
         'user_id' INTEGER NOT NULL,
         'info' INTEGER NOT NULL,
         'date' TEXT NOT NULL); '''

        # Query for inserting the info into database
        user_id = session["user_id"]
        db.execute("INSERT INTO tracking (user_id, info, date) VALUES(?, ?, ?)",
            user_id, counter, date_today)

        # Redirecting to the graph that shows the user emotional state based on the score
        return redirect("/graph")

    # User reached route via GET
    else:
        return render_template("mood_track.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    # This code is from CS50 FINANCE
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("Must provide username", 400)
        if not password:
            return apology("Must provide password", 400)

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password", 400)

        session["user_id"] = rows[0]["id"]

        return redirect("/mood")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():

    # This code is from CS50 FINANCE
    #Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget previous user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        email = request.form.get("email")

        # Ensure username was submited
        if not username:
            return apology("Must provide username", 400)
        # Ensure email was submited
        if not email:
            return apology("Please provide a valid email address!", 400)
        # Ensure password was submited
        if not password:
            return apology("Must provide password", 400)

        # Implementing the password: https://stackoverflow.com/questions/41117733/validation-of-a-password-python
        if len(password) < 8:
            return apology("Password must be at least 8 letters long", 400)

        elif re.search('[0-9]', password) is None:
            return apology("Password must contain a number", 400)

        elif re.search('[A-Z]', password) is None:
            return apology("Password must contain a capital letter!", 400)

        # Ensure the password matches
        if confirm != password:
            return apology("No match", 400)

        # Creating users table:
        '''CREATE TABLE 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        'username' TEXT NOT NULL,
        'hash' TEXT NOT NULL,
        'email' TEXT NOT NULL );
        CREATE UNIQUE INDEX 'username' ON "users" ("username" ASC) WHERE username;
        ); '''

        # Query for inserting the user information into the database
        try:
            db.execute("INSERT INTO users(username, hash, email) VALUES(:username, :hash, :email)",
                        username=request.form.get("username"),
                        hash=generate_password_hash(password),
                        email=request.form.get("email"))


            return redirect("/login")
        except:
            return apology("Username already in use", 400)

    # User reached route via GET
    else:
        return render_template("register.html")