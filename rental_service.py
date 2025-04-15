from flask import *
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'os.urandom(24)'  # Set a secure secret key

def get_user_id():
    return session.get('user_id')

@app.route('/')
def home():
    # Get user data from URL parameters if not already in session
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    if not user_id:
        return redirect('http://localhost:5505/login')
    
    session['user_id'] = int(user_id)
    session['user_name'] = user_name
    return render_template('rent_book.html', user_name=user_name)

# Rent a book
@app.route('/rent', methods=['POST'])
def rent_book():
    if not get_user_id():
        return redirect('http://localhost:5505/login')
    
    book_id = request.form['book_id']
    rental_date = datetime.now().strftime('%Y-%m-%d')
    user_id = get_user_id()
    
    conn = sqlite3.connect('Database/library.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    
    # Check if the book is available
    cursor.execute('SELECT status FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    if not book or book[0] != 'available':
        conn.close()
        return "Book is not available or does not exist."
    
    # Check if a rental already exists for the same user and book that is active.
    cursor.execute('''SELECT id FROM rentals 
                      WHERE user_id = ? AND book_id = ? AND return_date IS NULL''', (user_id, book_id))
    existing_rental = cursor.fetchone()
    if existing_rental:
        conn.close()
        return "Rental already exists for this book under your account."

    cursor.execute('INSERT INTO rentals (user_id, book_id, rental_date) VALUES (?, ?, ?)', 
                   (user_id, book_id, rental_date))
    cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('rented', book_id))
    conn.commit()
    conn.close()
    return redirect('/rentals')

# Return a book
@app.route('/return', methods=['POST'])
def return_book():
    if not get_user_id():
        return redirect('http://localhost:5505/login')
    
    book_id = request.form['book_id']
    user_id = get_user_id()
    
    conn = sqlite3.connect('Database/library.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()
    
    # Check if an active rental exists for this user and book
    cursor.execute('''SELECT id FROM rentals 
                      WHERE user_id = ? AND book_id = ? AND return_date IS NULL''', (user_id, book_id))
    rental = cursor.fetchone()
    
    if not rental:
        conn.close()
        return "No active rental found for this book under your account."
    
    # Delete the rental record
    cursor.execute('''DELETE FROM rentals 
                      WHERE user_id = ? AND book_id = ? AND return_date IS NULL''', (user_id, book_id))
    
    # Update the book status back to available
    cursor.execute('UPDATE books SET status = ? WHERE id = ?', ('available', book_id))
    conn.commit()
    conn.close()
    return redirect('/rentals')

# List rentals for the logged-in user
@app.route('/rentals')
def list_rentals():
    if not get_user_id():
        return redirect('http://localhost:5505/login')
    
    user_id = get_user_id()
    conn = sqlite3.connect('Database/library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rentals WHERE user_id = ?', (user_id,))
    rentals = cursor.fetchall()
    conn.close()
    return render_template('rentals.html', rentals=rentals, user_name=session.get('user_name'))

if __name__ == '__main__':
    app.run(debug=True, port=5002)