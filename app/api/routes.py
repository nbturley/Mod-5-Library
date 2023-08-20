from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api', __name__, url_prefix='/api')

# Create book route
@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    book_title = request.json['book_title']
    length = request.json['length']
    isbn = request.json['isbn']
    author_name = request.json['author_name']
    genre = request.json['genre']
    user_token = current_user_token.token

    print(f'Librarian: {user_token}')

    book = Book(book_title, length, isbn, author_name, genre, user_token=user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

# Route to get all books in inventory
@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    the_user = current_user_token.token
    books = Book.query.filter_by(user_token = the_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

# Route to get single book in inventory
@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    book = Book.query.get(id)
    response = book_schema.dump(book)
    return jsonify(response)

# Update book route
@api.route('/books/<id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id)
    book.book_title = request.json['book_title']
    book.length = request.json['length']
    book.user_token = current_user_token.token
    book.isbn = request.json['isbn']
    book.author_name = request.json['author_name']
    book.genre = request.json['genre']
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

# Delete book route
@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)