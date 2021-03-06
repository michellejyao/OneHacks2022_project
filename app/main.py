import logging
from typing import Counter
from flask import Flask
from flask import render_template # to render our html page
from flask import request # to get user input from form
from flask import Flask, session, redirect, url_for, escape, request

import hashlib # included in Python library, no need to install
import psycopg2 # for database connection
import db

app = Flask(__name__)
app.secret_key = "27eduCBA09"
conn = psycopg2.connect("postgresql://chantal:onehacks2022@free-tier6.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Donehacks-backend-2776")

@app.route("/")
def website():
    return render_template("Website.html")

@app.route("/about")
def about():
    return render_template("About.html")

@app.route("/Contact")
def contact():
    return render_template("Contact.html")

@app.route("/Sign-in", methods=["POST", "GET"])
def signin():
    if request.method == 'POST':
       
        t_email = request.form.get("t_Email", "")
        t_password = request.form.get("t_Password", "")
        db.validate_login(conn, email=t_email, password=t_password)
        session['password'] = t_password
        return redirect(url_for("counter_init"))
    return render_template("sign-in.html")

        
@app.route('/count', methods=['GET', 'POST'])
def count_up():
    if "password" in session:
        password_result = session['password']
        db.insertCounter(conn, password=password_result, counter=2)
        print(password_result)
        return redirect(url_for("website"))
    else:
        return redirect(url_for("signin"))


@app.route("/run")

def showForm():
    # show our html form to the user
    t_message = "Python and Postgres Registration Application"
    return render_template("register.html")

@app.route("/register", methods=["POST","GET"])
def register():
    # get user input from the html form
    t_username = request.form.get("t_Username", "")
    t_email = request.form.get("t_Email", "")
    t_password = request.form.get("t_Password", "")

    # # check for blanks
    if t_email == "":
        t_message = "Please fill in your email address"
        return render_template("register.html")

    if t_password == "":
        t_message = "Please fill in your password"
        return render_template("register.html")

    # hash the password they entered
    db.insert_user(conn, email=t_email, password=t_password, username=t_username)
    t_message = "Your user account has been added."
    return render_template("register.html")

@app.route('/counter', methods = ['GET', 'POST'])
def counter_init():
    return render_template("Recycle_Counter.html")

@app.route('/no')
def back():
    return redirect(url_for('website'))

@app.route('/leaderboard', methods=['POST', 'GET'])
def leaderboard():
    results = db.leaderboard(conn)

    usernames = []
    for result in results:
      usernames.append(result[0])
    counts = []
    for result in results:
        counts.append(result[1])

    return render_template('Leaderboard.html', usernames=usernames, counts=counts)





    
    
#db.insertCounter(conn, username=session_user, counter=t_counter)

     
  
# this is for command line testing
if __name__ == "__main__":
    app.run(debug=True)
