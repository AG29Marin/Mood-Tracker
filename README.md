# MOOD TRACKER
#### Link: <https://mood-tracker-web-app.herokuapp.com/>
#### Description: Web app that keeps track of your mood created with Flask and SQL

## Table of contents
* [General info](#general-info)
* [Project structure](#project-structure)
* [Technologies](#technologies)
* [Sources](#sources)

## General info
This project is a web application that keeps track of your mood by generating a graph based on a score you get after you answer some questions and the date on which you answered them. It also offers you advice on how to improve or maintain your emotional state.

## Project structure

### mood.db
This is the SQL database I've created to save the user and tracker information. It contains two tables named *users* and *tracking*.
The *users* table contains 4 rows for id, username, hash(password), and email.
The *tracking* table contains 4 rows for id, user_id, info(score), and date.
### app.py
Contains 7 functions:

The *register* function gets the information sent by the user in the HTML *register* form and saves it in the database. Redirects to the login template.

The *login* function gets the username and password from the HTML *login* form, verifies them with the info in the database, and login (or not) the user. Redirects to the mood template.

The *logout* function clears the session. Redirects to the login template.

The *mood* function requires login, gets the information from the HTML form, converts the info into a score, makes the necessary calculations for the final score, and stores this information and the submit date into the *tracking* table from the database. Redirects to the graph template.

The *graph* function gets the score and the date from the tracking table, creates the necessary values for the graphic, and converts the score into labels: excellent, good, average, and poor. The values are inserted into the graphic template using Jinja.

The *advice* function requires login and returns the HTML advice page.

The *home* function doesn't require login. Returns the HTML home page.

The project uses sessions instead of cookies.

### help.py
Contains 2 functions. One is for the login requirment and the second is for generating a 400 error message when something goes wrong.

### Templates
Contains 8 templates:

The HTML *layout* template contains the navbar and the basic html layout of the web app.

The HTML *error* template contains the 400 error message using Jinja.

The HTML *home* template contains the title of the web app and the image used for the presentation.

The HTML *register* template contains a form that asks the user for input on username, email, password, and password confirmation. The password has to be at least 8 letters long, has at least one uppercase letter, and at least one number.

The HTML *login* template contains also a form that asks the user for input on username and password.

The HTML *mood_track* template contains the form with questions that the user has to answer. Based on the answers, the *mood* function will make a score that will be inserted into the database. There are 9 questions in total and the type of input is radio.

The HTML *graph* template contains a flash of the score and the mood(excellent, good, average, and poor) and a Chart.js graphic that takes the score and date values with Jinja from app.py and then presents them in the graph.

The HTML *advice* template contains several youtube videos using iframe that advise on how to cope with anxiety, depression, how to sleep better, and how to have a social life.

## Static
Contains the styles.css and 2 images. One is used in the home template and the other in the error template.

In styles.css is where you can find the code for styling all the web app pages.

## Technologies
Project is created with:
* Python3.10
* Flask2
* SQL, SQLITE
* CS50 Library
* HTML5
* CSS3
* JavaScript
* Jinja2

## Sources
### For app.py:

CS50 Finance;

Auto-reload templates from: https://stackoverflow.com/questions/9508667/reload-flask-app-when-template-file-changes;

Configure Session from: https://www.geeksforgeeks.org/how-to-use-flask-session-in-python-flask/;

Configure CS50 Library to use SQLite database from: CS50 Finance;

Making sure responses are no-cache. More info at: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control
code from: https://stackoverflow.com/questions/34066804/disabling-caching-in-flask;

*Login* function: code is from CS50 Finance;

*Logout* function: code is from CS50 Finance;

*Register* function: some of the code is from my own work on CS50 Finance.

### For help.py:

Code from: https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/ and CS50 Finance.

### For the *graph* template:

Code from: https://www.chartjs3.com/docs/chart/getting-started/.

### For the *layout*, *register*, *login* templates:

Some of the code is from CS50 Finance.

### For styles.css:

Styling the log in and registration forms. Code inspiration from: https://www.youtube.com/watch?v=kRs3aTi3pzU&ab_channel=WebMaster;

Styling the advice page. Code inspiration from: https://www.youtube.com/watch?v=0L8cQ9nRtuE&ab_channel=ADesignerWhoCodes;

All animations are from: https://webcode.tools/generators/css/keyframe-animation.

