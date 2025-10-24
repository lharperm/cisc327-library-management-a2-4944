import pytest
from library_service import (
    add_book_to_catalog
)
from database import init_database, add_sample_data, DATABASE
import os
@pytest.fixture(autouse=True, scope="function")
def reset_db():
    """Reset the database before each test."""
    # Remove old DB if it exists
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    # Recreate fresh tables + sample data
    init_database()
    add_sample_data()

def test_add_book_isbn_too_long():
    """Test adding a book with an ISBN longer then the expected 13 digits"""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234577777123456", 5)
    
    assert success == False
    assert "13 digits" in message

def test_add_book_missing_author():
    """Test adding a book without an author"""
    success, message = add_book_to_catalog("Test Book", "", "1234563890123", 5)
    
    assert success == False
    assert "author" in message.lower()

def test_add_book_negative_copies():
    """Test adding a book with a negative integer of copies"""
    success, message = add_book_to_catalog("Test Book", "Test Author" , "1234554590133", -4)
    
    assert success == False
    assert "copies" in message.lower()

def test_add_book_valid_entry():
    """Test adding a book with a valid input"""
    success, message = add_book_to_catalog("Test Book", "Test Author" , "1313131313131", 10)
    
    assert success == True
    assert "successfully added" in message.lower()
