import os

from flask import Flask, flask, redirect, render_template, request, session
from flask_session import Session
from flask import flask
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from sqlalchemy import create_engine
from helpers import apology, login_reqired, lookup, used

app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods = ["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POSt ( as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("Username"):
            return apology("Username is mandatory", 403)

        elif not request.form.get("Password"):
            return apology("Password is mandatory", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("incorrect username and/or password",403)
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


