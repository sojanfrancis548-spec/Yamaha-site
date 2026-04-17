from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'yamaha123secret'
ADMIN_USERNAME = 'admin'        
ADMIN_PASSWORD = 'yamaha2026'   
DB = 'yamaha.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT NOT NULL,
                email     TEXT NOT NULL,
                model     TEXT,
                message   TEXT,
                created   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name    = request.form.get('name')
    email   = request.form.get('email')
    model   = request.form.get('model')
    message = request.form.get('message')
    with get_db() as conn:
        conn.execute(
            'INSERT INTO contacts (name, email, model, message) VALUES (?, ?, ?, ?)',
            (name, email, model, message)
        )
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    with get_db() as conn:
        leads = conn.execute('SELECT * FROM contacts ORDER BY created DESC').fetchall()
    return render_template('admin.html', leads=leads)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Wrong username or password!'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
