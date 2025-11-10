from flask import render_template, Blueprint, request, redirect, url_for, jsonify
from project import db
from project.books.models import Book
from project.books.forms import CreateBook
from project.utils import sanitize_text


# Blueprint for books
books = Blueprint('books', __name__, template_folder='templates', url_prefix='/books')


# Route to display books in HTML
@books.route('/', methods=['GET'])
def list_books():
    # Fetch all books from the database
    books = Book.query.all()
    print('Books page accessed')
    return render_template('books.html', books=books)


# Route to fetch books in JSON format
@books.route('/json', methods=['GET'])
def list_books_json():
    # Fetch all books from the database and convert to JSON
    books = Book.query.all()
    # Create a list of dictionaries representing each book with the required fields
    book_list = [{'name': book.name, 'author': book.author, 'year_published': book.year_published, 'book_type': book.book_type} for book in books]
    return jsonify(books=book_list)


# Route to create a new book
@books.route('/create', methods=['POST', 'GET'])
def create_book():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    try:
        # ✅ Sanitizacja i walidacja
        name = sanitize_text(data.get('name', ''), max_len=200)
        author = sanitize_text(data.get('author', ''), max_len=200)
        year_raw = data.get('year_published')
        try:
            year_published = int(year_raw) if year_raw not in (None, '') else None
        except ValueError:
            return jsonify({'error': 'year_published must be an integer'}), 400
        book_type = sanitize_text(data.get('book_type', ''), max_len=100)

        new_book = Book(name=name, author=author, year_published=year_published, book_type=book_type)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('books.list_books'))

    except ValueError as ve:
        db.session.rollback()
        return jsonify({'error': f'Invalid field: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error creating book: {str(e)}'}), 500


# Route to update an existing book
@books.route('/<int:book_id>/edit', methods=['POST'])
def edit_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    try:
        if 'name' in data:
            book.name = sanitize_text(data.get('name'), max_len=200)
        if 'author' in data:
            book.author = sanitize_text(data.get('author'), max_len=200)
        if 'year_published' in data:
            yr = data.get('year_published')
            book.year_published = int(yr) if yr not in (None, '') else None
        if 'book_type' in data:
            book.book_type = sanitize_text(data.get('book_type'), max_len=100)

        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})

    except ValueError as ve:
        db.session.rollback()
        return jsonify({'error': f'Invalid field: {str(ve)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error updating book: {str(e)}'}), 500



# Route to fetch existing book data for editing
@books.route('/<int:book_id>/edit-data', methods=['GET'])
def get_book_for_edit(book_id):
    # Get the book with the given ID
    book = Book.query.get(book_id)
    
    # Check if the book exists
    if not book:
        print('Book not found')
        return jsonify({'success': False, 'error': 'Book not found'}), 404

    # Create a dictionary representing the book data
    book_data = {
        'name': book.name,
        'author': book.author,
        'year_published': book.year_published,
        'book_type': book.book_type
    }
    
    return jsonify({'success': True, 'book': book_data})


# Route to delete a book
@books.route('/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        print('Book not found')
        return jsonify({'error': 'Book not found'}), 404

    try:
        # Delete the book from the database
        db.session.delete(book)
        db.session.commit()
        print('Book deleted successfully')
        return redirect(url_for('books.list_books'))
    except Exception as e:
        # Handle any exceptions, such as database errors
        db.session.rollback()
        print('Error deleting book')
        return jsonify({'error': f'Error deleting book: {str(e)}'}), 500


# Route to get book details based on book name
@books.route('/details/<string:book_name>', methods=['GET'])
def get_book_details(book_name):
        # Find the book by its name
        book = Book.query.filter_by(name=book_name).first()

        if book:
            book_data = {
                'name': book.name,
                'author': book.author,
                'year_published': book.year_published,
                'book_type': book.book_type
            }
            return jsonify(book=book_data)
        else:
            print('Book not found')
            return jsonify({'error': 'Book not found'}), 404