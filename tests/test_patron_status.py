import pytest
from library_service import (
    get_patron_status_report
)

def test_report_structure():
    """Testing the structure of patron status report"""
    report = get_patron_status_report("123456")

    assert isinstance(report, dict)
    for key in ["currently_borrowed", "total_late_fees", "num_currently_borrowed", "patron_id"]:
        assert key in report

def test_borrowed_books():
    """Testing that borrowed books are displayed as a list with due dates"""
    report = get_patron_status_report("123456")

    assert isinstance(report["currently_borrowed"], list)
    for book in report["currently_borrowed"]:
        assert "title" in book
        assert "due_date" in book

def test_total_late_fees():
    """Test that late fees are a float value >= 0"""
    report = get_patron_status_report("123456")

    assert isinstance(report["total_late_fees"], (int, float))
    assert report["total_late_fees"] >= 0

def test_borrowed_book():
    """Test that a patrons borrowed count matches the length of theur borrowed books"""
    report = get_patron_status_report("123456")

    assert isinstance(report["num_currently_borrowed"], int)
    assert report["num_currently_borrowed"] == len(report["currently_borrowed"])

