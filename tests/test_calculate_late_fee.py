import pytest
from services.library_service import (
    calculate_late_fee_for_book
)

def test_no_overdue_fee():
    """Testing a book returned before the 14 day late period. """
    result = calculate_late_fee_for_book("123456", 1)

    assert isinstance(result, dict)
    assert result["fee_amount"] == 0.00
    assert result["days_overdue"] == 0

def test_first_7days_overdue():
    """Testing a book returned within the first 7 days overdue"""

    result = calculate_late_fee_for_book("345453", 2)
    assert result["days_overdue"] == 5
    assert result["fee_amount"] == 5 * 0.50

def test_after_7days_overdue():
    """Testing a book returned after the first 7 days overdue"""

    result = calculate_late_fee_for_book("298734", 2)
    assert result["days_overdue"] == 10
    assert result["fee_amount"] == 7 * 0.50 + 3*1.00

def test_max_late_fee():
    """Testing a book returned beyond the max overdue fees"""

    result = calculate_late_fee_for_book("298745", 2)
    assert result["days_overdue"] == 35
    assert result["fee_amount"] == 15.00



