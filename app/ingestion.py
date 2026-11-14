import csv 

def read_transactions(file_path): 
    """
    Read financial transactions from a CSV file.

    Converts transaction and customer IDs to integers and
    transaction amounts to floats. Invalid numeric values
    are represented as None for downstream validation.

    Args:
        file_path (str): Path to the input CSV file.

    Returns:
        list[dict]: Transactions represented as dictionaries.
    """
    transactions = [] 

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            customer_id = row.get("customer_id")
            try:
                customer_id = int(customer_id)
            except(ValueError,TypeError):
                customer_id = None 
            row["customer_id"] = customer_id 

            transaction_id = row.get("transaction_id")
            try:
                transaction_id = int(transaction_id)
            except (ValueError, TypeError): 
                transaction_id = None 
            row["transaction_id"] = transaction_id

            amount = row.get("amount")
            try:
                amount = float(amount)
            except (ValueError, TypeError): 
                amount = None 
            row["amount"] = amount 

            transactions.append(row)

    return transactions