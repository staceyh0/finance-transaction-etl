import logging
import argparse

from app.ingestion import read_transactions
from app.cleaning import clean_transactions
from app.export import write_transactions


logger = logging.getLogger(__name__)

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

    logger.info("Starting transaction pipeline")

    try: 
        transactions = read_transactions(input_path)
        logger.info("Read %d transactions", len(transactions))
    except FileNotFoundError: 
        logger.exception("Input CSV file was not found.")
        raise

    result = clean_transactions(transactions)
    logger.info (
        "Cleaning complete: %d valid transactions", 
        result["summary"]["valid_rows"]
    )

    rejected_rows = (
        result["summary"]["total_rows"]
        - result["summary"]["valid_rows"]
    )

    if rejected_rows > 0: 
        logger.warning(
            "Rejected %d invalid transactions", 
            rejected_rows
        )
        missing_customer_id = result["summary"]["missing_customer_id"]
        if missing_customer_id > 0:
            logger.warning(
                "Missing customer ID: %d", missing_customer_id
            )
        invalid = result["summary"]["invalid_amount"]
        if invalid > 0: 
            logger.warning(
                "Invalid amount: %d", invalid
            )
        missing_transaction_id = result["summary"]["missing_transaction_id"]
        if missing_transaction_id > 0:
            logger.warning(
                "Missing transaction ID: %d", missing_transaction_id
            )
        duplicate = result["summary"]["duplicate_transactions"]
        if duplicate > 0: 
            logger.warning(
                "Duplicate transactions: %d", duplicate
            )
    try: 
        write_transactions(
            valid_path, 
            result["valid_transactions"], 
        )
        logger.info("Exported cleaned transactions")
    except OSError: 
        logger.exception("Failed to export transactions.")
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
        logger.info("Exported rejected transactions")
    except OSError:
        logger.exception("Failed to export rejected transactions")
        raise
        
    return result


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate and export financial transactions."
    )

    parser.add_argument(
        "--input",
        default="data/transactions.csv",
        help="Input CSV file path",
    )

    parser.add_argument(
        "--valid",
        default="data/clean_transactions.csv",
        help="Output path for valid transactions",
    )

    parser.add_argument(
        "--rejected",
        default="data/rejected_transactions.csv",
        help="Output path for rejected transactions",
    )

    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s"
    )

    args = parse_args()

    try:
        run_pipeline(
            args.input,
            args.valid,
            args.rejected
        )
    except (OSError, ValueError, KeyError) as exc:
        logger.error("Pipeline failed: %s", exc)
        raise SystemExit(1) from exc
