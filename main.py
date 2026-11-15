import logging
from app.ingestion import read_transactions
from app.cleaning import clean_transactions
from app.export import write_transactions

def run_pipeline(input_path, valid_path, rejected_path):
    """
    Execute the financial transaction ETL pipeline.

    Reads raw transactions, validates and separates records,
    logs processing results, and exports valid and rejected
    transactions into separate CSV files.

    Args:
        input_path (str): Path to the source CSV file.
        valid_path (str): Destination for valid transactions.
        rejected_path (str): Destination for rejected transactions.

    Returns:
        dict: Cleaning results containing valid transactions,
        rejected transactions, and processing statistics.
    """
    logging.basicConfig ( 
        level = logging.INFO, 
        format= "%(levelname)s: %(message)s"
    )

    logging.info("Starting transaction pipeline")

    try: 
        transactions = read_transactions(input_path)
        logging.info("Read %d transactions", len(transactions))
    except FileNotFoundError: 
        logging.exception("Input CSV file was not found.")
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
        missing_customer_id = result["summary"]["missing_customer_id"]
        if missing_customer_id > 0:
            logging.warning(
                "Missing customer ID: %d", missing_customer_id
            )
        invalid = result["summary"]["invalid_amount"]
        if invalid > 0: 
            logging.warning(
                "Invalid amount: %d", invalid
            )
        missing_transaction_id = result["summary"]["missing_transaction_id"]
        if missing_transaction_id > 0:
            logging.warning(
                "Missing transaction ID: %d", missing_transaction_id
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
    except OSError: 
        logging.exception("Failed to export transactions.")
        raise 
    try:
        write_transactions(
            rejected_path,
            result["rejected_transactions"],
            fieldnames=[
                "transaction_id",
                "customer_id",
                "amount",
                "rejection_reason",
            ],
        )
        logging.info("Exported rejected transactions")
    except OSError:
        logging.exception("Failed to export rejected transactions")
        raise
        
    return result


if __name__ == "__main__":
    run_pipeline(
        "data/transactions.csv",
        "data/clean_transactions.csv",
        "data/rejected_transactions.csv"
    )