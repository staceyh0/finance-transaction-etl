import csv 
import pytest
from app.export import write_transactions 

def test_write_transactions(tmp_path):
    output_file = tmp_path / "clean_transactions.csv"

    transactions = [
        {"transaction_id": 101, "customer_id": 1, "amount": 250.0},
        {"transaction_id": 104, "customer_id": 4, "amount": 500.0},    
    ]

    write_transactions(output_file, transactions)

    with open(output_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["transaction_id"] == "101"
    assert rows[1]["transaction_id"] == "104"
    assert rows[0]["amount"] == "250.0"

def test_error_handling(tmp_path): 
    output_file = tmp_path/ "missing_folder"/ "clean.csv"

    transactions = [
    {"transaction_id": 101, "customer_id": 1, "amount": 250.0}
    ]

    with pytest.raises(FileNotFoundError):
        write_transactions(output_file, transactions)

def test_export_rejected_transactions(tmp_path): 
    output_file = tmp_path/ "rejected_transactions.csv"

    rejected_transactions = [
        {
            "transaction_id": 102,
            "customer_id": None,
            "amount": 100.0,
            "rejection_reason": "missing_customer_id"
        },
        {
            "transaction_id": 103,
            "customer_id": 2,
            "amount": -50.0,
            "rejection_reason": "invalid_amount"
        }
    ]

    fieldnames = [
        "transaction_id",
        "customer_id",
        "amount",
        "rejection_reason"
    ]

    write_transactions (
        output_file,
        rejected_transactions, 
        fieldnames = [
            "transaction_id", 
            "customer_id", 
            "amount", 
            "rejection_reason"
        ]
    )

    with open(output_file, "r", newline="") as file: 
        reader = csv.DictReader(file) 
        rows = list(reader)

    assert len(rows) == 2 
    assert rows[0]["rejection_reason"] == "missing_customer_id"
    assert rows[1]["rejection_reason"] == "invalid_amount"