import sqlite3
from flask import Flask, render_template, redirect, request, session, flash
import os 
from functools import wraps 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("CS_50_FINAL_KEY")

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    return '<h3>Worked!</h3>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get("username")
        if not username:
            flash("Username entered is invalid.")
            return redirect("/login")
        
        password = request.form.get("password")
        if not password:
            flash("Password entered is invalid.")
            return redirect("/login")

        conn = get_db_connection()
        user = conn.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,)).fetchone()
        if not user:
            flash("Username does not exist. Did you mean to register?")
            conn.close()
            return redirect("/login")

        if check_password_hash(user['password_hash'], password):
            session["user_id"] = user['id']
            conn.close()
            return redirect('/')
        else:
            flash('Password did not match.')
            conn.close()
            return redirect('/login')



@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        conn = get_db_connection()
        username = request.form.get("username")
        if not username:
            flash("Username entered is invalid.")
            return redirect("/register")
        
        password = request.form.get("password")
        if not password:
            flash("Password entered is invalid.")
            return redirect("/register")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            flash("Invalid password confirmation.")
            return redirect("/register")

        if password != confirmation:
            flash("Password and confirmation do not match!")
            return redirect("/register")

        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            flash('Username already exists.')
            return redirect("/register")

        password_hash = generate_password_hash(password)

        conn.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, password_hash))
        conn.commit()
        session["user_id"] = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return redirect('/')



if __name__ == "__main__":
    init_db()
    app.run(debug=True)