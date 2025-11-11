import pytest
from services.library_service import (
    borrow_book_by_patron
)


def test_borrow_book_valid_input():
    """Test borrowing a book with an valid patron ID"""
    success, message = borrow_book_by_patron("123456", 1)  
    
    assert success is True
    assert "borrowed" in message.lower()
    assert "due date" in message.lower()

def test_borrow_book_invalid_patron_id():
    """Test borrowing a book with an invalid patron ID"""
    success, message = borrow_book_by_patron("1234567", 1)  
    
    assert success is False
    assert "id" in message.lower()

def test_borrow_missing_book_id():
    """Test borrowing a book with a non-existent id"""
    success, message = borrow_book_by_patron("123456", 89)  
    
    assert success is False
    assert "book not found" in message.lower()



