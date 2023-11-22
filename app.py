import os
from PIL import Image
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

app = Flask(__name__)

username = None


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
    global username
    if request.method == "POST":
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            "SELECT * FROM users WHERE username = %s", (request.form["username"],)
        )
        existing_user = cur.fetchone()

        if existing_user is None:
            username = request.form["username"]
            image_count = list(str(abs(hash(username))))[:6]
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

@app.route("/portfolio", methods=["GET", "POST"])
def portfolio():
    global username
    print(request.method)
    if request.method == "POST":
        image_path = request.form("image_path")
        print(image_path)
        if not os.path.exists(f"static/{image_path}.jpg"):
            image = Image.open(image_path)
            image.save()
        else:
            image_path += str(abs(hash(image_path)))
    else:
        n_vals = len(os.listdir('static/work_images'))
        return render_template("portfolio.html", n_images=n_vals)

@app.route("/login", methods=["GET", "POST"])
def login():
    global username
    if request.method == "POST":
        username = request.form["username"]
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
    app.run(debug=True, port=8000)
