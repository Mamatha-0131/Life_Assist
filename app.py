import pickle
import base64
import numpy as np
import cv2
import face_recognition
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# -----------------------------
# CREATE FLASK APP
# -----------------------------
app = Flask(__name__)
app.secret_key = "lifeassist_secret_key"

# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lifeassist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------------
# DATABASE MODELS
# -----------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(100), nullable=False)


# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route("/")
def home():
    return render_template("voice_home.html")


# -----------------------------
# REGISTER ROUTE
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


# -----------------------------
# LOGIN ROUTE
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")
            return redirect(url_for("login"))

    return render_template("login.html")


# -----------------------------
# DASHBOARD ROUTE
# -----------------------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"])
    else:
        return redirect(url_for("login"))


# -----------------------------
# LOGOUT ROUTE
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


# -----------------------------
# ADD REMINDER ROUTE
# -----------------------------
@app.route("/add_reminder", methods=["POST"])
def add_reminder():
    data = request.get_json()
    title = data.get("title")
    time = data.get("time")

    if not title or not time:
        return jsonify({"message": "Missing data"}), 400

    new_reminder = Reminder(title=title, time=time)
    db.session.add(new_reminder)
    db.session.commit()

    return jsonify({"message": "Reminder added successfully"})


# -----------------------------
# ASK AI ROUTE
# -----------------------------
@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"answer": "Please ask something."})

    answer = "You asked: " + question

    return jsonify({"answer": answer})


# -----------------------------
# RUN APPLICATION (ALWAYS LAST)
# -----------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
