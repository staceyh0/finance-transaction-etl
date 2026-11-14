import csv 

def write_transactions(file_path, transactions, fieldnames=None): 
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