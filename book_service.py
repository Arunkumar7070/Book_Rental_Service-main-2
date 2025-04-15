from flask import *
import sqlite3

app = Flask(__name__)

def book_exists(title, author):
    conn = sqlite3.connect('Database/library.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books WHERE title=? AND author=?", (title, author))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

@app.route('/')
def home():
    return render_template('add_book.html')

# Add a new book to the library
@app.route('/books', methods=['POST'])
def add_book():
    title = request.form['title']
    author = request.form['author']
    status = 'available'
    
    # Check for existing book instead of using try block for unique constraint
    if book_exists(title, author):
        return "Book already exists."

    conn = sqlite3.connect('Database/library.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO books (title, author, status) VALUES (?, ?, ?)', (title, author, status))
    conn.commit()
    conn.close()
    return redirect('/books')

# List all books
@app.route('/books')
def list_books():
    conn = sqlite3.connect('Database/library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()
    return render_template('books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
