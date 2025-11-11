import pytest
from unittest.mock import Mock
from services.library_service import (
    pay_late_fees, refund_late_fee_payment
)
from services.payment_service import PaymentGateway


def test_succesful_refund():
    """Tests valid payments are succesfull"""

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (
        True,
        "Refund of $12.00 processed successfully. Refund ID: refund_txn_123456_001",
    )

    success, message = refund_late_fee_payment(
        "txn_123456_001", 12.0, mock_gateway
    )

    assert success is True
    assert "Refund of $12.00 processed successfully" in message
    mock_gateway.refund_payment.assert_called_once_with("txn_123456_001", 12.0)

def test_invalid_transaction_ID_rejection():
    """Tests refunds with invalid transaction ID"""

    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (
        True,
        "Refund of $12.00 processed successfully. Refund ID: refund_txn_123456_001",
    )

    success, message = refund_late_fee_payment(
        "invalid_txn", 12.0, mock_gateway
    )

    assert success is False
    assert message == "Invalid transaction ID."
    mock_gateway.refund_payment.assert_not_called()

def test_invalid_refund_negative():
    """Tests invalid refund amount: negative values"""

    mock_gateway = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment(
        "txn_123456_001", -5.0, mock_gateway
    )

    assert success is False
    assert message == "Refund amount must be greater than 0."
    mock_gateway.refund_payment.assert_not_called()
 
def test_invalid_refund_Zero():
    """Tests invalid refund amount: Zero"""

    mock_gateway = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment(
        "txn_123456_001",0.0, mock_gateway
    )

    assert success is False
    assert message == "Refund amount must be greater than 0."
    mock_gateway.refund_payment.assert_not_called()

def test_invalid_refund_Over_Max():
    """Tests invalid refund amount: Over 15.0"""

    mock_gateway = Mock(spec=PaymentGateway)
    success, message = refund_late_fee_payment(
        "txn_123456_001", 20.0, mock_gateway
    )

    assert success is False
    assert message == "Refund amount exceeds maximum late fee."
    mock_gateway.refund_payment.assert_not_called()