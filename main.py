import logging

from app.ingestion import read_transactions
from app.cleaning import clean_transactions
from app.export import write_transactions

def run_pipeline(input_path, valid_path, rejected_path):
    logging.basicConfig ( 
    level = logging.INFO, 
    format= "%(levelname)s: %(message)s"
    )

    logging.info("Starting transaction pipeline")

    try: 
        transactions = read_transactions(input_path)
        logging.info("Read %d transactions", len(transactions))
    except FileNotFoundError: 
        logging.error("Input CSV file was not found.")
        raise

    result = clean_transactions(transactions)
    logging.info (
        "Cleaning complete: %d valid transactions", 
        result["summary"]["valid_rows"]
    )

    rejected_rows = (
        result["summary"]["total_rows"]
        - result["summary"]["valid_rows"]
    )

    if rejected_rows > 0: 
        logging.warning(
            "Rejected %d invalid transactions", 
            rejected_rows
        )
        missing = result["summary"]["missing_customer_id"]
        if missing > 0:
            logging.warning(
                "Missing customer ID: %d", missing
            )
        invalid = result["summary"]["invalid_amount"]
        if invalid > 0: 
            logging.warning(
                "Invalid amount: %d", invalid
            )
        duplicate = result["summary"]["duplicate_transactions"]
        if duplicate > 0: 
            logging.warning(
                "Duplicate transactions: %d", duplicate
            )
    try: 
        write_transactions(
            valid_path, 
            result["valid_transactions"], 
        )
        logging.info("Exported cleaned transactions")
    except FileNotFoundError: 
        logging.error("Failed to export transactions.")
        raise 
    try: 
        write_transactions(
        rejected_path,
        result["rejected_transactions"], 
                fieldnames = [
                "transaction_id",
                "customer_id", 
                "amount", 
                "rejection_reason"
            ]
        )
    except FileNotFoundError: 
        logging.error("Failed to export rejected transactions.")
        raise 

    return result


if __name__ == "__main__":
    run_pipeline(
        "data/transactions.csv",
        "data/clean_transactions.csv",
        "data/rejected_transactions.csv"
    )