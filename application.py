# Deploy to Heroku: https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/

import os
import psycopg2 as SQL  # To connect to the database

from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

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


# Testing SQL database
@app.route("/sqltable")
def sqltable():
	# SQL query
	users = cur.execute("SELECT * FROM accounts;")
	users2 = cur.fetchall()
	for user in users2:
		print(user)
	# Return template, passing in result of SQL query
	return render_template("sqltable.html", users2=users2)


# Add new cards
@app.route("/add")  #Need to do POST method for submitting form
def add():
	return render_template("add.html")
