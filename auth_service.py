from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = 'os.urandom(24)'

def email_registered(email):
    conn = sqlite3.connect('Database/library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email=?", (email,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

@app.route('/')
def home():
    return render_template('register.html')

# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        if email_registered(email):
            return "Email already registered."
        
        conn = sqlite3.connect('Database/library.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('Database/library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    
    return (
        f"Welcome, {session['user_name']}!<br>"
        f"<a href='http://localhost:5001'>Manage Books</a> | "
        f"<a href='http://localhost:5002?user_id={session['user_id']}&user_name={session['user_name']}'>Rent Books</a> | "
        f"<a href='/logout'>Logout</a>"
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True, port=5505)