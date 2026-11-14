import math 
def clean_transactions(transactions): 
    """
    Validate and separate financial transactions.

    Checks transactions for missing customer IDs, invalid
    amounts, and duplicate transaction IDs. Records rejection
    reasons and calculates a summary of validation results.

    Args:
        transactions (list[dict]): Transactions to validate.

    Returns:
        dict: A dictionary containing:
            - valid_transactions: Accepted transaction records.
            - rejected_transactions: Rejected records with reasons.
            - summary: Counts of processed and rejected records.
    """
    valid_transactions = [] 
    rejected_transactions = [] 

    seen_ids = set()

    missing_customer_id = 0 
    missing_transaction_id = 0 
    invalid_amount = 0
    duplicate_transactions = 0 

    for transaction in transactions: 

        if transaction.get("customer_id") is None: 
            missing_customer_id += 1 

            rejected = transaction.copy()
            rejected["rejection_reason"] = "missing_customer_id"

            rejected_transactions.append(rejected)
            continue

        amount = transaction.get("amount")
        if (
            isinstance(amount, bool)
            or not isinstance(amount, (float, int))
            or not math.isfinite(amount)
            or amount <= 0
        ):
            invalid_amount += 1

            rejected = transaction.copy() 
            rejected["rejection_reason"] = "invalid_amount"

            rejected_transactions.append(rejected)
            continue 

        transaction_id = transaction.get("transaction_id")
        if transaction_id is None: 
            missing_transaction_id += 1 

            rejected = transaction.copy() 
            rejected["rejection_reason"] = "missing_transaction_id"

            rejected_transactions.append(rejected)
            continue

        if transaction_id in seen_ids:
            duplicate_transactions += 1

            rejected = transaction.copy() 
            rejected["rejection_reason"] = "duplicate_transaction"

            rejected_transactions.append(rejected)
            continue

        seen_ids.add(transaction_id)     
        valid_transactions.append(transaction)
             
    return {
        "valid_transactions" : valid_transactions, 
        "rejected_transactions": rejected_transactions,
        "summary" : {
            "total_rows": len(transactions),
            "valid_rows": len(valid_transactions), 
            "missing_customer_id": missing_customer_id,
            "missing_transaction_id": missing_transaction_id,  
            "invalid_amount" : invalid_amount, 
            "duplicate_transactions" : duplicate_transactions
        }
    }