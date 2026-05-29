from flask import Flask, request, g, render_template, redirect
import sqlite3, os

DB_PATH = "hr.db"
app = Flask(__name__)

# ---------------- DB HANDLING ----------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db:
        db.close()

def init_db():
    if os.path.exists(DB_PATH):
        return
    db = sqlite3.connect(DB_PATH)
    c = db.cursor()

    c.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        notes TEXT
    )
    """)

    c.execute("""
    CREATE TABLE kpis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        metric TEXT,
        value INTEGER
    )
    """)

    employees = [
        ("Alice", "Engineer", "Normal employee"),
        ("Bob", "HR", "Normal employee"),
        ("Charlie", "Manager", "Normal employee"),
        ("Dana", "Analyst", "Normal employee"),
        ("Eve", "CTO", "SecurinetsENIT{URL_3NC0D1NG_I5_C00L}")
    ]

    c.executemany("INSERT INTO employees (name, position, notes) VALUES (?, ?, ?)", employees)
    db.commit()
    db.close()

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/employees")
def employees():
    db = get_db()
    rows = db.execute("SELECT id, name, position FROM employees").fetchall()
    return render_template("employees.html", employees=rows)

from urllib.parse import unquote

from urllib.parse import unquote

@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        raw_name = request.form.get("name", "")

        # ❌ Reject raw attack
        if raw_name == "' OR 1=1 --":
            return "Not so fast !", 400

        # ✅ Only now decode (this enables the vuln)
        name = unquote(raw_name)

        db = get_db()

        # 🚨 INTENTIONAL SQL INJECTION (URL-ENCODED ONLY) 🚨
        # name is intentionally NOT re-quoted after decode
        sql = "SELECT * FROM employees WHERE name = '" + name + "'"

        try:
            rows = db.execute(sql).fetchall()

            output = "<h2>Query Results</h2><br>"
            for row in rows:
                output += (
                    f"ID: {row['id']} | "
                    f"Name: {row['name']} | "
                    f"Position: {row['position']} | "
                    f"Notes: {row['notes']}<br>"
                )

            return output if rows else "No results."

        except Exception as e:
            return "SQL Error: " + str(e)

    return render_template("add.html")


@app.route("/kpi", methods=["GET", "POST"])
def add_kpi():
    if request.method == "POST":
        employee_id = request.form.get("employee_id")
        metric = request.form.get("metric")
        value = request.form.get("value")

        db = get_db()

        # 🚨 INTENTIONAL SQL INJECTION 🚨
        sql = "INSERT INTO kpis VALUES (NULL, " + employee_id + ", '" + metric + "', " + value + ")"
        try:
            db.execute(sql)
            db.commit()
            return "KPI added."
        except Exception as e:
            return f"SQL Error: {e}"

    return render_template("kpi.html")

@app.route("/delete", methods=["GET", "POST"])
def delete_employee():
    return render_template("forbidden.html"), 403


# ---------------- MAIN ----------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
