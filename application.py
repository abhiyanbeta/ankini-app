import os
import psycopg2 as SQL  # To connect to the database

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# My own modules
from helpers import apology

# Configure application
app = Flask(__name__)

# Configure database
db = SQL.connect("postgres://xxdbvyyiutrzfh:5f34c27570b453c1bf7878ec081efdd290c5cefff7684fd75e9d55c946d91273@ec2-54-247-94-127.eu-west-1.compute.amazonaws.com:5432/d1r5sk71q9ge8f")
cur = db.cursor()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
# Session uses filesystem instead of signed cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response



# Configure SQL database
'''
TODO
'''

# Index page
@app.route("/")
def index():
	return render_template("index.html")

# Password validation
def validate(password):
	import re  # Regular expressions
	if len(password) < 6:
		return apology("Password must be at least 6 characters")
	elif not re.search("[0-9]", password):  # No number entered
		return apology("Password must contain at least one number")



@app.route("/signup", methods=["GET", "POST"])
def register():
	if request.method == "POST":  # TODO if user tries to register
		# -- Error checking for email and password --
		# Validate password complexity
		validation_errors = validate(request.form.get("password"))
        # Ensure username was submitted
		if not request.form.get("email"):
			return apology("You must provide an email address")
        # Ensure password was submitted
		elif not request.form.get("password"):
			return apology("You must provide a password")
		elif validation_errors:  # Validate password complexity
			return validation_errors
		elif not request.form.get("confirmation"):
			return apology("You must re-type your password")
		elif not request.form.get("password") == request.form.get("confirmation"):
			return apology("Your passwords do not match.")

		# -- Passed error-checking - proceed to create user --
		# Hash the password
		hashed_password = generate_password_hash(request.form.get("password"))
		# Insert username and hashed password into users database
		cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (request.form.get("email"), hashed_password))
		db.commit()  # Ensures SQL command executes
		return apology("User created. Please log in.")



	else:
		return render_template("signup.html")


# Testing SQL database
@app.route("/sqltable")
def sqltable():
	# SQL query
	cur.execute("SELECT * FROM accounts;")
	users = cur.fetchall()
	# Return template, passing in result of SQL query
	return render_template("sqltable.html", users=users)


# Add new cards
@app.route("/add")  #Need to do POST method for submitting form
def add():
	return render_template("add.html")


# Edit new card -- need to prefill it with text from existing card
@app.route("/edit")  #Need to do POST method for submitting form
def edit():
	return render_template("edit.html")
