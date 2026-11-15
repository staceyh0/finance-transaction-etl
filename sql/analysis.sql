-- customer transaction summary 
SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount,
    ROUND(AVG(amount), 2) AS average_amount
FROM transactions
GROUP BY customer_id
ORDER BY total_amount DESC;

-- High-Value customers 
WITH customer_totals AS (
    SELECT
        customer_id,
        SUM(amount) AS total_amount
    FROM transactions
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_amount
FROM customer_totals
WHERE total_amount > (
    SELECT AVG(total_amount)
    FROM customer_totals
)
ORDER BY total_amount DESC;

-- Ranking customers by transaction value 
SELECT
    customer_id,
    SUM(amount) AS total_amount,
    RANK() OVER (
        ORDER BY SUM(amount) DESC
    ) AS customer_rank
FROM transactions
GROUP BY customer_id
LIMIT 10;
