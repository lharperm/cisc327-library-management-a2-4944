from services.payment_service import PaymentGateway

def test_process_payment_success():
    "Test succesfull payments processed"
    gateway = PaymentGateway()
    success, txn_id, msg = gateway.process_payment("123456", 10.0, "Late fee")
    assert success is True
    assert "processed successfully" in msg
    assert txn_id.startswith("txn_")

def test_process_payment_invalid_amount():
    "Test payments processed with invalid amounts"
    gateway = PaymentGateway()
    success, txn_id, msg = gateway.process_payment("123456", 0, "Invalid")
    assert success is False
    assert "Invalid amount" in msg

def test_process_payment_invalid_patron():
    "Test payments processed with invalid patron number"
    gateway = PaymentGateway()
    success, txn_id, msg = gateway.process_payment("2A", 10.0, "Bad ID")
    assert success is False
    assert "Invalid patron ID" in msg

def test_refund_payment_invalid_id():
    "Test payments processed with invalid transaction id"
    gateway = PaymentGateway()
    success, msg = gateway.refund_payment("invalid_id", 10.0)
    assert success is False
    assert "Invalid transaction ID" in msg

def test_verify_payment_status_completed():
    "Test payments processed completed succesfully."
    gateway = PaymentGateway()
    txn = "txn_123456_001"
    result = gateway.verify_payment_status(txn)
    assert result["status"] == "completed"
