from flask import Flask
from flask import render_template # to render our html page
from flask import request # to get user input from form
import hashlib # included in Python library, no need to install
import psycopg2 # for database connection
import db

app = Flask(__name__)
conn = psycopg2.connect("postgresql://chantal:onehacks2022@free-tier6.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Donehacks-backend-2776")


@app.route("/")

def showForm():
    # show our html form to the user
    t_message = "Python and Postgres Registration Application"
    return render_template("register.html", message = t_message)

@app.route("/register", methods=["POST","GET"])
def register():
    # get user input from the html form
    t_email = request.form.get("t_email", "")
    t_password = request.form.get("t_password", "")

    # check for blanks
    if t_email == "":
        t_message = "Please fill in your email address"
        return render_template("register.html", message = t_message)

    if t_password == "":
        t_message = "Please fill in your password"
        return render_template("register.html", message = t_message)

    # hash the password they entered
    db.insert_activity(conn, t_email, t_password )
    t_message = "Your user account has been added."
    return render_template("register.html", message = t_message)

# this is for command line testing
if __name__ == "__main__":
    app.run(debug=True, port=8080)
