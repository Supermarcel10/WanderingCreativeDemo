import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)


# Establish a connection to the PostgreSQL database
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return conn


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "SELECT * FROM users WHERE username = %s", (request.form["username"],)
        )
        existing_user = cur.fetchone()

        if existing_user is None:
            # Hash the password for security
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (request.form["username"], request.form["password"]),
            )
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for("login"))

        cur.close()
        conn.close()
        return "That username already exists!"

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "SELECT * FROM users WHERE username = %s", (request.form["username"],)
        )
        login_user = cur.fetchone()

        if login_user and login_user["password"] == request.form["password"]:
            cur.close()
            conn.close()
            return redirect(url_for("home"))

        cur.close()
        conn.close()
        return "Invalid username/password combination"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
