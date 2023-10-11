import os

from flask import Flask, flask, redirect, render_template, request, session
from flask_session import Session
from flask import flask
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from sqlalchemy import create_engine
from helpers import apology, login_reqired, lookup, used

app = Flask(_name_)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///finance.db")



