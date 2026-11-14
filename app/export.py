import csv 

def write_transactions(file_path, transactions, fieldnames=None):
    """
    Export transaction records to a CSV file.

    Writes a header row followed by transaction records.
    Uses default transaction columns unless custom fieldnames
    are provided.

    Args:
        file_path (str): Destination CSV file path.
        transactions (list[dict]): Records to export.
        fieldnames (list[str] | None): Optional CSV column names.

    Returns:
        None
    """ 
    if fieldnames is None: 
        fieldnames = [
            "transaction_id", 
            "customer_id", 
            "amount"
        ] 

    with open(file_path, "w", newline ="") as file: 
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        writer.writeheader() 

        for transaction in transactions: 
            writer.writerow(transaction) 