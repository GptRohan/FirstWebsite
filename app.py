

ADMIN_USER = "admin"
ADMIN_PASS = "1234"


from flask import Flask, render_template, request

import sqlite3

def init_db():
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("contact.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        return "Message saved successfully!"

    return render_template("contact.html")

from flask import request, redirect, url_for

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        if user == ADMIN_USER and pwd == ADMIN_PASS:
            conn = sqlite3.connect("contact.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name, email, message FROM messages")
            data = cursor.fetchall()
            conn.close()

            return render_template("admin.html", messages=data)
        else:
            return "Access Denied"

    return render_template("admin_login.html")


if __name__ == "__main__":
    init_db()
    app.run()