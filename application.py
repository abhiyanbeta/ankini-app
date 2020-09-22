import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# My own modules
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure database
db = SQL("postgres://xxdbvyyiutrzfh:5f34c27570b453c1bf7878ec081efdd290c5cefff7684fd75e9d55c946d91273@ec2-54-247-94-127.eu-west-1.compute.amazonaws.com:5432/d1r5sk71q9ge8f")

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


# Home page
@app.route("/")
@login_required
def index():
	notes = db.execute("""
		SELECT * FROM notes
		WHERE user_id=:user_id
	""", user_id=session["user_id"])




	return render_template("index.html", notes=notes)



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

		# Ensure email not already used
		check_user_exists = db.execute("SELECT * FROM users WHERE email = :email",
										email=request.form.get("email"))
		if len(check_user_exists) == 1:
			return apology("Email address already in use. Please enter another.")
		else:  # Email not in use so create new user
			# Hash the password
			hashed_password = generate_password_hash(request.form.get("password"))
			# Insert username and hashed password into users database
			db.execute("INSERT INTO users (email, password) VALUES (:email, :password)",
						email=request.form.get("email"), password=hashed_password)
			# Identify which user has just registered
			rows = db.execute("SELECT * FROM users WHERE email = :email",
							email=request.form.get("email"))
            # Log in just registered user
			session["user_id"] = rows[0]["user_id"]
            # Redirect user to home page
			return redirect("/")
	else:
		return render_template("signup.html")


# Log in
@app.route("/login", methods=["GET", "POST"])
def login():
	session.clear()  # Clear any pre-existing session
	# Error-checking for email and password
	if request.method == "POST":
		if not request.form.get("email"):
			return apology("Enter your email address")
		elif not request.form.get("password"):
			return apology("Enter your password")
		# Check if user exists and password is correct
		rows = db.execute("SELECT * FROM users WHERE email = :email",
							email=request.form.get("email"))
		if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
			return apology("Invalid email address or password")
		# Remember which user has logged in and redirect to homepage
		session["user_id"] = rows[0]["user_id"]
		return redirect("/")
	else:  # Page reached via GET method
		return render_template("login.html")

# Log out
@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")


# Add new cards
@app.route("/add", methods=["GET", "POST"])  #Need to do POST method for submitting form
@login_required
def add():
	if request.method == "POST":
		# Add note
		db.execute("""
			INSERT INTO notes (user_id, title, tag, body)
			VALUES (:user_id, :title, :tag, :body)
			""",
					user_id=session["user_id"],
					title=request.form.get("title"),
					tag=request.form.get("tag"),
					body=request.form.get("body")
					)
		flash("Added note!")
		return redirect("/add")

	else: # GET request
		return render_template("add.html")


# Edit new card -- need to prefill it with text from existing card
# TODO Atm anyone can visit note id by typing in URL, need to validate that user owns that note
@app.route("/edit/<note_id>", methods=["GET", "POST"])  #Need to do POST method for submitting form
@login_required
def edit(note_id):

	note = db.execute("""
		SELECT * FROM notes
		WHERE note_id=:note_id
	""", note_id=note_id)

	return render_template("edit.html", note=note)


@app.route("/edited", methods=["POST"])  #Need to do POST method for submitting form
@login_required
def edited():
	# IMPLEMENTING BEING ABLE TO EDIT NOTE


	return apology("TODO update edited note.")


# View the card
# TODO Atm anyone can visit note id by typing in URL, need to validate that user owns that note
@app.route("/view/<note_id>")
@login_required
def view(note_id):
	note = db.execute("""
		SELECT * FROM notes
		WHERE note_id=:note_id
	""", note_id=note_id)


	print(note_id)
	return render_template("view.html", note_id=note_id, note=note)

# Delete
@app.route("/delete/<note_id>", methods=['POST'])
@login_required
def delete(note_id):
    db.execute("""
		DELETE FROM notes
		WHERE note_id=:note_id
	""", note_id=note_id)
    flash('Deleted!')
    return redirect("/")



# Error handling
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
