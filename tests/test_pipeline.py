import csv 
from app.cleaning import clean_transactions 
from app.ingestion import read_transactions 
from app.export import write_transactions 
from main import run_pipeline

def test_ingestion_and_cleaning(tmp_path): 
    csv_file = tmp_path / "transactions.csv"

    csv_file.write_text (
        "transaction_id,customer_id,amount\n"
        "101,1,250\n"
        "102,,100\n"
        "103,2,-50\n"
        "101,3,300\n"
        "104,4,500\n"
        "105,5,125.75\n"       
    )

    transactions = read_transactions(csv_file)
    result = clean_transactions(transactions)

    assert len(transactions) == 6
    assert result["summary"]["valid_rows"] == 3

    valid_ids = [
        transaction["transaction_id"]
        for transaction in result["valid_transactions"]
    ]

    assert valid_ids == [101, 104, 105]
    assert result["summary"]["missing_customer_id"] == 1
    assert result["summary"]["invalid_amount"] == 1
    assert result["summary"]["duplicate_transactions"] == 1 

def test_full_pipeline_with_exports(tmp_path): 
    input_file = tmp_path / "transactions.csv"
    valid_file = tmp_path / "clean_transactions.csv"
    rejected_file = tmp_path / "rejected_transactions"

    input_file.write_text(
        "transaction_id,customer_id,amount\n"
        "101,1,250\n"
        "102,,100\n"
        "103,2,-50\n"
        "104,4,300\n"
    )

    transactions = read_transactions(input_file)
    result = clean_transactions(transactions)

    write_transactions(
        valid_file,
        result["valid_transactions"]
    )

    write_transactions(
        rejected_file, 
        result["rejected_transactions"],
        fieldnames = [
            "transaction_id", 
            "customer_id", 
            "amount", 
            "rejection_reason"
        ]
    )

    with open(valid_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        valid_rows = list(reader)

    with open(rejected_file, "r", newline="") as file: 
        reader = csv.DictReader(file)
        rejected_rows = list(reader)

    assert len(valid_rows) == 2
    assert len(rejected_rows) == 2
    assert rejected_rows[0]["rejection_reason"] == "missing_customer_id"
    assert rejected_rows[1]["rejection_reason"] == "invalid_amount"


def test_run_pipeline(tmp_path): 
    input_file = tmp_path / "transactions.csv"
    valid_file = tmp_path / "clean.csv"
    rejected_file = tmp_path / "rejected.csv"

    input_file.write_text(
        "transaction_id,customer_id,amount\n"
        "101,1,250\n"
        "102,,100\n"
        "103,2,-50\n"
        "104,4,300\n"
    )

    result = run_pipeline(input_file, valid_file, rejected_file)

    assert result["summary"]["total_rows"] == 4
    assert result["summary"]["valid_rows"] == 2

    assert valid_file.exists()
    assert rejected_file.exists() 