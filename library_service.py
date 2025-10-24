"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books, get_patron_borrowed_books, get_db_connection
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed > 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    Implements R4 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to return
        
    Returns:
        tuple: (success: bool, message: str)
    """

    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists 
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."

    #check if book is borrowed by patron

    books = get_patron_borrowed_books(patron_id)
    book_ids = []

    for book in books:
        book_ids.append(book["book_id"])
    if book_id not in book_ids:
        return (False, "Book is not borrowed by this patron")  
    
    update_avail = update_book_availability(book_id, 1)
    update_borrow = update_borrow_record_return_date(patron_id, book_id, datetime.now())

    if not update_avail or not update_borrow:
        return (False, "DB error")
    
    fees = calculate_late_fee_for_book(patron_id, book_id)
    
    if fees["fee_amount"] > 0:
        return (True, (f'Late by {fees["days_overdue"]} days. '
            f'Fee owed: ${fees["fee_amount"]:.2f}.'))
    
    return (True, "Book returned succesfully and on time!")


def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    Implements R5 as per requirements 
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book returned
        
    Returns:
        // return the calculated values
        'fee_amount': 0.00,
        'days_overdue': 0,
        'status': 'Calculation status'
    }
    """

    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {
            "fee_amount": 0.00,
            "days_overdue": 0,
            "status": "Invalid patron ID"
        }
    
    # Check if book exists 
    book = get_book_by_id(book_id)
    if not book:
        return {
            "fee_amount": 0.00,
            "days_overdue": 0,
            "status": "Book Doesn't Exist"
        }
    
    books = get_patron_borrowed_books(patron_id)
    book_ids = []
    due_dates = []

    for book in books:
        book_ids.append(book["book_id"])
        due_dates.append(book["due_date"])
    if book_id not in book_ids:
        return {
            "fee_amount": 0.00,
            "days_overdue": 0,
            "status": "Book not borrowed by patron."
        }
    
    index = book_ids.index(book_id)
    due_date = due_dates[index]
    
    days_overdue = max(0, (datetime.now() - due_date).days)

    fee = 0
    if days_overdue == 0:
        fee = 0.00
    elif days_overdue <= 7:
        fee += .50*days_overdue
    else:
        fee = (7 * 0.50) + ((days_overdue - 7) * 1.00)
    

    if fee > 15.00:
        fee = 15.00

    return {
        "fee_amount": round(fee, 2),
        "days_overdue": days_overdue,
        "status": "Completed"
    }

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    Implements R6 as per requirements

     Args:
        search_term: search input str
        search_type: str of search type
        
    Returns:
       dictionary of matches
    """

    if not search_term or not search_type:
        return []

    conn = get_db_connection()

    search_type = search_type.lower().strip()
    search_term = search_term.strip()

    if search_type == "isbn":
        query = "SELECT * FROM books WHERE isbn = ? ORDER BY title"
        params = (search_term,)
    elif search_type == "title":
        query = "SELECT * FROM books WHERE LOWER(title) LIKE ? ORDER BY title"
        params = (f"%{search_term.lower()}%",)
    elif search_type == "author":
        query = "SELECT * FROM books WHERE LOWER(author) LIKE ? ORDER BY title"
        params = (f"%{search_term.lower()}%",)
    else:
        conn.close()
        return []
    
    results = conn.execute(query, params).fetchall()
    conn.close()

    return [dict(book) for book in results]


def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    
    TODO: Implement R7 as per requirements
    """

    # Validate patron ID
    if not patron_id or not patron_id.isdigit() or len(patron_id) != 6:
        return {}
    
    books = get_patron_borrowed_books(patron_id)
    books_borrowed = get_patron_borrow_count(patron_id)
    total_late_fees = 0
    
    borrowed = []

    for book in books:
        fee_info = calculate_late_fee_for_book(patron_id, book["book_id"])
        late_fee = fee_info.get("fee_amount", 0.0)
        days_overdue = fee_info.get("days_overdue", 0)

        total_late_fees += late_fee

        borrowed.append({
            "book_id": book["book_id"],
            "title": book["title"],
            "author": book["author"],
            "due_date": book["due_date"].strftime("%Y-%m-%d"),
            "is_overdue": book["is_overdue"],
            "days_overdue": days_overdue,
            "late_fee": round(late_fee, 2)
        })
    
    return {
        "patron_id": patron_id,
        "currently_borrowed": borrowed,
        "num_currently_borrowed": books_borrowed,
        "total_late_fees": round(total_late_fees, 2),
    }

