-- Create the transactions table if it does not exist.

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    amount NUMERIC(12, 2) NOT NULL
);