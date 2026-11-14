import math 
def clean_transactions(transactions): 
    """
    Validate transactions and identifies invalid records, 

    Args:
    transactions (list[dict]): A list of transaction records.
        Each transaction must contain:
        - transaction_id: Unique transaction identifier.
        - customer_id: Customer identifier.
        - amount: Numeric transaction amount.

    Returns:
        dict: A dictionary containing:
            - valid_transactions: Accepted transaction records.
            - summary: Counts of accepted and rejected records.

    Validation rules:
        1. Reject missing customer IDs.
        2. Reject amounts less than or equal to zero.
        3. Reject duplicate transaction IDs.
        4. Keep the first valid transaction for each ID.
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