import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv("MONGO_URL"))
db = client.yourappdb


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        users = db.users
        existing_user = users.find_one({"name": request.form["username"]})

        if existing_user is None:
            # Hash the password for security
            hashed_pwd = generate_password_hash(request.form["password"])
            users.insert({"name": request.form["username"], "password": hashed_pwd})
            return redirect(url_for("login"))

        return "That username already exists!"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = db.users
        login_user = users.find_one({"name": request.form["username"]})

        if login_user:
            if check_password_hash(login_user["password"], request.form["password"]):
                return redirect(url_for("home"))

        return "Invalid username/password combination"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
