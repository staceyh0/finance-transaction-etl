from app.cleaning import clean_transactions 

def test_empty_transactions():
    result = clean_transactions([])

    assert result["valid_transactions"] == []
    assert result["summary"]["total_rows"] == 0
    assert result["summary"]["valid_rows"] == 0 


def test_duplicate_transactions():
    transactions = [
        {"transaction_id": 101, "customer_id": 1, "amount": 100},
        {"transaction_id": 101, "customer_id": 2, "amount": 200}
    ]

    result = clean_transactions(transactions)

    assert len(result["valid_transactions"]) == 1
    assert result["summary"]["duplicate_transactions"] == 1
    assert result['valid_transactions'][0]["amount"] == 100

def test_invalid_transactions():
    transactions = [
        {"transaction_id": 101, "customer_id": None, "amount": 100},
        {"transaction_id": 102, "customer_id": 2, "amount": -50},
        {"transaction_id": 103, "customer_id": 3, "amount": 0},
        {"transaction_id": 104, "customer_id": 4, "amount": 250}
    ]

    result = clean_transactions(transactions)

    assert result["summary"]["total_rows"] == 4
    assert result["summary"]["missing_customer_id"] == 1
    assert result["summary"]["invalid_amount"] == 2
    assert result["summary"]["valid_rows"] == 1
    assert result["valid_transactions"][0]["transaction_id"] == 104

def test_invalid_transaction_does_not_reserve_id(): 
    transactions = [
        {"transaction_id": 201, "customer_id": None, "amount": 100},
        {"transaction_id": 201, "customer_id": 5, "amount": 200}
    ]

    result = clean_transactions(transactions)

    assert result["summary"]["missing_customer_id"] == 1 
    assert result["summary"]["duplicate_transactions"] == 0
    assert result["summary"]["valid_rows"] == 1
    assert result["valid_transactions"][0]["amount"] == 200

import copy 

def test_does_not_modify_original(): 
    transactions = [
        {"transaction_id": 101, "customer_id": 1, "amount": 100},
        {"transaction_id": 102, "customer_id": None, "amount": 200}
    ]

    original = copy.deepcopy(transactions)
    result = clean_transactions(transactions)

    assert transactions == original
    assert len(result["valid_transactions"]) == 1 

def test_rejected_transactions_include_reasons(): 
    transactions = [
        {"transaction_id": 101, "customer_id": 1, "amount": 250.0},
        {"transaction_id": 102, "customer_id": None, "amount": 100.0},
        {"transaction_id": 103, "customer_id": 2, "amount": -50.0},
    ]

    result = clean_transactions(transactions)
    rejected = result["rejected_transactions"]

    assert len(rejected) == 2 
    assert rejected[0]["rejection_reason"] == "missing_customer_id"
    assert rejected[1]["rejection_reason"] == "invalid_amount"