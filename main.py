from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Konfigurasi MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="flask_book_management"
)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Periksa user di database
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not check_password_hash(user['password'], password):
        return jsonify({"message": "Invalid username or password!"}), 401

    # Kembalikan informasi pengguna
    return jsonify(user)

@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully!"})

@app.route('/books', methods=['GET'])
def get_books():
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    title = data['title']
    author = data['author']
    year = data['year']

    cursor = db.cursor()
    cursor.execute("INSERT INTO books (title, author, year) VALUES (%s, %s, %s)", (title, author, year))
    db.commit()
    cursor.close()
    return jsonify({"message": "Book added successfully"}), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
    db.commit()
    cursor.close()
    return jsonify({"message": "Book deleted successfully"})

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    title = data['title']
    author = data['author']
    year = data['year']

    cursor = db.cursor()
    cursor.execute("UPDATE books SET title = %s, author = %s, year = %s WHERE id = %s",
                   (title, author, year, book_id))
    db.commit()
    cursor.close()
    return jsonify({"message": "Book updated successfully"})

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_RUN_HOST'), port=os.gotenv('FLASK_RUN_PORT'))