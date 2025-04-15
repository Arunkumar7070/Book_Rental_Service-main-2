import sqlite3

conn = sqlite3.connect('library.db')
c = conn.cursor()

# Enable foreign key support
c.execute('PRAGMA foreign_keys = ON')

# Create users table
c.execute('''CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);''')

c.execute('''CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    status TEXT NOT NULL
);''')

c.execute('''CREATE TABLE rentals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    rental_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);
    
''')


conn.commit()
conn.close()

print("Database initialized successfully.")