import pytest
from services.library_service import (
    search_books_in_catalog
)

def test_partial_search_by_title():
    """Testing partial search by title"""
    results = search_books_in_catalog("gatsby", "title")

    assert isinstance(results, list)
    assert any("gatsby" in book["title"].lower() for book in results)

def test_partial_search_by_author():
    """Testing partial search by author"""
    results = search_books_in_catalog("orwell", "author")

    assert isinstance(results, list)
    assert any("orwell" in book["author"].lower() for book in results)

def test_search_by_isbn():
    """Testing search for book by ISBN"""
    results = search_books_in_catalog("19780743273565", "isbn")

    assert isinstance(results, list)
    assert all(book["isbn"] == "9780743273565" for book in results)


def test_search_invalid_entry():
    """Testing a search with an invalid entry"""
    results = search_books_in_catalog("Oppenheimer", "movie")

    assert isinstance(results, list)
    assert results == []