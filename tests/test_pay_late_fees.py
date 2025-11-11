import pytest
from unittest.mock import Mock
from services.library_service import (
    pay_late_fees
)
from services.payment_service import PaymentGateway

def test_succesful_payment(mocker):
    """Tests valid payments are succesfull"""

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id": 1, "title": "Harry Potter"},
    )
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 12.0, "days_overdue": 3, "status": "Completed"},
    )


    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (
        True,
        "txn_123456_001",
        "Payment processed",
    )

    success, message, txn_id = pay_late_fees("123456", 1, mock_gateway)

    assert success is True
    assert "Payment successful!" in message
    assert txn_id.startswith("txn_123456_001") or txn_id.startswith("txn_")
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=12.0,
        description="Late fees for 'Harry Potter'",
    )

def test_payment_declined(mocker):
    """Tests declined paymennts"""

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id": 1, "title": "Harry Potter"},
    )
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 12.0, "days_overdue": 3, "status": "Completed"},
    )

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (
        False,              
        "",                 
        "Payment declined",
    )

    success, message, txn_id = pay_late_fees("123456", 1, mock_gateway)

    assert success is False
    assert "Payment failed: Payment declined" in message
    assert txn_id is None
    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456", 
        amount=12.0, 
        description="Late fees for 'Harry Potter'",
        )

def test_invalid_patron_id(mocker):
    "Tests payments made with invalid patron ids"
    
    mock_gateway = Mock(spec=PaymentGateway)

    success, message, txn_id = pay_late_fees("1AAAAA", 1, mock_gateway)

    assert success is False
    assert message == "Invalid patron ID. Must be exactly 6 digits."
    assert txn_id is None

    mock_gateway.process_payment.assert_not_called()
 
def test_zero_late_fees(mocker):
    "Tests payments made but account had no late fees"

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id": 1, "title": "Harry Potter"},
    )
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 0.00, "days_overdue": 0, "status": "Completed"},
    )
    
    mock_gateway = Mock(spec=PaymentGateway)

    success, message, txn_id = pay_late_fees("123456", 1, mock_gateway)

    assert success is False
    assert message == "No late fees to pay for this book."
    assert txn_id is None

    mock_gateway.process_payment.assert_not_called()
 
def test_network_error(mocker):
    "Tests network error exception handling"

    mocker.patch(
        "services.library_service.get_book_by_id",
        return_value={"id": 1, "title": "Harry Potter"},
    )
    mocker.patch(
        "services.library_service.calculate_late_fee_for_book",
        return_value={"fee_amount": 12.00, "days_overdue": 3, "status": "Completed"},
    )
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.side_effect = Exception("Network error")

    success, message, txn_id = pay_late_fees("123456", 1, mock_gateway)

    assert success is False
    assert message == "Payment processing error: Network error"
    assert txn_id is None

    mock_gateway.process_payment.assert_called_once_with(
        patron_id="123456",
        amount=12.00,
        description="Late fees for 'Harry Potter'",
    )

    
