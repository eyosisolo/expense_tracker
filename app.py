from flask import Flask, render_template, request
from database import get_connection

app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
            """)

            cursor.execute(
                """
                INSERT INTO users(username, password)
                VALUES (?, ?)
                """,
                (username, password)
            )

            connection.commit()

        finally:
            connection.close()

        return "Registration Successful!"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (username, password)
        )

        user = cursor.fetchone()

        connection.close()

        if user:

            return render_template("dashboard.html")

        return "Invalid username or password."

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)