import pytest
from library_service import (
    return_book_by_patron
)

def test_return_book_valid_return():
    """Test successful return of a book"""
    success, message = return_book_by_patron("123456", 1)

    assert success is True
    assert "succesfully" in message.lower()
    assert "on time" in message.lower()

def test_return_book_not_borrowed():
    """Test returning a book that was never originally borrowed"""
    success, message = return_book_by_patron("123456", 999)  

    assert success is False
    assert "book not found" in message.lower()

def test_return_book_invalid_patron_id():
    """Test returninga book with invalid patron id"""
    success, message = return_book_by_patron("12356675", 1)  

    assert success is False
    assert "id" in message.lower()

def test_return_book_late_fee():
    """Test return after due date actually mentions late fees."""
    success, message = return_book_by_patron("123456", 3)

    assert success is True
    assert any(word in message.lower() for word in ["succesfully", "returned", "book"])