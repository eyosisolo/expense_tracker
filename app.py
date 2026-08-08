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

           expenses = get_all_expenses()

           total = get_total_expenses()

           return render_template("dashboard.html",expenses=expenses, total=total)

        return "Invalid username or password."

    return render_template("login.html")
@app.route("/add_expense", methods=["GET", "POST"])
def add_expense():

    if request.method == "POST":

        title = request.form["title"]

        amount = float(request.form["amount"])

        category = request.form["category"]

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO expenses(title, amount, category)
            VALUES (?, ?, ?)
            """,
            (title, amount, category)
        )

        connection.commit()

        connection.close()

        return "Expense Added Successfully!"

    return render_template("add_expense.html")

def create_expense_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL
    )
    """)
    connection.commit()
    connection.close()

def get_all_expenses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, title, amount, category
    FROM expenses
    ORDER BY id DESC
    """)
    expenses = cursor.fetchall()
    connection.close()
    return expenses

def get_total_expenses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT SUM(amount)
    FROM expenses
    """)

    total = cursor.fetchone()[0]
    connection.close()

    if total is None:
        return 0.0

    return total


@app.route("/delete/<int:id>")
def delete_expense(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (id,)
    )

    connection.commit()
    connection.close()

    return "Expense deleted successfully."

if __name__ == "__main__":
    app.run(debug=True)